import tkinter as tk
from tkinter import *
import cv2
from PIL import Image, ImageTk
import face_recognition
import os
import csv
from datetime import datetime
import datetime as dt
from tkinter import ttk
import pytz


cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# known_images_path = 'img/don'

known_images_path = ['img/don', 'img/ian', 'img/sonnie']

known_face_encodings = []
known_face_names = []

#Read the Path file 
for i in range(3):
    for filename in os.listdir(known_images_path[i]):
        if filename.endswith((".jpg", ".png")):
            name = os.path.splitext(filename)[0]
            image = face_recognition.load_image_file(os.path.join(known_images_path[i], filename))
            encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(encoding)
            known_face_names.append(name)


current_time = datetime.now().strftime('%Y-%m-%d')

# newname = 'attendance'+current_time+'.csv'
# Create and open a CSV file for attendance tracking
# csv_create = open('attendance'+current_time+'.csv', 'w')
# csv_writer = csv.writer(csv_create)




path_in = 'check_in'+ current_time+'.csv'
path_out = 'check_out'+ current_time+'.csv'

# Check whether the specified
# path exists or not
isExist_in = os.path.exists(path_in)
isExist_out = os.path.exists(path_out)


print(isExist_in, isExist_out)

if isExist_in == True and isExist_out == True:
# csv_file = open('attendance'+ current_time+'.csv','w', newline='')
    csv_file = open('check_in'+ current_time+'.csv','r+', newline='')
    csv_writer_in = csv.writer(csv_file)
    csv_file = open('check_out'+ current_time+'.csv','r+', newline='')
    csv_writer_out = csv.writer(csv_file)
else:
    csv_file = open('check_in'+ current_time+'.csv','w', newline='')
    csv_writer_in = csv.writer(csv_file)
    csv_file = open('check_out'+ current_time+'.csv','w', newline='')
    csv_writer_out = csv.writer(csv_file)


detected_names = set()

# def blah(pindot):
#     global btn_click
#     btn_click = pindot

# def out_check():
#     my_btn = btn_click
#     return my_btn
    
# def a():
#     b = out_check()
#     print(b)

# blah("")
# out_check()
# a()



# button_value = None

# # Function to handle button clicks
# def button_click(button_name):
#     global button_value
#     if button_name == "CHECK_IN":
#         button_value = "CHECK_IN"
#     elif button_name == "CHECK_OUT":
#         button_value = "CHECK_OUT"

# # Function to get the button value
# def get_button_value():
#     return button_value

# # Function to return the value without parameters
# def return_btn():
#     return get_button_value()


button_value = None

# Create a function to handle button clicks
def button_click(button_name):
    global button_value
    button_value = button_name

def my_camera():

    #para hindi dalawa yung window ng camera
    return_cam, frame = cam.read()
    if not return_cam:
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #thresh Hold
    #thresh = cv2.thresh
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1, minSize=(30, 30))
    
    #para sa rectangle at face recognition
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

                #PARA MAAPALITAN YUNG NAME NA ILALAGAY SA CSV AHHAHA PAKI GITPUSH NALANG 
                remove = "()123456789"
                for char in remove:
                    name = name.replace(char, "")

                
                if name not in detected_names:
                    # Record the current time
                    current_time = datetime.now().strftime('%H:%M:%S')

                    # attendance = get_button_value()
                    
                    if button_value == "CHECK_OUT":
                    # Save the attendance record in the CSV file
                        print("OUT")
                        csv_writer_out.writerow([current_time, name])
                        detected_names.add(name)
                    elif button_value == "CHECK_IN":
                        print("IN")
                        csv_writer_in.writerow([current_time, name])
                        detected_names.add(name)
                    else:
                        print("No Value")

                    # csv_writer_out.writerow([current_time, name])
                    # detected_names.add(name)
        
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    #para ma display sa tkinter yung opencv
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = Image.fromarray(frame)
    frame = ImageTk.PhotoImage(image=frame)
    cap.config(image=frame)
    cap.image = frame
    
    #para gumalaw yung video
    root.after(10, my_camera)

#alam mo na 'to
def update_clock():
    raw_TS = datetime.now(IST)
    date_now = raw_TS.strftime("%d %b %Y")
    time_now = raw_TS.strftime("%I:%M:%S %p")
    formatted_now = raw_TS.strftime("%d-%m-%Y")
    label_date_now.config(text = date_now)
    # label_date_now.after(500, update_clock)
    label_time_now.config(text = time_now)
    label_time_now.after(1000, update_clock)
    return formatted_now








#WINDOW
root = tk.Tk()
root.resizable(False, False)
root.geometry("1417x720+150+50")
IST = pytz.timezone('Asia/Manila')
root.title("Face Recognition")
my_tree = ttk.Treeview(root)


#position ng video feed
cap = tk.Label(root)
cap.place(x=30, y=60)

label_time = tk.Label(root, text="Current Date and Time", font=('Verdana', 25, 'bold')).place(x=860, y=390)

label_date_now = tk.Label(text="Current Date", font = 'Verdana 20 bold')
label_date_now.place(x=730, y=450)

label_time_now = tk.Label(text="Current Time", font = 'Verdana 20 bold')
label_time_now.place(x=1150, y=450)

Button(text="CHECK IN", font=('Verdana', 15, 'bold'), width=15, height=1, bg='SpringGreen4', foreground='white', command=lambda: button_click("CHECK_IN")).place(x=730, y=340)
Button(text="CHECK OUT", font=('Verdana', 15, 'bold'), width=15, height=1, bg='SpringGreen4', foreground='white', command=lambda: button_click("CHECK_OUT")).place(x=1170, y=340)



bg = PhotoImage(file="./banner.png")
bg_label = Label(root, image=bg)
bg_label.place(x=0, y=500, height=280)

label2 = tk.Label(root, text="ISU-CC INSTRUCTORS ATTENDANCE", font=('Verdana', 20, 'bold'))
label2.place(x=500,y=0)


my_tree.tag_configure('orow', background="#EEEEEE", font=('Verdana', 10))
my_tree.place(x=730, y=60, height=260)

#TREE VIEW
style = ttk.Style()
style.configure("Treeview.Heading", font=('Verdana', 13, 'bold'))

my_tree['columns'] = ("Date and Time", "Name")

my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Date and Time", anchor=CENTER, width=327)
my_tree.column("Name", anchor=CENTER, width=327)
my_tree.heading("Date and Time", text="Date and Time", anchor=CENTER)
my_tree.heading("Name", text="Name", anchor=CENTER)



update_clock()
my_camera()
root.mainloop()