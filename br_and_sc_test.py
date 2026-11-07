#sc and br test


import keyboard
import time
import pydirectinput
import pyautogui
import pywin32_system32
screenWidth, screenHeight = pyautogui.size()
print(screenWidth, screenHeight)


def click_at(x, y):
    pydirectinput.moveTo(x-1, y)
    pydirectinput.moveRel(1, 0)
    pydirectinput.click()






time.sleep(2) #swap application time


#open inventory
click_at(34, 508)
time.sleep(0.2)



#use strange controller
click_at(819, 367) #search bar
time.sleep(0.1)
keyboard.write('strange ')
keyboard.write('controller')

click_at(851, 470) #strange controller
time.sleep(0.1)
click_at(686, 576) #use item

#use biome rando
click_at(819, 367) #search bar
time.sleep(0.1)
keyboard.write('biome ')
keyboard.write('randomizer')

click_at(851, 470) #biome randomizer
time.sleep(0.1)
click_at(686, 576) #use item