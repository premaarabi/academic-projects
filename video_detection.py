import cv2
import torch
import speech_recognition as sr
import pyttsx3

# Initialize the recognizer and speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Load YOLO model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or load from local path

# Initialize webcam
cap = cv2.VideoCapture(0)

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for the command
def listen_for_command():
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"Command received: {command}")
            return command.lower()
        except Exception:
            print("Sorry, I did not understand that.")
            return None

# Function to describe the objects detected
def describe_objects(objects):
    if objects:
        description = "Objects detected: " + ", ".join(objects)
    else:
        description = "No objects detected."
    speak(description)

# Function to annotate image with detected objects
def annotate_image(frame, results):
    # Extract boxes, labels, and confidence scores
    boxes = results.xyxy[0]  # Coordinates of bounding boxes
    labels = results.names  # Class names
    class_ids = results.xyxy[0][:, -1].int()  # Detected class IDs

    detected_classes = []

    # Annotate the image with labels and bounding boxes
    for i, box in enumerate(boxes):
        x1, y1, x2, y2, confidence, class_id = box.tolist()
        label = labels[int(class_id)]  # Get the label from the class ID
        detected_classes.append(label)

        # Draw bounding box and label on the image
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
        cv2.putText(frame, f'{label} {confidence:.2f}', (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    return frame, detected_classes

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to access the camera.")
        break

    # Perform inference on the live camera feed
    results = model(frame)
    annotated_frame, live_classes = annotate_image(frame, results)

    # Show the live camera feed with annotations
    cv2.imshow("Live Camera Feed", annotated_frame)

    # Provide live voice feedback on detected objects
    describe_objects(live_classes)

    # Listen for command
    command = listen_for_command()
    if command:
        if "click photo" in command:
            print("Command received: 'Click Photo'. Capturing image...")
            speak("Photo clicked. Image capturing...")

            # Perform inference on the captured frame
            results = model(frame)

            # Annotate image with detected objects
            annotated_frame, detected_classes = annotate_image(frame, results)

            # Show the annotated image
            cv2.imshow("Captured Image - Object Detection", annotated_frame)

            # Provide voice feedback on detected objects
            describe_objects(detected_classes)

            # Wait for user to press any key to close the captured image window
            cv2.waitKey(0)
        elif "stop" in command:
            print("Command received: 'Stop'. Stopping the live feed.")
            speak("Stopping the live feed.")
            break  # Exit the loop to stop the live feed

    # Quit the live feed on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()