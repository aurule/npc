"""
Package for handling the NPC windowed interface
"""

from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from subprocess import run

from .. import commands, main, settings

def start():
    root = Tk()

    # set up the widgets
    npc_app = NPCApp(root)

    # run and done
    root.mainloop()

class NPCApp:
    def __init__(self, master):
        self.prefs = settings.InternalSettings()
        self.master = master

        master.title("NPC")
        master.positionfrom('user')
        master.minsize(width=200, height=300)

        self.init_menubar()

    def init_menubar(self):

        menubar = Menu(self.master)

        file_menu = Menu(menubar, tearoff=False)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", underline=0, command=self.master.quit)
        menubar.add_cascade(label="File", underline=0, menu=file_menu)

        settings_menu = Menu(menubar, tearoff=False)
        settings_menu.add_command(label="User", underline=0, command=self.show_user_settings)
        menubar.add_cascade(label="Settings", underline=0, menu=settings_menu)

        help_menu = Menu(menubar, tearoff=False)
        help_menu.add_command(label="About", underline=0, command=self.show_about)
        menubar.add_cascade(label="Help", underline=0, menu=help_menu)

        self.master.config(menu=menubar)

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

    def show_user_settings(self):
        try:
            result = commands.open_settings('campaign', show_defaults=True)
        except AttributeError as err:
            messagebox.showerror("Error!", err)

        if not result.success:
            messagebox.showerror("Error!", result)

        if result.openable:
            run([self.prefs.get("editor")] + result.openable)

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
