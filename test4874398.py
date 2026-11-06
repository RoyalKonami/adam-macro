import json

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


json_data = json.dumps(BIOMES)
print(json_data)