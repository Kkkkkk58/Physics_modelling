from tkinter.tix import Tk
import matplotlib
from tkinter import *

class Visualizer(Tk):
    def __init__(self):
        super(Visualizer, self).__init__()
        self.title("Vertical Jump")
        #self.minsize(1200, 1200)
        self.wm_iconbitmap("pp.ico")
        param = self.enter_data()
        print(param)

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
        input_btn = Button(text="Ввести", command=self.on_click(entry)).pack()
        print(report)
        #input_btn.grid(column=1, row= 0)
        #entry.grid(column=0, row=0)
        param = entry.get()
        return param




class VerticalJumpEvaluation:
    def __init__(self, mass, height, sex, squat_depth, mcp = -1):
        self.mass = mass
        self.height = height
        self.sex = sex
        self.mcp = mcp
        self.squat_depth = squat_depth
    
    def evaluate_mcp(self, leg_girth, body_size): # обхват голени, размер туловища
        if self.mcp == -1:

            if self.sex == "M":
                self.mcp = 11.066 + 0.675 * self.height - 0.173 * leg_girth - 0.299 * body_size
            else:
                self.mcp = -4.667 + 0.289 * self.height + 0.383 * leg_girth + 0.301 * body_size

        return self.mcp
    

        


if __name__ == "__main__":
    test_m = VerticalJumpEvaluation(57, 178, "F", 100000000)
    print(test_m.evaluate_mcp(30, 45))
    visualize = Visualizer()
    visualize.mainloop()

