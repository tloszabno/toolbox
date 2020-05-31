#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Script checks for weather info from local network raspberry pi """


import requests
from requests.exceptions import HTTPError


def format_unit(unit):
    if unit == "C":
        return "°C"
    return unit

def find_measurement(json, sensor_name, measurement_name):
    m = list(filter(lambda x: x["measurement_name"] == measurement_name and x["sensor_name"] == sensor_name, json))
    return (m[0]["value"], m[0]["unit"]) if len(m) > 0 else None


def format_measurement(json, sensor_name, measurement_name, full_info=False):
    value, unit = find_measurement(json, sensor_name, measurement_name)
    unit = format_unit(unit)
    if full_info:
        return f"{measurement_name.capitalize()} {sensor_name} {value}{unit}"
    return f"{value}{unit}"


def handle_response(json):
    measurements = json["data"][0]["measurements"]
    temp = format_measurement(measurements, "Outside", "temperature")
    pm10, pm_unit = find_measurement(measurements, "Airly Slomczynskiego", "pm 10")
    pm10 = float(pm10)
    pm10_icon = "user-online" if pm10 < 50 else "user-idle" if pm10 < 100.0 else "user-busy"

    print(f"{temp} | iconName={pm10_icon}")
#    print("---\n")
#    print(format_measurement(measurements, "Outside", "temperature", full_info=True))




def main():
    try:
        response = requests.get("http://192.168.1.102:81/api/measurements/1")
        if response:
            handle_response(response.json())
        else:
            print("-")
    except:
        print("-")


if __name__ == "__main__":
    main()
