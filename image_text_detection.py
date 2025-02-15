import cv2
import easyocr
import pyttsx3
import speech_recognition as sr

# Initialize the OCR reader and speech engine
reader = easyocr.Reader(['en'], gpu=True)
engine = pyttsx3.init()

# Initialize recognizer for voice commands
recognizer = sr.Recognizer()

# Initialize webcam
cap = cv2.VideoCapture(0)

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to process the frame for OCR
def process_frame_for_ocr(frame):
    # Perform OCR on the frame
    results = reader.readtext(frame)
    return results

# Function to annotate frame with OCR results
def annotate_frame(frame, results):
    for (bbox, text, conf) in results:
        (top_left, top_right, bottom_right, bottom_left) = bbox
        top_left = tuple(map(int, top_left))
        bottom_right = tuple(map(int, bottom_right))

        # Draw bounding box and text
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
        cv2.putText(frame, f'{text} ({conf:.2f})', (top_left[0], top_left[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    return frame

# Function to listen for voice command
def listen_for_command():
    with sr.Microphone() as source:
        print("Listening for a command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"Command received: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None

# Capture a single frame and perform OCR when a command is received
while True:
    command = listen_for_command()
    if command and "capture" in command:
        print("Command received: Capture. Taking a photo...")
        speak("Taking a photo.")

        # Capture a single frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture image.")
            break

        # Perform OCR on the captured frame
        ocr_results = process_frame_for_ocr(frame)

        # Annotate the frame with OCR results
        annotated_frame = annotate_frame(frame, ocr_results)

        # Display the annotated image
        cv2.imshow("Captured Image with OCR", annotated_frame)

        # Speak out the detected text
        if ocr_results:
            detected_texts = [text for _, text, _ in ocr_results]
            if detected_texts:
                speak("Detected text: " + ", ".join(detected_texts))

        # Wait for user to close the window
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        break

    elif command and "stop" in command:
        print("Command received: Stop. Exiting...")
        speak("Stopping the application.")
        break

# Release resources
cap.release()
cv2.destroyAllWindows()