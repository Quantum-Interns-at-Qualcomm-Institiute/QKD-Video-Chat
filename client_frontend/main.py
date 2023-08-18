import tkinter as tk
from components import header
from pages import createConnectPage, createVideoPage
from PIL import Image, ImageTk

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

videoPage, placeholder1, placeholder2 = createVideoPage.createVideoPage(window)
connectPage = createConnectPage.createConnectPage(window, videoPage)

connectPage.grid(row=1,column=0,)
window.mainloop()