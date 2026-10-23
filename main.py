from tkinter import *
from tkinter import ttk, messagebox

from gui import GUI

def main():
    root = Tk()

    gui = GUI(
        root=root,
        resolution="1280x600"
        )

    root.mainloop()

if __name__ == "__main__":
    main()
