#! /bin/libcamerify /bin/python3

import interface
import tkinter as tk
import os
import model

app_path = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    root = tk.Tk()
    root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(
        file=app_path+'/petri_icon.png'))

    mh = model.ModelHandler('models.yaml')

    app = interface.App(root, mh)
    app.mainloop()
