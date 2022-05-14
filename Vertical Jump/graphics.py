from enum import IntEnum
from tkinter.tix import Tk
from tkinter import *

class Values(IntEnum):
    IN_WEIGHT = 0
    IN_HEIGHT = 1
    IN_LEG_GIRTH = 2
    IN_BODY_SIZE = 3
    IN_SEX = 4
    IN_SQUAT = 5
    
Window = Tk()
#Window.geometry('1200x1200')
Window.title("Vertical jump model")
fullscreen_state = False
# Window.columnconfigure(0, minsize=250)
# Window.rowconfigure([0, 1, 2, 3, 4], minsize=20)
Entries = []
Labels = []
sex=StringVar()
sex.set("F")


def confirm():
    print( Entries[Values.IN_WEIGHT].get(), Entries[Values.IN_HEIGHT].get(), Entries[Values.IN_SEX].get(), Entries[Values.IN_LEG_GIRTH].get(), \
        Entries[Values.IN_BODY_SIZE].get(), Entries[Values.IN_SQUAT].get()  )
    
def toggle_fullscreen(event = None):
    global fullscreen_state
    fullscreen_state = not fullscreen_state
    Window.attributes("-fullscreen", fullscreen_state)
    return "break"

def shut_fullscreen(event = None):
    global fullscreen_state
    fullscreen_state = False
    Window.attributes("-fullscreen", fullscreen_state)
    return "break"

def set_screen():
    Window.bind("<F5>", toggle_fullscreen)
    Window.bind("<Escape>", shut_fullscreen)


def set_gui():
    set_screen()
    txtfont = ("Bahnschrift SemiCondensed", 12, "normal")
    Requests = ["Введите массу человека", "Введите рост человека", "Введите обхват голени в сантиметрах", \
        "Введите длину туловища в сантиметрах", "Введите пол", "Введите высоту приседа в сантиметрах"]

    for i in range(0, 4):
        Labels.append(Label(Window, text=Requests[i], font=txtfont))
        Labels[i].grid(column=0, row=i)
        Entries.append(Entry(Window, background="#C0C0C0"))
        Entries[i].grid(column=1, row = i)

    Labels.append(Label(Window, text = Requests[Values.IN_SEX], font=txtfont))
    Labels[Values.IN_SEX].grid(column = 0, row = 4, columnspan=3)
    sex0 = Radiobutton(Window, text="Мужчина", variable=sex, value="М")
    sex1 = Radiobutton(Window, text="Женщина", variable=sex, value="F")
    sex0.grid(column=0, row=5, ipadx=10, padx=20)
    sex1.grid(column=1, row=5, padx=0)
    Entries.append(sex)
    Labels.append(Label(Window, text = Requests[Values.IN_SQUAT], font=txtfont))
    Labels[Values.IN_SQUAT].grid(column=0, row=6, columnspan=2)
    squat = Scale(Window, from_= 0, to=60, orient=HORIZONTAL)
    Entries.append(squat)
    squat.grid(column=0, row=7, columnspan=3)
    img = PhotoImage(file="btn3.png")
    confirm_btn = Button(Window, text="Подтвердить", font=txtfont, image=img, border=1, command=confirm)
    confirm_btn.grid(column = 0, row = 10, columnspan=3)
    Window.mainloop()


#set_gui()