#!/usr/bin/env python3
from datetime import datetime

default_sync_file_path = "/tmp/pomodoro_timer_sync"


STATE_POMODORO = "pomodoro"
STATE_BREAK = "break"

def read_last_state():
    try:
        with open(default_sync_file_path, "r") as file:
            content = file.readlines()
            state = content[0].strip()
            return state
    except Exception as e:
        print(str(e))
        return None


def write_next_state(next_state):
    with open(default_sync_file_path, "w") as file:
        file.write(f"{next_state}\n")
        file.write(datetime.now().isoformat())

state = read_last_state()

if state is None:
    write_next_state(STATE_POMODORO)

if state == STATE_POMODORO:
    write_next_state(STATE_BREAK)

if state == STATE_BREAK:
    write_next_state(STATE_POMODORO)
