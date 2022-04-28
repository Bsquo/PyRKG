import PIL.Image
import PIL.ImageTk
import time
from tkinter import *
import traceback
from .Controller import Controller
from .CONFIG import TESTSUITE_SIZE, TESTSUITE_VERBOSE

class TestSuite:

    def __init__(self, layout):
        self.layout = layout
        self.controller = Controller()
        self.win = Tk()
        self.win.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.win.geometry(f"{TESTSUITE_SIZE[0]}x{TESTSUITE_SIZE[1]}")
        self.closed = False

        # input buttons
        self.a_v = IntVar()
        a = Checkbutton(self.win, variable=self.a_v, text="A")
        a.grid(column=0, row=0, sticky=W)
        self.b_v = IntVar()
        b = Checkbutton(self.win, variable=self.b_v, text="B")
        b.grid(column=1, row=0, sticky=W)
        self.x_v = IntVar()
        x = Checkbutton(self.win, variable=self.x_v, text="X")
        x.grid(column=2, row=0, sticky=W)
        self.y_v = IntVar()
        y = Checkbutton(self.win, variable=self.y_v, text="Y")
        y.grid(column=3, row=0, sticky=W)
        self.l_v = IntVar()
        l = Checkbutton(self.win, variable=self.l_v, text="L")
        l.grid(column=4, row=0, sticky=W)
        self.r_v = IntVar()
        r = Checkbutton(self.win, variable=self.r_v, text="R")
        r.grid(column=5, row=0, sticky=W)
        self.first_person_v = IntVar()
        first_person = Checkbutton(self.win, variable=self.first_person_v, text="1st Person Enabled")
        first_person.grid(column=6, row=0, sticky=W)

        self.hor_v = IntVar(self.win)
        self.hor_v.set(7)
        hor = OptionMenu(self.win, self.hor_v, *range(0, 15))
        hor.grid(column=7, row=0, sticky=W)

        self.vert_v = IntVar(self.win)
        self.vert_v.set(7)
        vert = OptionMenu(self.win, self.vert_v, *range(0, 15))
        vert.grid(column=8, row=0, sticky=W)

        # canvas
        self.label = Label(self.win)
        self.label.grid(row=1, columnspan=10)
        self.label.grid_rowconfigure(1, weight=1)
        self.label.grid_columnconfigure(1, weight=1)

    def on_closing(self):
        self.closed = True
        self.win.destroy()

    def update_image(self):
        # don't update the image if something went wrong while parsing the config file
        # to prevent error spamming in the terminal the error is only printed if it is new
        try:
            self.controller.read_json(self.layout)
        except Exception as e:
            if str(e) != self.last_error:
                self.last_error = str(e)
                if TESTSUITE_VERBOSE:
                    print(traceback.format_exc())
                else:
                    print(e)
        else:
            self.last_error = ""
            self.controller.process_inputs_and_draw(self.get_inputs(), False, True, True, False)
            self.tkimage = PIL.ImageTk.PhotoImage(self.controller.canvas.canvas)
            self.label.configure(image=self.tkimage)

    def start_loop(self):
        self.last_error = ""
        self.update_image()
        start_time = time.time()
        while not self.closed:
            if time.time() - start_time >= 0.5: # update every half a second
                start_time = time.time()
                self.update_image()
            self.win.update()

    def get_inputs(self):
        return (str(self.a_v.get()), str(self.b_v.get()), str(self.x_v.get()), str(self.y_v.get()), str(self.r_v.get()), str(self.l_v.get()), str(self.first_person_v.get()), self.hor_v.get(), self.vert_v.get())


if __name__ == "__main__":
    t = TestSuite("mk7")
    t.start_loop()