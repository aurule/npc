"""
Package for handling the NPC windowed interface
"""

from tkinter import *
from tkinter.ttk import *

from .. import commands
from .. import main

def run():
    root = Tk()
    npc_app = NPCApp(root)
    root.mainloop()
    root.destroy()

def startup_error(message):
    raise NotImplementedError
    # TODO create a window that shows the error text with a quit button

class NPCApp:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.quit_button = Button(frame, text="QUIT", command=frame.quit)
        self.quit_button.pack(side=LEFT)

        self.hi_button = Button(frame, text="Hello", command=self.say_hi)
        self.hi_button.pack(side=LEFT)

    def say_hi(self):
        print("hi there, everyone!")
