#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Script Name:          pomodoro.py
# Author:               Alejandro Druetta
# Version:              0.2.3
#
# Description:          Python 3 CLI pomodoro app.
#
# Usage:
#           ./pomodoro.py -opt <arg>
#
#           ./pomodoro.py -h            help
#           ./pomodoro.py -t <tag>      tagging
#           ./pomodoro.py -s <theme>    stylize

import sys
import subprocess
import getopt
from getopt import GetoptError
from pygame import mixer
from os import path
from time import time, gmtime, strftime, sleep


class PomodoroApp:
    def __init__(self, abspath):
        self.abspath = abspath
        self._tag = ""
        self.tags = set()
        self.t_work = 25                    # working time
        self.t_break = self.t_work * 0.2    # 20%
        self.t_long = self.t_work * 0.6     # 60%
        self.count = 0
        self.ascii_art = AsciiArt(self.abspath)

    def set_theme(self, theme):
        valid_themes = ("Electronic", "Colossal", "Shadow")
        if theme in valid_themes:
            self.ascii_art.style = theme

    def loop(self):
        while(True):
            status = self.clock(self.t_work)
            if status == 0:
                self.count += 1
            answer = self.ask("break", "work", "exit")
            if answer == "b":
                if self.count < 4:
                    status = self.clock(self.t_break)
                else:
                    status = self.clock(self.t_long)
                    self.count = 0
                answer = self.ask("work", "exit")

    def ask(self, *args):
        options = [arg[0] for arg in args]
        chars = "/".join(options)
        words = ", ".join(list(args))

        self.notify_send()
        self.play_sound()

        message = "\n{} ({})? ".format(words.capitalize(), chars)
        option = input(message).lower()
        while(option not in options):
            print("Invalid option!")
            option = input(message).lower()

        if option == "e":
            sys.exit(0)

        return option

    def notify_send(self):
        icon_path = path.join(self.abspath, "images/tomato.xpm")
        tmp = subprocess.call(
            'notify-send "Pomodoro Time" "What would you like to do now?"' +
            ' -i {}'.format(icon_path), shell=True
        )

    def play_sound(self):
        mixer.init()
        sound_path = path.join(self.abspath, "sounds/alert2.mp3")
        mixer.music.load(sound_path)
        mixer.music.play()
        # while mixer.music.get_busy() == True:
        #     continue

    def set_tag(self, tag):
        self._tag = tag
        self.tags.add(tag)

    def clock(self, minutes):
        try:
            # Hide terminal cursor
            tmp = subprocess.call("setterm -cursor off", shell=True)

            if minutes == self.t_work:
                message = "\nWorking... \n(Ctrl+c to abort)"
            elif minutes == self.t_break or minutes == self.t_long:
                message = "\nCoffe time... \n(Ctrl+c to abort)"

            finish = time() + minutes * 60
            while(time() < finish):
                tmp = subprocess.call('clear', shell=True)
                seconds = finish - time()
                remaining = gmtime(seconds)
                self.show(strftime("%M:%S", remaining))
                print(message)
                sleep(1)
        except KeyboardInterrupt:
            return -1
        else:
            return 0
        finally:
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
    python3 pomodoro.py -opt <arg>

    -h, --help      Print usage
    -t, --tag       Start with taged cicle
    -s, --style     Select clock's theme (Electronic, Colossal, Shadow)

examples:
    python3 pomodoro.py -h
    python3 pomodoro.py -t develop
    python3 pomodoro.py -s Shadow -t lesson
""")


class AsciiArt:
    def __init__(self, abspath):
        self.abspath = abspath
        self.style = "Colossal"
        self.hight = 0
        self.widths = []

    def _get_template(self):
        ascii_path = path.join(self.abspath, "ascii.txt")
        with open(ascii_path) as ascii_txt:
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
        template = self._get_template()
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
    dirname = path.dirname(argv[0])
    abspath = path.abspath(dirname)
    pomodoro = PomodoroApp(abspath)

    try:
        # Parse terminal arguments
        opts, args = getopt.getopt(argv[1:], "ht:s:",
                                   ["help", "tag=", "style="])
    except GetoptError:
        print("Invalid! Try `pomodoro.py --help' for more information.")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            pomodoro.help()
            sys.exit(0)
        elif opt in ("-t", "--tag"):
            pomodoro.set_tag(arg)
        elif opt in ("-s", "--style"):
            pomodoro.set_theme(arg)

    pomodoro.loop()

if __name__ == '__main__':
    main(sys.argv)
