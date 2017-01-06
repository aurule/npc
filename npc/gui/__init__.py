"""
Package for handling the NPC windowed interface
"""

from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

from .. import commands
from .. import main

def run():
    root = Tk()

    # set up the widgets
    npc_app = NPCApp(root)

    # run and done
    root.mainloop()

class NPCApp:
    def __init__(self, master):
        self.master = master

        master.title("NPC")
        master.positionfrom('user')
        master.minsize(width=200, height=300)

        menubar = Menu(master)

        file_menu = Menu(menubar, tearoff=False)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=master.quit, underline=0)
        menubar.add_cascade(label="File", menu=file_menu, underline=0)

        help_menu = Menu(menubar, tearoff=False)
        help_menu.add_command(label="About", command=self.show_about, underline=0)
        menubar.add_cascade(label="Help", menu=help_menu, underline=0)

        master.config(menu=menubar)

    def show_about(self):
        message = "\n".join([
            "NPC Version {0}".format(main.VERSION),
            "",
            "GM helper script to manage game files.",
            "",
            "Copyright (c) 2015-2017 Peter Andrews",
            "Distributed under the MIT license"
        ])
        messagebox.showinfo("About NPC", message, parent=self.master)

def startup_error(message):
    root = Tk()

    # set up the widgets
    error_window = StartupError(root, message)

    # run and done
    root.mainloop()

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
