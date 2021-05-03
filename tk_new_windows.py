from tkinter import *

def openwindow():
    new_window = Toplevel(root)
    new_window.geometry("250x250")
    new_window.title("New Window")
    lbl = Label(new_window,text="I am in new window")
    lbl.pack()



root = Tk()

btn = Button(root,text="Open New Window",command=openwindow)
btn.pack(padx=20,pady=20)

root.geometry("500x500")
root.title("My Main window")






root.mainloop()