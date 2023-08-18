import tkinter as tk
from PIL import Image, ImageTk
import cv2

# https://stackoverflow.com/questions/50922175/to-show-video-streaming-inside-frame-in-tkinter

def createVideoPage(window):
    placeholder = Image.open('./assets/placeholder.jpg')
    placeholder2 = placeholder.resize((410,339))
    placeholder1 = ImageTk.PhotoImage(placeholder)
    placeholder2 = ImageTk.PhotoImage(placeholder2)

    contentFrame = tk.Frame(window,bg="#000023")

    contentFrame.rowconfigure(0,weight=1)
    contentFrame.columnconfigure(0,weight=1)
    contentFrame.columnconfigure(1,minsize=5)
    contentFrame.columnconfigure(2,minsize=50)

    outgoingVideo = tk.Label(contentFrame, image=placeholder2, bg="#000023", justify="right", anchor="n")
    outgoingVideo.grid(row=0,column=2,sticky="n")

    incomingVideo = tk.Label(contentFrame, image=placeholder1, bg="#000023", justify="left", anchor="w")
    incomingVideo.grid(row=0,column=0,sticky="w")

    metricsFrame = tk.Frame(contentFrame, height=100,bg="#000023")
    metricsFrame.grid(row=0,column=2,sticky="s")
    metricsFrame.columnconfigure(0,weight=1)
    metricsFrame.rowconfigure(0,weight=1)
    metricsFrame.rowconfigure(1,weight=1)
    metricsFrame.rowconfigure(2,weight=2)

    accumKeyLabel = tk.Label(metricsFrame, text="Accumulated Secret Key", bg="#000023",fg="White", font="Helvetica 12")
    accumKey = tk.Label(metricsFrame, text="some# Mbits", bg="white",fg="black", font="Helvetica 20")
    accumKeyLabel.grid(row=0,column=0)
    accumKey.grid(row=1,column=0,padx=50)

    spaceFiller = tk.Label(metricsFrame,text="k",bg="#000023",fg="#000023",font="Helvetica 150")
    # spaceFiller.grid(row=2,column=0)

    return contentFrame, placeholder1, placeholder2, incomingVideo, outgoingVideo


# def video_stream(cap, frame):
#     _, frame = cap.read()
#     cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
#     img = Image.fromarray(cv2image)
#     imgtk = ImageTk.PhotoImage(image=img)
#     frame.imgtk = imgtk
#     frame.configure(image=imgtk)
#     frame.after(1, video_stream) 