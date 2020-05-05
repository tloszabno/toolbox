#!/usr/bin/env python3

from threading import Thread
from datetime import datetime
from time import sleep
from os import path
import subprocess
import math
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Notify

session_time_in_sec = 25 * 60
break_time_in_sec = 5 * 60
timer_loop_sleep_interval_in_sec = 1
default_sync_file_path = "/tmp/pomodoro_timer_sync"

sound_file = "/usr/share/sounds/freedesktop/stereo/complete.oga"
icon = './cherrytomato.png'

iso_date_format = '%Y-%m-%dT%H:%M:%S.%f'


STATE_POMODORO = "pomodoro"
STATE_BREAK = "break"
STATE_PAUSE_AFTER_POMODORO = "pause_after_pomodoro"
STATE_PAUSE_AFTER_BREAK = "pause_after_break"


def round_to_five(x):
    return 5 * math.floor(x/5)


def read_last_state():
    try:
        with open(default_sync_file_path, "r") as file:
            content = file.readlines()
            state = content[0].strip()
            start_date = datetime.strptime(
                content[1].strip(), iso_date_format) if len(content) > 1 else None
            return state, start_date
    except Exception as e:
        print(str(e))
        return None, None


def write_next_state(next_state):
    with open(default_sync_file_path, "w") as file:
        file.write(f"{next_state}\n")
        file.write(datetime.now().isoformat())


def get_left_time(state):
    interval_time = session_time_in_sec if state == STATE_POMODORO else break_time_in_sec
    seconds_left = interval_time - \
        (datetime.now() - start_date).total_seconds()
    minutes = int(seconds_left / 60) if seconds_left > 0 else 0
    seconds = round_to_five(int(seconds_left % 60)) if seconds_left > 0 else 0
    return minutes, seconds

def notify(msg):
    Notify.init("Pomodoro")
    Notify.Notification.new("Timer", msg, icon).show()
    subprocess.call(("paplay", sound_file))


state, start_date = read_last_state()
if not state:
    write_next_state(STATE_POMODORO)
if (state == STATE_BREAK or state == STATE_POMODORO) and start_date is None:
    write_next_state(state)

state, start_date = read_last_state()
if state == STATE_POMODORO:
    minutes, seconds = get_left_time(state)
    print(f"{minutes:02d}:{seconds:02d}| iconName=cherrytomato")
    if minutes == 0 and seconds == 0:
        notify("25 minutes of pomorodo finished")
        write_next_state(STATE_PAUSE_AFTER_POMODORO)

if state == STATE_PAUSE_AFTER_POMODORO:
    print("| iconName=flag-yellow")

if state == STATE_BREAK:
    minutes, seconds = get_left_time(state)
    print(f"{minutes:02d}:{seconds:02d}| iconName=flag-green")
    if minutes == 0 and seconds == 0:
        notify("5 minutes of break finished")
        write_next_state(STATE_PAUSE_AFTER_BREAK)

if state == STATE_PAUSE_AFTER_BREAK:
    print("| iconName=flag-red")
