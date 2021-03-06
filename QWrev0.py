# Quality Window Rev 0
# December 16, 2017
# Newest data: 12/1/2017 13:35

import datetime
import socket
import sys
import time
from datetime import datetime
import logging
# import mysql.connector
import pandas as pd
import tkinter as tk
from tkinter import ttk

import joepulp

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import urllib
import json

import pandas as pd
import numpy as np

from matplotlib import pyplot as plt

# Capture Host Name (computer name)
hostname = socket.gethostname()
# Create and configure logger
LOG_FORMAT = '%(asctime)s:%(levelname)s:  %(message)s'
logging.basicConfig(filename= "B:\\logfiles\\QWindow.log",
                    level = logging.DEBUG,
                    format = LOG_FORMAT)
logger = logging.getLogger()
logger.info('QWindow rev0.0 started on: {}'.format(hostname))

nnow = "12/1/2017 13:35"

df = pd.read_csv('pe.csv')
df.head()

df2 = df[(df.week_num.isin ([47])) & \
         (df.SamplePoint<8) & \
         (df.SamplePoint>0) & \
         (df.millday == 'Tuesday')]

LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

f = Figure()
a = f.add_subplot(111)


def LookBack(hours):
    print(hours)

def animate(i):
    a.clear()

    # plt.scatter(df2.CSF, df2.FL, c = df2.SamplePoint, alpha=0.4)
    # plt.ylabel('\nFibre Length (mm)')
    # plt.xlabel('Freeness (ml)\n')
    # plt.xticks()

    a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3,
             ncol=2, borderaxespad=0)

    title = "Quality Window"
    a.set_title(title)
    # a.plot(df2.CSF, df2.FL)

    a.scatter(df2.CSF, df2.FL, c=df2.SamplePoint, alpha=0.4)
    a.ylabel('\nFibre Length (mm)')
    a.xlabel('Freeness (ml)\n')
    a.xticks()
    a.title('Quality Window\nFreeness vs Fibre Length\n')
    a.legend(df.PulpName)
    a.grid()


class QWindow(tk.Tk):



    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "TMP Quality Window")
        tk.Tk.iconbitmap(self, default="PHP.ico")

        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command=lambda: popupmsg("Not supported just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        settingsmenu = tk.Menu(menubar, tearoff=1)
        settingsmenu.add_command(label="Show last 4 hours", command=lambda: LookBack(4))
        settingsmenu.add_command(label="Show last 8 hours", command=lambda: LookBack(8))
        settingsmenu.add_command(label="Show last 12 hours", command=lambda: LookBack(12))
        settingsmenu.add_command(label="Show last 24 hours", command=lambda: LookBack(24))
        settingsmenu.add_command(label="Show last week", command=lambda: LookBack(joepulp.admtpd(1000,3)))
        settingsmenu.add_separator()
        settingsmenu.add_command(label="Save settings", command=lambda: print("Computer Name: ", hostname))
        settingsmenu.add_separator()
        settingsmenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="Settings", menu=settingsmenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        frame = StartPage(container, self)
        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky='nsew')
        logger.debug("StartPage init")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        # label.pack(pady=10, padx=10)

        # button2 = ttk.Button(self, text="Exit",
        #                      command=quit)
        # button2.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = QWindow()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, interval=5000)
app.mainloop()
