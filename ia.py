import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition
import os
import csv
from datetime import datetime

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

known_images_path = 'img'

known_face_encodings = []
known_face_names = []

for filename in os.listdir(known_images_path):
    if filename.endswith((".jpg", ".png")):
        name = os.path.splitext(filename)[0]
        image = face_recognition.load_image_file(os.path.join(known_images_path, filename))
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(name)

# Create and open a CSV file for attendance tracking
csv_file = open('attendance.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)

detected_names = set()

def my_camera():
    return_cam, frame = cam.read()
    if not return_cam:
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    for (x, y, w, h) in faces:
        face = frame[y:y + h, x:x + w]
        rgb_face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(rgb_face)

        if len(face_encodings) > 0:
            matches = face_recognition.compare_faces(known_face_encodings, face_encodings[0])
            
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                
                if name not in detected_names:
                    # Record the current time
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Save the attendance record in the CSV file
                    csv_writer.writerow([current_time, name])
                    detected_names.add(name)
        
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = Image.fromarray(frame)
    frame = ImageTk.PhotoImage(image=frame)
    cap.config(image=frame)
    cap.image = frame
    
    root.after(10, my_camera)

root = tk.Tk()
root.resizable(False, False)
root.geometry("1080x720+50+50")
root.title("Face Recognition")

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

cap = tk.Label(root)
cap.pack()

my_camera()

root.mainloop()