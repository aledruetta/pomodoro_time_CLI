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
from tkinter import Tk, Frame, Label, Button, Entry, StringVar
from pygame import mixer
import sqlite3 as sql
import sys
from os import path
from time import time, gmtime, strftime, sleep

DEBUG = True

# Constants
if DEBUG:
    T_WORK = 0.5
else:
    T_WORK = 25

T_BREAK = T_WORK * 0.2
T_LONG = T_WORK * 0.6

YELLOW = "#fcf3cf"
BLUE = "#2874a6"
RED = "#e74c3c"
GREEN = "#229954"
ORANGE = "#dc7633"

WORK = "Work"
PAUSE = "Pause"
CONTINUE = "Continue"
BREAK = "Break"


class Pomodoro(Frame):

    def __init__(self, parent, abspath):
        super().__init__(parent)
        self.root = parent
        self.abspath = abspath
        self.database = path.join(self.abspath, "database.db")

        self.work_count = 0

        # Tk variables
        self.tagVar = StringVar()
        self.tagVar.set("")
        self.actionVar = StringVar()
        self.actionVar.set(WORK)
        self.displayVar = StringVar()
        self.displayVar.set("00:00")

        self.initUI()

    def initUI(self):
        # toplevel
        self.root.title("PomodoroPy")
        self.root.resizable(0, 0)

        # main frame
        self.pack()

        self.entryTag = Entry(self, textvariable=self.tagVar)
        self.entryTag["font"] = "helvetica 14 bold"
        self.entryTag["fg"] = "gray"
        self.entryTag.pack(expand=True, fill=tk.X)

        self.timeLabel = Label(self, textvariable=self.displayVar)
        self.timeLabel["background"] = YELLOW
        self.timeLabel["padx"] = "10px"
        self.timeLabel["font"] = "helvetica 48 bold"
        self.timeLabel["fg"] = "gray"
        self.timeLabel.pack(expand=True, fill=tk.X)

        self.actionButton = Button(self)
        self.actionButton["text"] = WORK
        self.actionButton["font"] = "helvetica 16"
        self.actionButton["command"] = lambda: self.action(
            self.actionButton.cget("text"))
        self.actionButton.pack(expand=True, fill=tk.X)

    def catchTag(self, event=None):
        self.entryTag["state"] = "readonly"
        self.tagVar.set(self.tagVar.get().strip().upper())
        self.updateDB()

        # DEBUG | Delete for release
        if DEBUG:
            print(self.tagVar.get())

    def updateDB(self):
        conn = sql.connect(self.database)
        tag = self.tagVar.get().lower()
        with conn:
            if tag:
                cur = conn.cursor()
                count = cur.execute(
                    "SELECT count FROM tags WHERE tag_ID=?",
                    (tag,)).fetchone()
                print(tag, count)
                try:
                    cur.execute("UPDATE tags SET count=? WHERE tag_ID=?",
                                (count[0] + 1, tag))
                except TypeError:
                    cur.execute("INSERT INTO tags VALUES (?, ?)",
                                (tag, 1))
                finally:
                    conn.commit()

    def action(self, action):
        if action == WORK:
            self.catchTag()
            self.work_count += 1
            self.timeLabel["fg"] = BLUE
            self.actionButton["text"] = PAUSE
            self.clock(T_WORK)
            self.actionButton["text"] = BREAK
        elif action == PAUSE:
            self.timeLabel["fg"] = RED
            self.actionButton["text"] = CONTINUE
        elif action == CONTINUE:
            self.timeLabel["fg"] = BLUE
            self.actionButton["text"] = PAUSE
        elif action == BREAK:
            self.actionButton["state"] = "disable"
            if self.work_count < 4:
                self.timeLabel["fg"] = GREEN
                self.clock(T_BREAK)
            elif self.work_count >= 4:
                self.timeLabel["fg"] = ORANGE
                self.clock(T_LONG)
                self.work_count = 0
            self.entryTag["state"] = "normal"
            self.actionButton["state"] = "normal"
            self.actionButton["text"] = WORK

    def clock(self, minutes):
        finish = time() + minutes * 60
        while(time() < finish):
            self.actionButton.update()
            if self.actionButton.cget("text") != CONTINUE:
                seconds = finish - time()
                remaining = gmtime(seconds)
                self.displayVar.set(strftime("%M:%S", remaining))
                self.update_idletasks()
                sleep(1)
            else:
                finish = time() + seconds

        self.playSound()

    def playSound(self):
        mixer.init()
        soundPath = path.join(self.abspath, "sounds/alert2.mp3")
        mixer.music.load(soundPath)
        mixer.music.play()


def main():
    dirname = path.dirname(sys.argv[0])
    abspath = path.abspath(dirname)
    root = Tk()
    app = Pomodoro(root, abspath)
    root.mainloop()


if __name__ == '__main__':
    main()
