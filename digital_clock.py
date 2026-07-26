from tkinter import*
from tkinter.ttk import*

from time import strftime

root=Tk()
root.title("Digital Clock")

def time():
    string =strftime("%H:%M:%S %p")
    lbl.config(text=string)
    lbl.after(1000,time)

lbl=Label(root,font=("Arial",50,"bold"),background="black",foreground="cyan")

lbl.pack(anchor='center',pady=40)

time()

root.mainloop()