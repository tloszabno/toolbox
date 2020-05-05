#!/usr/bin/env python3

# 25m -> 5m -> 25m
#


from threading import Thread
from datetime import datetime
from time import sleep
from os import path
import math

session_time_in_sec = 25 * 60
timer_loop_sleep_interval_in_sec = 1
default_sync_file_path = "/tmp/pomodoro_timer_sync"

iso_date_format = '%Y-%m-%dT%H:%M:%S.%f'

def round_to_five(x):
    return 5 * math.floor(x/5)

def read_last_state():
    try:
        with open(default_sync_file_path, "r") as file:
            return datetime.strptime(file.readline(), iso_date_format)
    except:
        return None

if not read_last_state():
    with open(default_sync_file_path, "w") as file:
        file.write(datetime.now().isoformat())


start_date = read_last_state()
seconds_left = session_time_in_sec - (datetime.now() - start_date).total_seconds()

minutes = int(seconds_left / 60) if seconds_left > 0 else 0
seconds = round_to_five(int(seconds_left % 60)) if seconds_left > 0 else 0

print(f"{minutes:02d}:{seconds:02d} | iconName=cherrytomato")
