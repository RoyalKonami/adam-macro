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

with mss.MSS() as sct:
    monitor = {"top": """top of fish box""", "left": """left of fish box""", "width": """width of fish box""", "height": 1 }    #sets scanning area to be the width of the fish box and 1 pixel high to make it take less cpu than reading the whole box
    output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)
    sct_img = sct.grab(monitor)
    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

    