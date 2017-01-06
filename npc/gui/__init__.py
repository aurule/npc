"""
Package for handling the NPC windowed interface
"""

from tkinter import *
from tkinter.ttk import *

from .. import commands
from .. import main


def run():
    root = Tk()

    # set up the widgets
    npc_app = NPCApp(root)

    # run and done
    root.mainloop()
    root.destroy()

def startup_error(message):
    root = Tk()

    # set up the widgets
    error_window = StartupError(root, message)

    # run and done
    root.mainloop()
    root.destroy()

class NPCApp:
    def __init__(self, master):
        self.master = master

        master.title("NPC")
        master.positionfrom('user')
        master.minsize(width=200, height=300)

        frame = Frame(master)
        frame.pack()

        self.quit_button = Button(frame, text="QUIT", command=frame.quit)
        self.quit_button.pack(side=LEFT)

        self.hi_button = Button(frame, text="Hello", command=self.say_hi)
        self.hi_button.pack(side=LEFT)

    def say_hi(self):
        print("hi there, everyone!")

class StartupError:
    def __init__(self, master, message):
        master.title("NPC - Startup Error!")
        master.positionfrom('user')

        frame = Frame(master)
        frame.pack()

        self.error_text = Message(frame, text=message)
        self.error_text.pack()

        self.quit_button = Button(frame, text="Quit", command=frame.quit)
        self.quit_button.pack()
