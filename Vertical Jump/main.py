from tkinter.tix import Tk
import matplotlib
from tkinter import *

class Visualizer(Tk):
    
    def __init__(self):
        super(Visualizer, self).__init__()
        self.title("Vertical Jump")
        #self.minsize(1200, 1200)
        self.wm_iconbitmap("pp.ico")
        self.enter_data()
        #param = self.enter_data()
        #print(param)

    def quit(self):
        pass

    def start(self):
        pass
    
    
    def on_click(self, entry):
        print("GOVNO")
        txt = entry.get()
        print(txt)
        
    def enter_data(self):
        label = Label(text="Введите слово")
        report = ""
        entry = Entry(fg="yellow", bg="blue",  textvariable=report, width=50)
        entry.pack()
        entry.bind("<Return>", self.on_click)
        input_btn = Button(text="Ввести", command=self.on_click(entry)).pack()
        print(report)
        #input_btn.grid(column=1, row= 0)
        #entry.grid(column=0, row=0)
        #param = entry.get()
        #return param


class Human:
    def __init__(self, mass, height, sex, leg_girth, body_size, squat_depth, mcp = -1):
        self.mass = mass
        self.height = height
        self.sex = sex
        self.mcp = mcp
        self.leg_girth = leg_girth
        self.body_size = body_size
        self.squat_depth = squat_depth


class VerticalJumpEvaluation:
    def __init__(self, human):
        self.human = human
    
    def evaluate_mcp(self): # обхват голени, размер туловища
        if self.human.mcp == -1:

            if self.human.sex == "M":
                self.human.mcp = 11.066 + 0.675 * self.human.height - \
                    0.173 * self.human.leg_girth - 0.299 * self.human.body_size
            else:
                self.mcp = -4.667 + 0.289 * self.height + \
                    0.383 * self.human.leg_girth + 0.301 * self.human.body_size

        return self.mcp
    

        


if __name__ == "__main__":
    test_m = VerticalJumpEvaluation(57, 178, "F", 100000000)
    print(test_m.evaluate_mcp(30, 45))
    visualize = Visualizer()
    visualize.mainloop()

