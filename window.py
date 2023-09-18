import tkinter as tk
from tkinter import *
import cv2
from PIL import Image, ImageTk
import datetime
from tkinter import ttk

#VIDEO FRAME
width, height = 600, 500
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

#WINDOW FRAME
root = tk.Tk()
root.resizable(False, False)
root.geometry("1417x720")
lmain = tk.Label(root)
lmain.place(x=50, y=60)
my_tree = ttk.Treeview(root)

#TAKING PICS
def snapshot():
    img = Image.fromarray(cv2image)
    time = str(datetime.datetime.now().today()).replace(":"," ")+ ".jpg"
    img.save(time)

#FRAME
def show_frame():
    global cv2image
    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(5, show_frame)

#COLUMN TREE
my_tree.tag_configure('orow', background="#EEEEEE", font=('Verdana', 10))
my_tree.place(x=730, y=440, height=260)

label2 = tk.Label(root, text="ISU Student Registration", font=('Verdana', 20, 'bold'))
label2.place(x=500,y=0)

Label(root, text="Instructors ID: ", font=('Verdana', 20, 'bold')).place(x=730, y=60)
Label(root, text="Name: ", font=('Verdana', 20, 'bold')).place(x=730, y=200)

Button(text="Check In", command=snapshot, font=('Verdana', 15, 'bold'), width=15, height=1, bg='SpringGreen4').place(x=730, y=340)
Button(text="Check Out", font=('Verdana', 15, 'bold'), width=15, height=1, bg='SpringGreen4').place(x=1150, y=340)

style = ttk.Style()
style.configure("Treeview.Heading", font=('Verdana', 13, 'bold'))

my_tree['columns'] = ("Instructor ID", "Name", "Time In", "Time Out")

my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Instructor ID", anchor=CENTER, width=165)
my_tree.column("Name", anchor=CENTER, width=165)
my_tree.column("Time In", anchor=CENTER, width=165)
my_tree.column("Time Out", anchor=CENTER, width=165)

my_tree.heading("Instructor ID", text="Instructor ID", anchor=CENTER)
my_tree.heading("Name", text="Name", anchor=CENTER)
my_tree.heading("Time In", text="Time In", anchor=CENTER)
my_tree.heading("Time Out", text="Time Out", anchor=CENTER)


show_frame()
root.mainloop()