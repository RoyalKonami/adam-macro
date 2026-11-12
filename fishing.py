import mss
import mss.tools
import os               #importing stuff i might want
import time
import json
import webbrowser
import glob
import psutil
import discord_webhook
import configparser
import customtkinter
import logging
import sys
import ctypes
import re
import pydirectinput
import pyautogui
import keyboard


location = 0        #0 is spawn, 1 is flarg, 2 is fishing spot
fishing_state = 0   #0 is nothing, 1 is fish button is onscreen, 2 is exit fising button is onscreen
collection_open = (31, 451)
collection_exit = (384, 126)
flarg_sell_open = (959, 942)
flarg_first_fish = (829, 411)
flarg_sell_all = (665, 802)
flarg_confirm_sell = (794, 621)
flarg_exit = (1459, 261)
monitor = {"top": 770, "left": 758, "width": 403, "height": 1}          #this sets the fishing area to be monitored, its 1 pixel high to reduce lag
fish_pixel_coord = (849, 836)
fish_pixel_rgb_ref = (120, 140, 255)
exit_fishing_pixel_rgb_ref = (255, 117, 117)           #these are reference colour values for checking against the testing pixel
fishing_bar_rgb = (0, 0, 0)
testing_pixel_rgb = (0, 0, 0)





def kill_loop():
    exit

def get_pixels():
    with mss.MSS() as sct:
        while True:
            rgb = sct.grab(monitor).rgb        #check for a similar color at any scanned pixel
            target = (fishing_bar_rgb)
            tolerance = 25
            found = any(
                all(abs(rgb[i + channel] - target[channel]) <= tolerance
                    for channel in range(3))
                for i in range(0, len(rgb), 3)
                )
                                            
            if found:
                print("Color found")

            time.sleep(0.1) 

def sample_pixel(x, y):
    with mss.MSS() as sct:
        pixel = sct.grab({"left": x, "top": y, "width": 1, "height": 1})
        return tuple(pixel.rgb)
    



def click_at(x: int, y: int):
    pydirectinput.moveTo(x-1, y)
    pydirectinput.moveRel(1, 0)                     #moves 1 pixel so the game registers the cursor, it is accounted for with the x-1
    pydirectinput.click()
    time.sleep(0.1)              

def double_click_at(x: int, y: int):
    pydirectinput.moveTo(x-1, y)
    pydirectinput.moveRel(1, 0)                     #same as above
    for n in range(2):
        pydirectinput.click()
        time.sleep(0.1)

def orient_camera():
    click_at(*collection_open)
    time.sleep(0.1)
    click_at(*collection_exit)
    time.sleep(0.1)

def reset_character():
    global location
    pydirectinput.press("esc")
    pydirectinput.press("r")
    pydirectinput.press("enter")
    time.sleep(1.5)
    location = 0

def walk_to_flarg():
    global location
    if location != 0:
        reset_character()
    pydirectinput.keyDown("w")
    time.sleep(1)
    pydirectinput.keyDown("a")
    time.sleep(6)
    pydirectinput.keyUp("w")
    pydirectinput.keyUp("a")
    time.sleep(0.1)
    pydirectinput.keyDown("d")
    time.sleep(0.01)
    pydirectinput.keyUp("d")
    time.sleep(0.2)
    pydirectinput.keyDown("space")
    time.sleep(0.1)
    pydirectinput.keyUp("space")
    pydirectinput.keyDown("w")
    time.sleep(0.1)
    pydirectinput.keyDown("space")
    time.sleep(0.2)
    pydirectinput.keyUp("space")
    time.sleep(0.1)
    pydirectinput.keyDown("space")
    time.sleep(0.2)
    pydirectinput.keyUp("space")
    pydirectinput.keyUp("w")

def walk_to_fishing_spot(k):
    global location
    if k == 0:
        walk_to_flarg()
        location = 1
        walk_to_fishing_spot(location)
    if k == 1:
        pydirectinput.keyDown("a")
        time.sleep(1)
        pydirectinput.keyUp("a")
        pydirectinput.keyDown("w")
        time.sleep(2.5)
        pydirectinput.keyUp("w")
        location = 2

def sell_to_flarg(loops):
    pydirectinput.press("e")
    time.sleep(0.1)
    click_at(flarg_sell_open)
    time.sleep(0.1)
    for _ in range (loops):
        click_at(*flarg_first_fish)
        click_at(*flarg_sell_all)
        click_at(*flarg_confirm_sell)

def check_fishing_state():
    testing_pixel_rgb = sample_pixel(*fish_pixel_coord)
    if testing_pixel_rgb == fish_pixel_rgb_ref:
        fishing_state = 1
    
    elif testing_pixel_rgb == exit_fishing_pixel_rgb_ref:
        fishing_state = 2
    print(f"Fishing state is {fishing_state}")
    time.sleep(1)

keyboard.add_hotkey("k", kill_loop)



    