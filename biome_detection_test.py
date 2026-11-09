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
DO_NOT_SKIP_BIOMES = config["do_not_skip_biomes"]
settings = config["settings"]         #puts the lists under the names settings

with open(os.path.join(os.path.dirname(__file__), "webhooks.json"), encoding="utf-8") as f:
    webhooks = json.load(f)

biome_webhook_url = webhooks["biome_webhook_url"]           #this loads webhook urls and server link from webhooks.json
aura_webhook_url = webhooks["aura_webhook_url"]
server_link = webhooks["server_link"]

current_biome = "START"
last_biome = None
equipped_aura = None
last_aura_string = None
biome_randomizer_time = 0
strange_controller_time = 0
macro_state = 0
is_macro_open = 1       #this will detect if the menu is open, if it is closed it will terminate the macro

"""Variables from JSON"""
search_stuff = config["search_stuff"]
search_word = search_stuff["search_word"]       #sets all my variables from json
before_aura = search_stuff["before_aura"]
after_aura = search_stuff["after_aura"]
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
INVENTORY_OPEN_COORD = (34, 508) # Open inventory button x and y coords
INVENTORY_SEARCHBAR_COORD = (819, 367) # Search bar x and y coords
INVENTORY_FIRST_SLOT_COORD = (851, 470) #Device position in inventory x and y coords
INVENTORY_AMOUNT_COORD = (574, 580) # Amount textbox x and y coords
INVENTORY_USE_COORD = (686, 576) # Use button x and y coords
INVENTORY_CLOSE_COORD = (1524, 233)
INVENTORY_ITEMS_TAB_COORD = (1270, 335)

"""Defining functions"""

#embed for biome start
def get_start_biome_embed():
    unix_timestamp = int(time.time())
    thumbnail_name = f"{current_biome.replace(' ', '')}.png"
    embed = discord_webhook.DiscordEmbed(
        title=f"{current_biome} has started,",
        description=f"{current_biome} biome has started <t:{unix_timestamp}:R>.\n{server_link}",
        color=BIOME_COLORS.get(current_biome, 0x808080),
    )
    embed.set_thumbnail(url=f"attachment://{thumbnail_name}")
    embed.set_footer(text="Adams Macro Nuke")
    return embed

#embed for biome end
def get_end_biome_embed():
    unix_timestamp = int(time.time())
    return discord_webhook.DiscordEmbed(
        title=f"{last_biome} has ended",
        description=f"The {last_biome} biome has ended <t:{unix_timestamp}:R>.",
        color=BIOME_COLORS.get(last_biome, 0x808080)
        )

#embed for aura 1
def get_aura_embed():
    return discord_webhook.DiscordEmbed(
        title=f"{extracted_aura} has been equipped",
        description=f"The user {player_username} has equipped the aura {extracted_aura}.",
        color=0x00d62b
        )

def attach_biome_thumbnail(webhook):
    thumbnail_name = f"{current_biome.replace(' ', '')}.png"
    thumbnail_path = os.path.join(
        os.path.dirname(__file__), "images", thumbnail_name
    )

    with open(thumbnail_path, "rb") as thumbnail_file:
        webhook.add_file(file=thumbnail_file.read(), filename=thumbnail_name)


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

def click_at(x, y):
    pydirectinput.moveTo(x-1, y)
    pydirectinput.moveRel(1, 0)                     #moves 1 pixel so the game registers the cursor, it is accounted for with the x-1
    pydirectinput.click()
    time.sleep(0.1)                                 #waits 10ms to make

def double_click_at(x, y):
    pydirectinput.moveTo(x-1, y)
    pydirectinput.moveRel(1, 0)                     #same as above
    pydirectinput.click()
    time.sleep(0.1)
    pydirectinput.click()
    time.sleep(0.1)                                 #same as above

def use_device(k: int):
    global strange_controller_time
    global biome_randomizer_time
    """If k is 0, then uses SC. If k is 1, then uses BR."""
    click_at(*INVENTORY_OPEN_COORD)
    click_at(*INVENTORY_ITEMS_TAB_COORD)
    click_at(*INVENTORY_SEARCHBAR_COORD)
    if k == 0:
        keyboard.write("strange ")
        time.sleep(0.1)
        keyboard.write("controller")
        strange_controller_time = int(time.time())  + 1230  #sets strange controller time to 20m 30s in the future
    elif k == 1:
        keyboard.write("biome ")
        time.sleep(0.1)
        keyboard.write("randomizer")
        biome_randomizer_time = int(time.time()) + 2130     #sets biome randomiser time to 35m 30s in the future
    click_at(*INVENTORY_FIRST_SLOT_COORD)
    double_click_at(*INVENTORY_AMOUNT_COORD)
    time.sleep(0.1)
    keyboard.write("1")
    click_at(*INVENTORY_USE_COORD)
    time.sleep(0.1)
    click_at(*INVENTORY_CLOSE_COORD)
    time.sleep(0.1)

def anti_afk_action():
    if anti_afk_action_type == 1:
        pyautogui.keyDown('space')
        time.sleep(0.2)
        pyautogui.keyUp('space')
    elif anti_afk_action_type == 2:
        pyautogui.keyDown('w')
        time.sleep(0.1)
        pyautogui.keyUp('w')    
        time.sleep(0.1)
        pyautogui.keyDown('s')
        time.sleep(0.1)
        pyautogui.keyUp('s')
        time.sleep(0.1)
    elif anti_afk_action_type == 3:
        pyautogui.keyDown('o')
        time.sleep(0.1)
        pyautogui.keyUp('o')
        time.sleep(0.1)
        pyautogui.keyDown('i')
        time.sleep(0.1)
        pyautogui.keyUp('i')
        time.sleep(0.1)
    anti_afk_time = int(time.time()) + anti_afk_amount
    time.sleep(0.5)

def change_macro_state():
    global macro_state   
    if macro_state == 1:
        macro_state = 0
        print("macro stopped")
    else:
        macro_state = 1
        print("macro started")



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
                            if biome != current_biome and last_biome != "NORMAL" and last_biome != "START":    #checks if biome is not the last registered biome and is not normal, this is for br and sc changes during biome
                                biome_change(biome)
                                print(f"{last_biome} biome has ended.")
                                print(f"[BIOME DETECTED]:Biome is now {current_biome}!")
                                webhook = discord_webhook.DiscordWebhook(url=biome_webhook_url)
                                webhook.add_embed(get_end_biome_embed())
                                webhook.add_embed(get_start_biome_embed())
                                attach_biome_thumbnail(webhook)
                                response = webhook.execute()
                                break

                            elif current_biome != "NORMAL" and current_biome == "NORMAL":  #checks if the biome changed to normal which means it ended normally
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
                                attach_biome_thumbnail(webhook)
                                response = webhook.execute()
                                break
                            else: continue


            if anti_afk == True and anti_afk_time < int(time.time()):     #putting anti afk here
                anti_afk_action()


            

            if(

                auto_strange_controller == True                         #checks if: strange controller option is on
                and current_biome is not None                           #           the current biome isnt none, this stops no skip biomes getting skipped
                and strange_controller_time < int(time.time())          #           strange controller timer is up
                and not DO_NOT_SKIP_BIOMES.get(current_biome, False) ): #           makes sure you arent in a no skip biome
                use_device(0)
            elif(
                
                auto_biome_randomizer == True                           #exact same as above but for biome randomizer
                and current_biome is not None
                and biome_randomizer_time < int(time.time()) 
                and not DO_NOT_SKIP_BIOMES.get(current_biome, False) ):
                use_device(1)

            elif(
                auto_strange_controller == True                         
                and current_biome is not None                           
                and strange_controller_time < int(time.time())         
                and DO_NOT_SKIP_BIOMES.get(current_biome, True) ):     #if the timer is up but you are in a no skip biome it sets it to 10 seconds in the future
                strange_controller_time = int(time.time()) + 10

            elif(
                auto_biome_randomizer == True                         
                and current_biome is not None                           
                and biome_randomizer_time < int(time.time())         
                and DO_NOT_SKIP_BIOMES.get(current_biome, True) ):      #same as above but for biome randomizer       
                biome_randomizer_time = int(time.time()) + 10
                


            
                
    else: exit  #kills terminal if the menu is closed



