import tkinter as tk
from tkinter import *
import cv2
from PIL import Image, ImageTk
import datetime as dt
from tkinter import ttk
from datetime import datetime
import pytz
import csv

#VIDEO FRAME
width, height = 600, 500
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

#face cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


#WINDOW FRAME
root = tk.Tk()
root.resizable(False, False)
root.geometry("1417x720")
IST = pytz.timezone('Asia/Manila')
lmain = tk.Label(root)
lmain.place(x=30, y=60)
my_tree = ttk.Treeview(root)

bg = PhotoImage(file="./banner.png")
bg_label = Label(root, image=bg)
bg_label.place(x=0, y=480, height=300)

ico = Image.open('./logo.png')
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)

root.title('Isabela State University Cauayan Campus')


#TAKING PICS
def snapshot():
    img = Image.fromarray(img)
    time = str(dt.datetime.now().today()).replace(":"," ")+ ".jpg"
    img.save(time)

#FRAME
def show_frame():
    global cv2image
    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(5, show_frame)
    #faces = face_classifier.detectMultiScale(gray, 1.1, 4)
    #for (x, y, w, h) in faces:
        #cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    #faces = face_classifier.detectMultiScale(cv2image, 1.1, 5, minSize=(10, 10))
    #for (x, y, w, h) in faces:
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
    #return faces

def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    for (x, y, w, h) in faces:
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
    return faces

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

#COLUMN TREE
my_tree.tag_configure('orow', background="#EEEEEE", font=('Verdana', 10))
my_tree.place(x=730, y=60, height=260)

#BODY
label2 = tk.Label(root, text="ISU-CC INSTRUCTORS ATTENDANCE", font=('Verdana', 20, 'bold'))
label2.place(x=500,y=0)

Button(text="CHECK IN", command=snapshot, font=('Verdana', 15, 'bold'), width=15, height=1, bg='SpringGreen4', foreground='white').place(x=730, y=340)
Button(text="CHECK OUT", font=('Verdana', 15, 'bold'), width=15, height=1, bg='SpringGreen4', foreground='white').place(x=1170, y=340)

label_time = tk.Label(root, text="Current Date and Time", font=('Verdana', 25, 'bold')).place(x=860, y=390)

label_date_now = tk.Label(text="Current Date", font = 'Verdana 20 bold')
label_date_now.place(x=730, y=450)

label_time_now = tk.Label(text="Current Time", font = 'Verdana 20 bold')
label_time_now.place(x=1150, y=450)

style = ttk.Style()
style.configure("Treeview.Heading", font=('Verdana', 13, 'bold'))

my_tree['columns'] = ("Date and Time", "Name")

my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Date and Time", anchor=CENTER, width=165)
my_tree.column("Name", anchor=CENTER, width=165)

my_tree.heading("Date and Time", text="Date and Time", anchor=CENTER)
my_tree.heading("Name", text="Name", anchor=CENTER)

# Read data from the CSV file and insert it into the table
with open('attendance.csv', 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        my_tree.insert('', 'end', values=row)


update_clock()
show_frame()
root.mainloop()
detect_bounding_box()