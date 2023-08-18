import tkinter as tk
from PIL import Image, ImageTk

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

    incomingVideo = tk.Label(contentFrame, image=placeholder1, bg="#000023", justify="left", anchor="w")
    incomingVideo.grid(row=0,column=0,sticky="w")

    outgoingVideo = tk.Label(contentFrame, image=placeholder2, bg="#000023", justify="right", anchor="n")
    outgoingVideo.grid(row=0,column=2,sticky="n")


    return contentFrame, placeholder1, placeholder2