import tkinter as tk

def handleConnect(codeField, contentFrame, videoPage):
    inp = codeField.get(1.0,"end-1c")
    # Attempt to connect
    if len(inp) > 0 and inp != "Invalid": # Connect Succeded
        contentFrame.grid_forget()
        videoPage.grid(row=1,column=0,padx=40,pady=40)
    else:
        codeField.delete(1.0,"end-1c")
        codeField.insert(1.0,"Invalid")

def createConnectPage(window, createVideoPage):
    contentFrame = tk.Frame(window,bg="#000023")
    contentFrame.rowconfigure(0, weight=1)
    contentFrame.rowconfigure(1, weight=1)
    contentFrame.columnconfigure(0, weight=1)

    connectButton = tk.Button(contentFrame, text="Connect",height=1,font="Helvetica 10", command=lambda:handleConnect(codeField, contentFrame, createVideoPage))

    codeFrame = tk.Frame(contentFrame,bg="#000023")
    codeFrame.rowconfigure(0, weight=1)
    codeFrame.rowconfigure(1, weight=1)
    codeFrame.columnconfigure(0, weight=1)

    codeLabel = tk.Label(codeFrame, text="Connection Code:", bg="#000023", fg="#ffffdc", font="Helvetica 15")
    codeField = tk.Text(codeFrame,height=1,width=10,bg="white",
    font="Helvetica 20")

    codeLabel.grid(row=0, column=1)
    codeField.grid(row=1, column=1, pady=(0,20))

    codeFrame.grid(row=0,column=0,sticky="s")
    connectButton.grid(row=1,column=0,sticky="n")

    return contentFrame