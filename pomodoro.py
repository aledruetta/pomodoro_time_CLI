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
#           ./pomodoro.py --clear       clear database

import sys
import subprocess
import getopt
import sqlite3 as sql
from getopt import GetoptError
from pygame import mixer
from os import path
from collections import Counter
from time import time, gmtime, strftime, sleep

DATABASE = "database.db"


class PomodoroApp:
    def __init__(self, abspath):
        self.abspath = abspath
        self.tag = ""
        self.tags = self.get_tags()
        self.t_work = 25                    # working time
        self.t_break = self.t_work * 0.2    # 20%
        self.t_long = self.t_work * 0.6     # 60%
        self.ascii_art = AsciiArt(self.abspath)

    def main_loop(self):
        break_count = 0

        while(True):
            status = self.clock(self.t_work)

            if status == 0:
                break_count += 1
                if self.tag:
                    self.tags.update((self.tag,))      # tag +1
                    self.update_db()

            answer = self.ask_user("\nBreak, Work or Exit", "b", "w", "e")
            if answer == "b":       # break
                if break_count < 4:
                    status = self.clock(self.t_break)
                else:
                    status = self.clock(self.t_long)
                    break_count = 0

                answer = self.ask_user("\nWork or Exit", "w", "e")

            if answer == "e":
                sys.exit(0)

            self.summary()

            if self.tag:
                answer = self.ask_user("\nContinue {}".format(
                    self.tag), "y", "n")
                if answer == "n":
                    new_tag = input("Enter a new tag or press Return: ")
                    new_tag = new_tag.strip().lower()
                    if new_tag and (new_tag != self.tag):
                        self.tag = new_tag
            else:
                tag = input("Enter a new tag or press Return: ")
                self.tag = tag.lower().strip()

    def clock(self, minutes):
        try:
            # Hide terminal cursor
            tmp = subprocess.call("setterm -cursor off", shell=True)

            if minutes == self.t_work:
                message = "\nWorking in {}... \n(Ctrl+c to abort)".format(
                    self.tag.upper())
            elif minutes == self.t_break or minutes == self.t_long:
                message = "\nCoffe time... \n(Ctrl+c to abort)"

            finish = time() + minutes * 60
            while(time() < finish):
                tmp = subprocess.call('clear', shell=True)
                seconds = finish - time()
                remaining = gmtime(seconds)     # time tuple
                self.show(strftime("%M:%S", remaining))
                print(message)
                sleep(1)
        except KeyboardInterrupt:       # Ctrl+C
            return -1
        else:
            return 0
        finally:
            # Cursor ON
            tmp = subprocess.call("setterm -cursor on", shell=True)

    def show(self, str_f_time):
        digits = self.ascii_art.get_digits()
        digit_height = self.ascii_art.digit_height
        lcd = ["" for i in range(digit_height)]

        for char in str_f_time:
            for i in range(digit_height):
                lcd[i] += digits[char][i] + " "

        for i in range(digit_height):
            print(lcd[i])

    def ask_user(self, message, *options):
        opts = "/".join(options)
        while True:
            answer = input(message + " (" + opts + ")? ").lower().strip()
            if answer not in opts:
                print("Invalid option!")
            else:
                break
        return answer

    def summary(self):
        if self.tags:
            print()
            for tag, count in self.tags.most_common():
                print("{} \t {}".format(tag, count))

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

    def set_theme(self, theme):
        valid_themes = ("Electronic", "Colossal", "Shadow")
        if theme in valid_themes:
            self.ascii_art.style = theme

    def get_tags(self):
        tags_counter = Counter()
        conn = sql.connect(DATABASE)
        with conn:
            cur = conn.cursor()
            fetch = cur.execute("SELECT * FROM tags").fetchall()
            for tag, count in fetch:
                tags_counter[tag] = count

        return tags_counter

    def update_db(self):
        conn = sql.connect(DATABASE)
        with conn:
            cur = conn.cursor()
            count = self.tags[self.tag]
            cur.execute("INSERT or REPLACE INTO tags VALUES (?, ?)",
                        (self.tag, count))
            conn.commit()

    def clear_db(self):
        answer = self.ask_user("Are you shure", "y", "n")
        if answer == "y":
            subprocess.call(['rm', DATABASE])
            subprocess.check_output("cat schema.sql | sqlite3 {}".format(
                DATABASE), shell=True)

    def help(self):
        print("""
usage:
    python3 pomodoro.py -opt <arg>

    -h, --help      Print usage
    -t, --tag       Start with taged cicle
    -s, --style     Select clock's theme (Electronic, Colossal, Shadow)
        --clear     Clear database

examples:
    python3 pomodoro.py -h
    python3 pomodoro.py -t develop
    python3 pomodoro.py -s Shadow -t lesson
""")


class AsciiArt:
    def __init__(self, abspath):
        self.abspath = abspath
        self.style = "Colossal"
        self.digit_height = 0
        self.widths = []

    def _get_template(self):
        ascii_path = path.join(self.abspath, "ascii.txt")
        with open(ascii_path) as ascii_txt:
            count = 0
            flag = False
            template = []
            for line in ascii_txt:
                if flag and count < self.digit_height:
                    template.append(line.strip("\n"))
                    count += 1

                if self.style in line:
                    settings = line.strip().split(sep=":")
                    self.digit_height = int(settings[1])
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
            for j in range(self.digit_height):
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
                                   ["help", "clear", "tag=", "style="])
    except GetoptError:
        print("Invalid! Try `pomodoro.py --help' for more information.")
        sys.exit(2)
    else:
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                pomodoro.help()
                sys.exit(0)
            elif opt in ("-t", "--tag"):
                pomodoro.tag = arg
            elif opt in ("-s", "--style"):
                pomodoro.set_theme(arg)
            elif opt in ("--clear"):
                pomodoro.clear_db()
                sys.exit(0)

    pomodoro.main_loop()

if __name__ == '__main__':
    main(sys.argv)
