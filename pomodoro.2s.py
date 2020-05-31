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
notification_visibility_timeout_in_sec = 5
default_sync_file_path = "/tmp/pomodoro_timer_sync"

sound_file = "/usr/share/sounds/freedesktop/stereo/complete.oga"
icon = './cherrytomato.png'

iso_date_format = '%Y-%m-%dT%H:%M:%S.%f'


STATE_POMODORO = "pomodoro"
STATE_BREAK = "break"


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
    seconds_left = session_time_in_sec - \
        (datetime.now() - start_date).total_seconds()
    minutes = int(seconds_left / 60) if seconds_left > 0 else 0
    seconds = round_to_five(int(seconds_left % 60)) if seconds_left > 0 else 0
    return minutes, seconds

def notify(msg):
    subprocess.call(("paplay", sound_file))
    Notify.init("Pomodoro")
    notif = Notify.Notification.new("Timer", msg)
    notif.show()
    sleep(notification_visibility_timeout_in_sec)
    notif.close()

state, start_date = read_last_state()
if not state:
    write_next_state(STATE_BREAK)
if (state == STATE_BREAK or state == STATE_POMODORO) and start_date is None:
    write_next_state(state)

state, start_date = read_last_state()
if state == STATE_POMODORO:
    minutes, seconds = get_left_time(state)
    print(f"{minutes:02d}:{seconds:02d}| iconName=cherrytomato")
    if minutes == 0 and seconds == 0:
        write_next_state(STATE_BREAK)
        notify("25 minutes of pomodoro finished")

if state == STATE_BREAK:
    print(f"| iconName=cherrytomato")
