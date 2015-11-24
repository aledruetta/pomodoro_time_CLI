#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Script Name:          pomodoro.py
# Author:               Alejandro Druetta
# Version:              0.1
#
# Description:          Python 3 CLI pomodoro app.
#
# Usage:
#           ./pomodoro.py -opt <arg>
#           ./pomodoro.py -h
#           ./pomodoro.py -t <tag>

import sys
import subprocess
import getopt
from os import path
from time import time, gmtime, strftime, sleep


class PomodoroApp:
    def __init__(self):
        self._tag = ""
        self.tags = set()
        self.t_work = 0.3
        self.t_break = 0.1
        self.t_long = 0.2
        self.count = 0
        self.digits = {
            "0": [" ███ ",
                  "█   █",
                  "█   █",
                  "█   █",
                  " ███ "],

            "1": ["██",
                  " █",
                  " █",
                  " █",
                  " █"],

            "2": [" ███ ",
                  "█   █",
                  "   █ ",
                  "  █  ",
                  " ████"],

            "3": [" ███ ",
                  "█   █",
                  "   █ ",
                  "█   █",
                  " ███ "],

            "4": ["   █",
                  "  ██",
                  " █ █",
                  "████",
                  "   █"],

            "5": ["█████",
                  "█    ",
                  "█████",
                  "    █",
                  "█████"],

            "6": [" ███ ",
                  "█    ",
                  "████ ",
                  "█   █",
                  " ███ "],

            "7": ["████",
                  "   █",
                  "  █ ",
                  " █  ",
                  "█   "],

            "8": [" ███ ",
                  "█   █",
                  " ███ ",
                  "█   █",
                  " ███ "],

            "9": [" ███ ",
                  "█   █",
                  " ████",
                  "    █",
                  " ███ "],

            ":": [" █ ",
                  " █ ",
                  "   ",
                  " █ ",
                  " █ "]
                   }
        self.loop()

    def loop(self):
        while(True):
            self.clock(self.t_work)
            self.count += 1
            answer = self.ask("break", "work", "exit")
            if answer == "break":
                if self.count < 4:
                    self.clock(self.t_break)
                else:
                    self.clock(self.t_long)
                    self.count = 0
                answer = self.ask("work", "exit")

    def ask(self, *args):
        options = {}
        for arg in args:
            options[arg[0]] = arg

        chars = "/".join(sorted([key for key, value in options.items()]))
        words = ", ".join(sorted([value for key, value in options.items()]))
        message = "{} ({})? ".format(words.capitalize(), chars)
        icon_path = path.abspath("images/tomato.xpm")
        tmp = subprocess.call(
            'notify-send "Pomodoro Time" "What would you like to do now?"' +
            ' -i {}'.format(icon_path), shell=True
        )

        option = input(message).lower()
        while(option not in options.keys()):
            print("Invalid option!")
            option = input(message).lower()

        if options[option] == "exit":
            sys.exit(0)

        return options[option]

    def set_tag(self, tag):
        self._tag = tag
        self.tags.add(tag)

    def clock(self, minutes):
        if minutes == self.t_work:
            message = "Working... "
        elif minutes == self.t_break or minutes == self.t_long:
            message = "Coffe time... "

        finish = time() + minutes * 60
        while(time() < finish):
            tmp = subprocess.call('clear', shell=True)
            seconds = finish - time()
            remaining = gmtime(seconds)
            print(message)
            self.show(strftime("%M:%S", remaining))
            sleep(1)

    def show(self, string):
        lcd = ["" for i in range(5)]

        for char in string:
            digit = self.digits[char]
            for i in range(5):
                line = digit[i]
                lcd[i] += line + " "

        for i in range(5):
            print(lcd[i])

    def help(self):
        print("""
usage:
    pomodoro.py -opt <arg>

    -h, --help      Print usage
    -t, --tag       Start with taged cicle

examples:
    pomodoro.py -h
    pomodoro.py -t develop
""")


def main(argv):
    pomodoro = PomodoroApp()
    try:
        # Parse terminal arguments
        opts, args = getopt.getopt(argv, "ht:", ["help", "tag="])
    except getopt.GetoptError:
        print("Invalid! Try `pomodoro.py --help' for more information.")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            pomodoro.help()
            sys.exit(0)
        elif opt in ("-t", "--tag"):
            pomodoro.set_tag(arg)

if __name__ == '__main__':
    main(sys.argv[1:])
