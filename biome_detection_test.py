import os
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
from PIL import Image


BIOMES = ["NORMAL", "WINDY", "SNOWY", "RAINY", "SANDSTORM", "HELL", "STARFALL", "HEAVEN", "LOST FOREST", "CORRUPTION", "NULL", "GLITCHED", "DREAMSPACE", "CYBERSPACE", "SINGULARITY", "THE RADIANT FOREST", "PUMPKIN MOON", "GRAVEYARD", "BLOOD RAIN"]
BIOME_COLORS = {
    "NORMAL": 0x00d62b,
    "WINDY": 0x00cefc,
    "SNOWY": 0x99e9ff,
    "RAINY": 0x0049d1,
    "SANDSTORM": 0xa18f50,
    "HELL": 0xc90000,
    "STARFALL": 0x6500d9,
    "HEAVEN": 0xfff947,
    "LOST FOREST": 0x056903,
    "CORRUPTION": 0x580775,
    "NULL": 0x696969,
    "GLITCHED": 0xb4eb00,
    "DREAMSPACE": 0xff4fdf,
    "CYBERSPACE": 0x002a6e,
    "SINGULARITY": 0x631010,
    "THE RADIANT FOREST": 0x400485,
    "PUMPKIN MOON": 0xed5700,
    "GRAVEYARD": 0x383838,
    "BLOOD RAIN": 0x820d0d,
}

current_biome = None
last_biome = None
equipped_aura = None
last_aura_string = None
search_word = ("equipped")
before_aura = ('"Equipped \"')
after_aura = ('\"","smallImage')
server_link = ("https://www.roblox.com/share?code=5c16c5596ed6714db52e089c8bb7ae17&type=Server")
biome_webhook_url = "https://discord.com/api/webhooks/1567999438780104824/vz1Y7Hyu9RJpS_-cvs8nPy4EKyszOX64HSA5sAYM0SaPpdYtMvczZPUXTN63_tMHFUot"
aura_webhook_url = "https://discord.com/api/webhooks/1568255027481542736/yDv9zBzz4bYOC-k2ETVq3pj2nJBWCEVdRvexx55ArnFvT4dBtOZJGoaORHx58aCcx8c6"
aura_check = True
biome_check = True
auto_strange_contoller = True
auto_biome_randomizer = True
player_username = "GOGOPO365"
unix_timestamp = int(time.time())





#embed for biome start
def get_start_biome_embed():
    unix_timestamp = int(time.time())
    return discord_webhook.DiscordEmbed(
        title=f"{current_biome} has started,",
        description=f"{current_biome} biome has started <t:{unix_timestamp}:R>.\nServer Link: {server_link}",
        color=BIOME_COLORS.get(current_biome, 0x808080)
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
    log_dir = os.path.expandvars(r'%localappdata%\Roblox\logs')
    search_pattern = os.path.join(log_dir, "*_Player_*.log")
    log_files = glob.glob(search_pattern)
    if not log_files:
        raise FileNotFoundError("no log found")

    latest_log = max(log_files, key=os.path.getmtime)   
    return latest_log

latest_log_file = get_current_log_file()
print(latest_log_file)



with open(latest_log_file, 'r', encoding='utf-8', errors='ignore') as file:
    #goes to end of file
    file.seek(0, os.SEEK_END)
    
    while True:
        line = file.readline()
        
        #rest if no new lines
        if not line:
            time.sleep(0.1)
            continue
        
        #remove hidden formatting
        clean_line = line.strip()

        #check fr equipped auras
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
        for biome in BIOMES:
            if biome in clean_line.upper():
                if biome != "NORMAL" and current_biome != biome:    #checks if biome is not the last registered biome and is not normal, this is for br and sc changes during biome
                    last_biome = current_biome
                    current_biome = biome
                    print(f"{last_biome} biome has ended.")
                    print(f"[BIOME DETECTED]:Biome is now {current_biome}!")
                    webhook = discord_webhook.DiscordWebhook(url=biome_webhook_url)
                    webhook.add_embed(get_end_biome_embed())
                    webhook.add_embed(get_start_biome_embed())
                    response = webhook.execute()
                    break

                elif biome != current_biome and current_biome == "NORMAL":  #checks if the biome changed to normal which means it ended normally
                    last_biome = current_biome
                    current_biome = biome
                    print(f"{current_biome} biome has ended.")
                    webhook = discord_webhook.DiscordWebhook(url=biome_webhook_url)
                    webhook.add_embed(get_end_biome_embed())
                    response = webhook.execute()
                    break

                elif current_biome != biome and biome != "NORMAL" and current_biome != "NORMAL":  #this checks if the biome is new from normal biome which means it does not need an end biome embed
                    last_biome = current_biome
                    current_biome = biome
                    print(f"[BIOME DETECTED]:Biome is now {current_biome}!")
                    webhook = discord_webhook.DiscordWebhook(url=biome_webhook_url)
                    webhook.add_embed(get_start_biome_embed())
                    response = webhook.execute()

                    break
                else: continue






