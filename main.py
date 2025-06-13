import tkinter as tk
from gui import GUIManager

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIManager(root)
    root.mainloop()