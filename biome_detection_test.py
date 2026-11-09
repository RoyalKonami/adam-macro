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
from PIL import Image


with open(os.path.join(os.path.dirname(__file__), "config.json"), encoding="utf-8") as config_file:
    config = json.load(config_file)    #selects the config file to load the stuff from

BIOME_COLORS = config["biome_colors"]
BIOMES = list(BIOME_COLORS)
DO_NOT_SKIP_BIOMES = config["do_not_skip_biomes"]
settings = config["settings"]         #puts the lists under the names settings

current_biome = "START"
last_biome = None
equipped_aura = None
last_aura_string = None
biome_randomizer_time = 0
strange_controller_time = 0
macro_state = 0
is_macro_open = 1       #this will detect if the menu is open, if it is closed (if 0) it will terminate the macro

"""Variables from JSON"""
search_stuff = config["search_stuff"]
search_word = search_stuff["search_word"]       #sets all variables from JSON
after_aura = search_stuff["after_aura"]
server_link = settings["server_link"]
biome_webhook_url = settings["biome_webhook_url"]
aura_webhook_url = settings["aura_webhook_url"]
aura_check = settings["aura_check"]
biome_check = settings["biome_check"]
auto_strange_controller = settings["auto_strange_contoller"]
auto_biome_randomizer = settings["auto_biome_randomizer"]
player_username = settings["player_username"]
anti_afk = settings["anti_afk"]
anti_afk_amount = settings["anti_afk_amount"]
anti_afk_action_type = settings["anti_afk_action_type"]
unix_timestamp = int(time.time())
anti_afk_time = int(time.time()) + anti_afk_amount

"""Coordinates"""
inventory_open_coord = (34, 508) # Open inventory button x and y coords
inventory_searchbar_coord = (819, 367) # Search bar x and y coords
inventory_first_slot_coord = (851, 470) #Device position in inventory x and y coords
inventory_amount_coord = (574, 580) # Amount textbox x and y coords
inventory_use_coord = (686, 576) # Use button x and y coords
inventory_close_coord = (1524, 233) # Close button x and y coords



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
    log_files = glob.glob(search_pattern)                       #glob uses above search pattern to find current log
    if not log_files:
        raise FileNotFoundError("no log found")                 #if no log is found it raises a warning
    latest_log = max(log_files, key=os.path.getmtime)
    return latest_log

def biome_change(biome: str):
    """Fixes the last_biome and current_biome variables upon the biome changing.""" #w edo
    global last_biome, current_biome
    last_biome = current_biome
    current_biome = biome
    return last_biome, current_biome


def click_at(x: int, y: int):
    pydirectinput.moveTo(x-1, y)
    pydirectinput.moveRel(1, 0)                     #moves 1 pixel so the game registers the cursor, it is accounted for with the x-1
    pydirectinput.click()
    time.sleep(0.1)                                 #waits 10ms to make

def double_click_at(x: int, y: int):
    pydirectinput.moveTo(x-1, y)
    pydirectinput.moveRel(1, 0)                     #same as above
    for n in range(2):
        pydirectinput.click()
        time.sleep(0.1)

def use_device(k: int):
    """If k is 0, then uses SC. If k is 1, then uses BR."""
    global strange_controller_time
    global biome_randomizer_time
    click_at(*inventory_open_coord)
    click_at(*inventory_searchbar_coord)
    if k == 0:
        keyboard.write("strange ")
        keyboard.write("controller")
        strange_controller_time = int(time.time())  + 1230  #sets strange controller time to 20m 30s in the future
    elif k == 1:
        keyboard.write("biome ")
        keyboard.write("randomizer")
        biome_randomizer_time = int(time.time()) + 2130     #sets biome randomizer time to 35m 30s in the future
    click_at(*inventory_first_slot_coord)
    double_click_at(*inventory_amount_coord)
    keyboard.write("1")
    click_at(*inventory_use_coord)
    click_at(*inventory_close_coord)

def anti_afk_action():
    """Type 1 is jump, Type 2 is move up and down, Type 3 is uhhhh???"""
    if anti_afk_action_type == 1:
        pyautogui.keyDown('space')
        time.sleep(0.2)
        pyautogui.keyUp('space')
    elif anti_afk_action_type == 2:
        keypresses = ['w', 's']
        for k in keypresses:
            pyautogui.keyDown(k)
            time.sleep(0.1)
            pyautogui.keyUp(k)
            time.sleep(0.1)
    elif anti_afk_action_type == 3:
        keypresses = ['o', 'i']
        for k in keypresses:
            pyautogui.keyDown(k)
            time.sleep(0.1)
            pyautogui.keyUp(k)
            time.sleep(0.1)
    anti_afk_time = int(time.time()) + anti_afk_amount
    time.sleep(0.5)

def change_macro_state():
    global macro_state   
    if macro_state == 1:
        macro_state = 0
    else:
        macro_state = 1



keyboard.add_hotkey("j", change_macro_state)


screenWidth, screenHeight = pyautogui.size()
print(screenWidth, screenHeight)

latest_log_file = get_current_log_file()
print(latest_log_file)


with open(latest_log_file, 'r', encoding='utf-8', errors='ignore') as file:
    file.seek(0, os.SEEK_END) #goes to end of file
    print("Time to swap...")
    while is_macro_open == 1:
        if macro_state == 0:
            time.sleep(0.2)  #makes it so that if is_macro_open == 1 and macro_state == 0 the loop doesnt run every tick
        
        while True and macro_state == 1:
            line = file.readline() 
            
            #rest if no new lines
            if not line:
                time.sleep(0.1)
                continue
            
            #remove hidden formatting
            clean_line = line.strip()

            #check for equipped auras
            if aura_check: # "if var == True" is the same as "if var" -e
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
            if biome_check: # "if var == true" is the same as "if var" -e
                for biome in BIOMES:
                    if biome in clean_line.upper(): # i have no idea how this works. -e
                        if current_biome != biome:
                            if last_biome != "NORMAL" and last_biome != "START":    #checks if biome is not the last registered biome and is not normal, this is for br and sc changes during biome
                                biome_change(biome)
                                print(f"{last_biome} biome has ended.")
                                print(f"[BIOME DETECTED]:Biome is now {current_biome}!")
                                webhook = discord_webhook.DiscordWebhook(url=biome_webhook_url)
                                webhook.add_embed(get_end_biome_embed())
                                webhook.add_embed(get_start_biome_embed())
                                response = webhook.execute()
                                break

                            elif current_biome == "NORMAL":  #checks if the biome changed to normal which means it ended normally
                                                             # You had if current_biome != "NORMAL" and if current_biome == "NORMAL" which is always False. I assume you mean if current_biome == "NORMAL" -e
                                                             # This code might look unreachable because current_biome is according to your IDE always initalised to "START" -e
                                biome_change(biome)
                                print(f"{current_biome} biome has ended.")
                                webhook = discord_webhook.DiscordWebhook(url=biome_webhook_url)
                                webhook.add_embed(get_end_biome_embed())
                                response = webhook.execute()
                                break
                            elif current_biome != "NORMAL": #this checks if the biome is new from normal biome which means it does not need an end biome embed
                                                            # current_biome and biome are already different by the if statement at the top. -e
                                                            # This code might look unreachable for same reason above. -e
                                biome_change(biome)
                                print(f"[BIOME DETECTED]:Biome is now {current_biome}!")
                                webhook = discord_webhook.DiscordWebhook(url=biome_webhook_url)
                                webhook.add_embed(get_start_biome_embed())
                                response = webhook.execute()
                                break
                            else: continue


            if anti_afk == True and anti_afk_time < int(time.time()):     #putting anti afk here
                anti_afk_action()


            

            if current_biome is not None:
                if auto_strange_controller and strange_controller_time < int(time.time()): # Fixed it hopefully :D -e
                    if DO_NOT_SKIP_BIOMES.get(current_biome, False):
                        use_device(0)
                    elif DO_NOT_SKIP_BIOMES.get(current_biome, True):
                        strange_controller_time = int(time.time()) + 10
                elif auto_biome_randomizer and biome_randomizer_time < int(time.time()):
                    if DO_NOT_SKIP_BIOMES.get(current_biome, False):
                        use_device(1)
                    elif DO_NOT_SKIP_BIOMES.get(current_biome, True):
                        biome_randomizer_time = int(time.time()) + 10

# else exit is useless, when macro_is_open == 0, the while statements ends on its own. -e
# also, we should put the while macro_is_open loop in a main.py, and leave the biome detection (and auto sc and br) in separate files, even from each other. -e





