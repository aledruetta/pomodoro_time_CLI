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
        self.t_work = 25
        self.t_break = self.t_work * 0.2    # 20%
        self.t_long = self.t_work * 0.6     # 60%
        self.count = 0
        # Styles: "Electronic", "Shadow", "Colossal"
        self.ascii_art = AsciiArt("Electronic")
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
        # Hide terminal cursor
        tmp = subprocess.call("setterm -cursor off", shell=True)

        if minutes == self.t_work:
            message = "Working... "
        elif minutes == self.t_break or minutes == self.t_long:
            message = "Coffe time... "

        finish = time() + minutes * 60
        while(time() < finish):
            tmp = subprocess.call('clear', shell=True)
            seconds = finish - time()
            remaining = gmtime(seconds)
            self.show(strftime("%M:%S", remaining))
            print(message)
            sleep(1)

        # Cursor ON
        tmp = subprocess.call("setterm -cursor on", shell=True)

    def show(self, string):
        digits = self.ascii_art.get_digits()
        hight = self.ascii_art.hight
        lcd = ["" for i in range(hight)]

        for char in string:
            for i in range(hight):
                lcd[i] += digits[char][i] + " "

        for i in range(hight):
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


class AsciiArt:
    def __init__(self, style):
        self.style = style
        self.hight = 0
        self.widths = []

    def get_template(self):
        with open("ascii.txt") as ascii_txt:
            count = 0
            flag = False
            template = []
            for line in ascii_txt:
                if flag and count < self.hight:
                    template.append(line.strip("\n"))
                    count += 1

                if self.style in line:
                    settings = line.strip().split(sep=":")
                    self.hight = int(settings[1])
                    self.widths = [int(width) for width in settings[-11:]]
                    flag = True

        return template

    def get_digits(self):
        template = self.get_template()
        digits = {}
        keys = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":")
        start = 0
        for i in range(len(keys)):
            key = keys[i]
            digits[key] = []
            end = start + self.widths[i]
            for j in range(self.hight):
                digits[key].append(template[j][start:end])
            start = end

        return digits


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
