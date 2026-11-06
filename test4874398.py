#finding coords


import keyboard
import time
import pyautogui
import pywin32_system32
screenWidth, screenHeight = pyautogui.size()
print(screenWidth, screenHeight)

#pyautogui.moveTo(384, 126, duration=0.5, tween=pyautogui.easeInOutQuad) 

time.sleep(5) #swap application time

currentMouseX, currentMouseY = pyautogui.position()
print(currentMouseX, currentMouseY)

