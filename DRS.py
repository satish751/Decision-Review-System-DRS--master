import tkinter
from PIL import Image, ImageTk
import cv2
from functools import partial
import threading
import imutils
import time

stream = cv2.VideoCapture("clip.mp4")
flag = True
def play(speed):
	global flag
	frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
	stream.set(cv2.CAP_PROP_POS_FRAMES, frame1+speed)

	grabbed, frame = stream.read()
	if not grabbed:
		exit()
	frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
	frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
	canvas.image = frame
	canvas.create_image(0, 0, image=frame, anchor = tkinter.NW)
	if flag:
		canvas.create_text(134, 26, fill="red", font="Times 25 bold", text="Decision Panding")
	flag = not flag


def pending(decision):
	
	# Dispaly decision pending image
	frame = cv2.cvtColor(cv2.imread("pending.jpg"), cv2.COLOR_BGR2RGB)
	frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
	frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
	canvas.image = frame
	canvas.create_image(0, 0, image=frame, anchor = tkinter.NW)
	# Wait for 1 sec
	time.sleep(1)
	# Dispaly sponser image
	frame = cv2.cvtColor(cv2.imread("wallpaper.jpg"), cv2.COLOR_BGR2RGB)
	frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
	frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
	canvas.image = frame
	canvas.create_image(0, 0, image=frame, anchor = tkinter.NW)
	# Wait for 1.5 sec
	time.sleep(1.5)
	# Dispaly out/not_out image
	if decision == "out":
		decisionImage = "out1.jpg"
	else:
		decisionImage = "not_out.jpg"
	frame = cv2.cvtColor(cv2.imread(decisionImage), cv2.COLOR_BGR2RGB)
	frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
	frame = ImageTk.PhotoImage(image=Image.fromarray(frame))
	canvas.image = frame
	canvas.create_image(0, 0, image=frame, anchor = tkinter.NW)



def out():
	thread = threading.Thread(target=pending, args=("out",))
	thread.daemon = 1
	thread.start()
	print("Player is out")

def not_out():
	thread = threading.Thread(target=pending, args=("not_out",))
	thread.daemon = 1
	thread.start()
	print("Player is not out")

# Width and Height of our main screen
SET_WIDTH = 650
SET_HEIGHT = 368

# tkinter GUI starts here
window = tkinter.Tk()
window.title("Third umpire DRS")
cv_img = cv2.cvtColor(cv2.imread("Welcome.jpg"),cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, ancho=tkinter.NW, image=photo)
canvas.pack()


#Buttons to control playback
btn = tkinter.Button(window, text="<< Previous (fast)",width=50, command=partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text="<< Previous (slow)",width=50, command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text=" Next (slow) >>",width=50, command=partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text=" Next (fast) >>",width=50, command=partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text=" Out ",width=50, command=out)
btn.pack()

btn = tkinter.Button(window, text=" Not Out",width=50, command=not_out)
btn.pack()


window.mainloop()

