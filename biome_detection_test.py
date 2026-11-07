import os               #importhing stuff i might want
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
from PIL import Image


with open(os.path.join(os.path.dirname(__file__), "config.json"), encoding="utf-8") as config_file:
    config = json.load(config_file)    #selects the config file to load the stuff from

BIOME_COLORS = config["biome_colors"]
BIOMES = list(BIOME_COLORS)
settings = config["settings"]         #puts the lists under the names settings

current_biome = "NORMAL"
last_biome = None
equipped_aura = None
last_aura_string = None
biome_randomizer_time = None
strange_controller_time = None
"""Variables from JSON"""
search_word = settings["search_word"]
before_aura = settings["before_aura"]
after_aura = settings["after_aura"]
server_link = settings["server_link"]
biome_webhook_url = settings["biome_webhook_url"]
aura_webhook_url = settings["aura_webhook_url"]
aura_check = settings["aura_check"]
biome_check = settings["biome_check"]
auto_strange_controller = settings["auto_strange_contoller"]
auto_biome_randomizer = settings["auto_biome_randomizer"]
player_username = settings["player_username"]
unix_timestamp = int(time.time())
"""Coordinates"""
inventory_x = 34
inventory_y = 508 # Open inventory button x and y coords
searchbar_x = 819
searchbar_y = 367 # Search bar x and y coords
device_x = 851
device_y = 470 # Device position in inventory x and y coords
amount_x = 574
amount_y = 580 # Amount textbox x and y coords
use_x = 686
use_y = 576 # Use button x and y coords



"""Defining functions"""

#embed for biome start
def get_start_biome_embed():
    unix_timestamp = int(time.time())
    return discord_webhook.DiscordEmbed(
        title=f"{current_biome} has started,",
        description=f"{current_biome} biome has started <t:{unix_timestamp}:R>.",
        color=BIOME_COLORS.get(current_biome, 0x808080),
        url=biome_webhook_url
        )

#embed for biome end
def get_end_biome_embed():
    unix_timestamp = int(time.time())
    return discord_webhook.DiscordEmbed(
        title=f"{last_biome} has ended",
        description=f"The {last_biome} biome has ended <t:{unix_timestamp}:R>.",
        color=BIOME_COLORS.get(last_biome, 0x808080)
        )

#embed for aura equip
def get_aura_embed():
    return discord_webhook.DiscordEmbed(
        title=f"{extracted_aura} has been equipped",
        description=f"The user {player_username} has equipped the aura {extracted_aura}.",
        color=0x00d62b
        )



def get_current_log_file():
    log_dir = os.path.expandvars(r'%localappdata%\Roblox\logs') #locates the log file
    search_pattern = os.path.join(log_dir, "*_Player_*.log")    #sets a search pattern for glob to find the current log file
    log_files = glob.glob(search_pattern)   #glob uses above search pattern to find current log
    if not log_files:
        raise FileNotFoundError("no log found") #if no log is found it raises a warning

    latest_log = max(log_files, key=os.path.getmtime)   
    return latest_log

def biome_change(biome: str):
            """Fixes the last_biome and current_biome variables upon the biome changing.""" #w edo
            global last_biome, current_biome
            last_biome = current_biome
            current_biome = biome
            return last_biome, current_biome

def click_at(x, y):
    pydirectinput.moveTo(x-1, y)
    pydirectinput.moveRel(1, 0)                     #moves 1 pixel so the game registers the cursor, it is accounted for with the x-1
    pydirectinput.click()
    time.sleep(0.1)                                 #waits 10ms to make

def double_click_at(x, y):
    pydirectinput.moveTo(x-1, y)
    pydirectinput.moveRel(1, 0)                     #same as above
    pydirectinput.doubleClick()
    time.sleep(0.1)                                 #same as above

def use_device(k: int):
    """If k is 0, then uses SC. If k is 1, then uses BR."""
    click_at(inventory_x, inventory_y)
    click_at(searchbar_x, searchbar_y)
    if k == 0:
        keyboard.write("strange ")
        keyboard.write("controller")
    elif k == 1:
        keyboard.write("biome ")
        keyboard.write("randomizer")
    click_at(device_x, device_y)
    double_click_at(amount_x, amount_y)
    keyboard.write("1")
    click_at(use_x, use_y)

def set_timers():
    global strange_controller_time
    strange_controller_time = int(time.time())  + 1230  #sets strange controller time to 20m 30s in the future
    biome_randomizer_time = int(time.time()) + 2130     #sets biome randomiser time to 35m 30s in the future

screenWidth, screenHeight = pyautogui.size()
print(screenWidth, screenHeight)

latest_log_file = get_current_log_file()
print(latest_log_file)


with open(latest_log_file, 'r', encoding='utf-8', errors='ignore') as file:
    file.seek(0, os.SEEK_END) #goes to end of file
    print("waiting for stuff to happen...")
    
    while True:
        line = file.readline() 
        
        #rest if no new lines
        if not line:
            time.sleep(0.1)
            continue
        
        #remove hidden formatting
        clean_line = line.strip()

        #check for equipped auras
        if aura_check == True:
            match = re.search(r'Equipped \\"([^"]+)\\"', clean_line)
            if match and match.group(0) != last_aura_string:
                extracted_aura = match.group(1) #get text string
            
                # compare the strings
                print(f"[AURA DETECTED]: {extracted_aura}")
                webhook = discord_webhook.DiscordWebhook(url=aura_webhook_url)
                webhook.add_embed(get_aura_embed())
                response = webhook.execute()
                equipped_aura = extracted_aura #saves text
                last_aura_string = match.group(0) #saves full match string





        
        #compare for biomes
        if biome_check == True:
            for biome in BIOMES:
                if biome in clean_line.upper():
                    if current_biome != biome:
                        if biome != "NORMAL":    #checks if biome is not the last registered biome and is not normal, this is for br and sc changes during biome
                            biome_change(biome)
                            print(f"{last_biome} biome has ended.")
                            print(f"[BIOME DETECTED]:Biome is now {current_biome}!")
                            webhook = discord_webhook.DiscordWebhook(url=biome_webhook_url)
                            webhook.add_embed(get_end_biome_embed())
                            webhook.add_embed(get_start_biome_embed())
                            response = webhook.execute()
                            break

                        elif current_biome == "NORMAL":  #checks if the biome changed to normal which means it ended normally
                            biome_change(biome)
                            print(f"{current_biome} biome has ended.")
                            webhook = discord_webhook.DiscordWebhook(url=biome_webhook_url)
                            webhook.add_embed(get_end_biome_embed())
                            response = webhook.execute()
                            break

                        elif biome != "NORMAL" and current_biome != "NORMAL":  #this checks if the biome is new from normal biome which means it does not need an end biome embed
                            biome_change(biome)
                            print(f"[BIOME DETECTED]:Biome is now {current_biome}!")
                            webhook = discord_webhook.DiscordWebhook(url=biome_webhook_url)
                            webhook.add_embed(get_start_biome_embed())
                            response = webhook.execute()
                            break
                        else: continue