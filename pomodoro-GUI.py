#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Script Name:          pomodoro-GUI.py
# Author:               Alejandro Druetta
# Version:              0.1
#
# Description:          Python 3 GUI pomodoro app.
#
# Usage:

import tkinter as tk
from tkinter import Tk, Frame, Label, Button, StringVar
import sqlite3 as sql
import sys
from os import path
from time import time, gmtime, strftime, sleep


class Pomodoro(Frame):
    def __init__(self, parent, abspath):
        super().__init__(parent)
        self.top = parent
        self.abspath = abspath
        self.t_work = 25
        self.t_break = self.t_work * 0.2
        self.t_long = self.t_work * 0.6
        self.initUI()

    def initUI(self):
        # toplevel
        self.top.title("PomodoroPy")
        self.top.resizable(0, 0)

        # main frame
        self["relief"] = "solid"
        self.pack()

        self.time = StringVar()
        self.time.set("25:00")

        self.timeLabel = Label(self, textvariable=self.time)
        self.timeLabel["padx"] = "10px"
        self.timeLabel["font"] = "helvetica 48 bold"
        self.timeLabel["relief"] = "raised"
        self.timeLabel.pack(expand=True, fill=tk.X)

        self.buttonFrame = Frame(self)
        self.buttonFrame.pack(expand=True, fill=tk.X)

        self.breakButton = Button(self.buttonFrame)
        self.breakButton["text"] = "Break"
        self.breakButton["font"] = "helvetica 16"
        self.breakButton.pack(expand=True, fill=tk.X)

        self.workButton = Button(self.buttonFrame)
        self.workButton["text"] = "Work"
        self.workButton["font"] = "helvetica 16"
        self.workButton.pack(expand=True, fill=tk.X)

        self.tag = StringVar()
        self.tag.set("unknown")

        self.statusLabel = Label(self, textvariable=self.tag)
        self.statusLabel["relief"] = "ridge"
        self.statusLabel.pack(expand=True, anchor=tk.NW)

    def main_loop(self):
        break_count = 0

        while(True):
            self.clock(self.t_work)

    def clock(self, minutes):
        if minutes == self.t_work:
            color = "blue"
        elif minutes == self.t_break:
            color = "green"
        elif minutes == self.t_long:
            color = "orange"

        self.timeLabel["fg"] = color

        finish = time() + minutes * 60
        while(time() < finish):
            seconds = finish - time()
            remaining = gmtime(seconds)
            self.time.set(strftime("%M:%S", remaining))
            sleep(1)


def main():
    dirname = path.dirname(sys.argv[0])
    abspath = path.abspath(dirname)
    top = Tk()
    app = Pomodoro(top, abspath)
    top.mainloop()


if __name__ == '__main__':
    main()
