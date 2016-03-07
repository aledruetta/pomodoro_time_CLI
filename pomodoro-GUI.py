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

# Constants
T_WORK = 0.5
T_BREAK = T_WORK * 0.2
T_LONG = T_WORK * 0.6


class Pomodoro(Frame):

    def __init__(self, parent, abspath):
        super().__init__(parent)
        self.top = parent
        self.abspath = abspath

        self.work_count = 0

        # Tk variables
        self.tagVar = StringVar()
        self.tagVar.set("unknown")
        self.actionVar = StringVar()
        self.actionVar.set("Work")
        self.displayVar = StringVar()
        self.displayVar.set("00:00")

        self.initUI()

    def initUI(self):
        # toplevel
        self.top.title("PomodoroPy")
        self.top.resizable(0, 0)

        # main frame
        self["relief"] = "solid"
        self.pack()

        self.timeLabel = Label(self, textvariable=self.displayVar)
        self.timeLabel["padx"] = "10px"
        self.timeLabel["font"] = "helvetica 48 bold"
        self.timeLabel["relief"] = "raised"
        self.timeLabel["fg"] = "gray"
        self.timeLabel.pack(expand=True, fill=tk.X)

        self.buttonFrame = Frame(self)
        self.buttonFrame.pack(expand=True, fill=tk.X)

        self.actionButton = Button(self.buttonFrame)
        self.actionButton["text"] = "Work"
        self.actionButton["font"] = "helvetica 16"
        self.actionButton["command"] = lambda: self.action(
            self.actionButton.cget("text"))
        self.actionButton.pack(expand=True, fill=tk.X)

        self.statusLabel = Label(self, textvariable=self.tagVar)
        self.statusLabel["relief"] = "ridge"
        self.statusLabel.pack(expand=True, anchor=tk.NW)

    def action(self, action):
        if action == "Work":
            self.work_count += 1
            self.timeLabel["fg"] = "blue"
            self.actionButton["text"] = "Pause"
            self.clock(T_WORK)
            self.actionButton["text"] = "Break"
        elif action == "Pause":
            self.timeLabel["fg"] = "red"
            self.actionButton["text"] = "Continue"
        elif action == "Continue":
            self.timeLabel["fg"] = "blue"
            self.actionButton["text"] = "Pause"
        elif action == "Break":
            self.actionButton["state"] = "disabled"
            if self.work_count < 4:
                self.timeLabel["fg"] = "green"
                self.clock(T_BREAK)
            elif self.work_count >= 4:
                self.timeLabel["fg"] = "orange"
                self.clock(T_LONG)
                self.work_count = 0
            self.actionButton["state"] = "normal"
            self.actionButton["text"] = "Work"

    def clock(self, minutes):
        finish = time() + minutes * 60
        while(time() < finish):
            self.actionButton.update()
            if self.actionButton.cget("text") != "Continue":
                seconds = finish - time()
                remaining = gmtime(seconds)
                self.displayVar.set(strftime("%M:%S", remaining))
                self.update_idletasks()
                sleep(1)
            else:
                finish = time() + seconds


def main():
    dirname = path.dirname(sys.argv[0])
    abspath = path.abspath(dirname)
    top = Tk()
    app = Pomodoro(top, abspath)
    top.mainloop()


if __name__ == '__main__':
    main()
