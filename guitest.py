# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 23:17:07 2023

@author: en_lo
"""

import tkinter as tk
gui = tk.Tk()
gui.geometry("300x100")
def getEntry():
    res = myEntry.get()
    print(res)
    
myEntry = tk.Entry(width=40)
myEntry.pack(pady=20)
btn = tk.Button(height=1, width=10, text="Read", command=getEntry)
btn.pack()
gui.mainloop()