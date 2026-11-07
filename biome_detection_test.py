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

current_biome = None
last_biome = None
equipped_aura = None
last_aura_string = None
biome_randomizer_time = None
strange_controller_time = None
search_word = settings["search_word"]       #sets all my variables from json
before_aura = settings["before_aura"]
after_aura = settings["after_aura"]
server_link = settings["server_link"]
biome_webhook_url = settings["biome_webhook_url"]
aura_webhook_url = settings["aura_webhook_url"]
aura_check = settings["aura_check"]
biome_check = settings["biome_check"]
auto_strange_contoller = settings["auto_strange_contoller"]
auto_biome_randomizer = settings["auto_biome_randomizer"]
player_username = settings["player_username"]
unix_timestamp = int(time.time())





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
    log_dir = os.path.expandvars(r'%localappdata%\Roblox\logs') #locates tthe log file
    search_pattern = os.path.join(log_dir, "*_Player_*.log")    #sets a search pattern for glob to find the current log file
    log_files = glob.glob(search_pattern)   #glob uses above search pattern to find current log
    if not log_files:
        raise FileNotFoundError("no log found") #if no log is found it raises a warning

    latest_log = max(log_files, key=os.path.getmtime)   
    return latest_log

def biome_change(biome: str):
            """Fixes the last_biome and current_biome variables upon the biome changing.""" #w edo ❤️‍🩹🥹
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

def use_biome_randomizer():
    print("br used")
    click_at(34, 508)        #open inventory
    click_at(819, 367) #search bar
    keyboard.write('biome ')    #types biome randomizer into search
    keyboard.write('randomizer')
    click_at(851, 470) #click biome randomizer
    double_click_at(574, 580)
    keyboard.write('1')     #selects the number and makes sure it is 1
    click_at(686, 576) #use item

def use_strange_controller():
    print("sc used")
    click_at(34, 508)        #open inventory
    click_at(819, 367) #search bar
    keyboard.write('strange ')    #types strange controller into search
    keyboard.write('controller')
    click_at(851, 470) #click strange controller
    double_click_at(574, 580)
    keyboard.write('1')     #selects the number and makes sure it is 1
    click_at(686, 576) #use item

def set_timers():
    global strange_controller_time
    strange_controller_time = int(time.time())  + 20 * 6 + 30   #sets strange controller time to 20m 30s in the future
    biome_randomizer_time = int(time.time()) +  35 * 6 + 30     #same with biome randomizer

     










screenWidth, screenHeight = pyautogui.size()
print(screenWidth, screenHeight)

latest_log_file = get_current_log_file()
print(latest_log_file)



with open(latest_log_file, 'r', encoding='utf-8', errors='ignore') as file:
    #goes to end of file
    file.seek(0, os.SEEK_END)
    print("waiting for stuff to happen...")
    
    while True:
        line = file.readline() 
        
        #rest if no new lines
        if not line:
            time.sleep(0.1)
            continue
        
        #remove hidden formatting
        clean_line = line.strip()

        #check fr equipped auras
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
                    if biome != "NORMAL" and current_biome != biome :    #checks if biome is not the last registered biome and is not normal, this is for br and sc changes during biome
                        biome_change(biome)
                        print(f"{last_biome} biome has ended.")
                        print(f"[BIOME DETECTED]:Biome is now {current_biome}!")
                        webhook = discord_webhook.DiscordWebhook(url=biome_webhook_url)
                        webhook.add_embed(get_end_biome_embed())
                        webhook.add_embed(get_start_biome_embed())
                        response = webhook.execute()
                        break

                    elif biome != current_biome and current_biome == "NORMAL":  #checks if the biome changed to normal which means it ended normally
                        biome_change(biome)
                        print(f"{current_biome} biome has ended.")
                        webhook = discord_webhook.DiscordWebhook(url=biome_webhook_url)
                        webhook.add_embed(get_end_biome_embed())
                        response = webhook.execute()
                        break

                    elif current_biome != biome and biome != "NORMAL" and current_biome != "NORMAL":  #this checks if the biome is new from normal biome which means it does not need an end biome embed
                        biome_change(biome)
                        print(f"[BIOME DETECTED]:Biome is now {current_biome}!")
                        webhook = discord_webhook.DiscordWebhook(url=biome_webhook_url)
                        webhook.add_embed(get_start_biome_embed())
                        response = webhook.execute()
                        break
                    else: continue





