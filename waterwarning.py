from tkinter import *
from sys import exit

def popup(s):
    popupRoot = Tk()
    popupRoot.after(10000, popupRoot.destroy())
    popupButton = Button(popupRoot, text = s, font = ("Verdana", 12), bg = "yellow")
    popupButton.pack()
    popupRoot.geometry('600x50+700+500')
    popupRoot.mainloop()