import tkinter as tk
from PIL import Image, ImageTk

def createHeader(window):
    ucsdlogo = Image.open('./assets/ucsdlogo.png')
    ucsdlogo = ucsdlogo.resize((175,175))
    ucsdlogo = ImageTk.PhotoImage(ucsdlogo)
    header = tk.Frame(window, background='#000023')
    header.grid(row=0, column=0,sticky="nsew")

    header.rowconfigure(0,weight=1)
    header.columnconfigure(0,weight=1)
    header.columnconfigure(1,weight=4)
    header.columnconfigure(2,weight=1)

    headerFrames = [0]*3
    for i in range(3):
        headerFrames[i] = tk.Frame(header,background='#000023',padx=40,pady=40)
        headerFrames[i].grid(row=0,column=i,sticky="nsew")
        headerFrames[i].rowconfigure(0,weight=1)
        headerFrames[i].columnconfigure(0,weight=1)

    titleText = tk.Label(headerFrames[1], text = "QKD VIDEO CHAT", font=("Helvetica 50 bold"), bg="#000023", fg="#ffffdc")

    ucsdLogo1 = tk.Label(headerFrames[0], image=ucsdlogo, bg="#000023")
    ucsdLogo2 = tk.Label(headerFrames[2], image=ucsdlogo, bg="#000023")

    titleText.grid(row=0,column=0,sticky="n")
    ucsdLogo1.grid(row=0,column=0)
    ucsdLogo2.grid(row=0,column=0)

    return ucsdlogo
