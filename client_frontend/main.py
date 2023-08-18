import tkinter as tk
from components import header
from pages import createConnectPage, createVideoPage
from PIL import Image, ImageTk
import cv2

# class App(Tk):
    
#     def __init__(self):

#         Tk.__init__(self)

#         self.mainloop()
    
# if __name__ == "__main__":
#     App()



window = tk.Tk()
window.title("Quantum Video Chat by Qualcomm Institute")
window.geometry("1440x1024")
window.configure(background='#000023')

window.rowconfigure(0, minsize=255)
window.rowconfigure(1, weight=1)
window.columnconfigure(0, weight=1)

loadingText = tk.Label(window, text = "Establishing Encryption", font=("Helvetica 48 bold"), bg="#000023", fg="#ffffdc")

image = header.createHeader(window) # ghetto ass way to keep image reference from being garbage collected after function call ends

videoPage, placeholder1, placeholder2, incomingVideo, outgoingVideo = createVideoPage.createVideoPage(window)
connectPage = createConnectPage.createConnectPage(window, videoPage)



# Capture from camera
cap = cv2.VideoCapture(0)

# function for video streaming
def video_stream():
    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    incomingVideo.imgtk = imgtk
    incomingVideo.configure(image=imgtk)
    incomingVideo.after(1, video_stream)
    
    # outgoingVideo.imgtk = imgtk
    # outgoingVideo.configure(image=imgtk)
    # outgoingVideo.after(1, video_stream)

connectPage.grid(row=1,column=0,)
video_stream()
window.mainloop()