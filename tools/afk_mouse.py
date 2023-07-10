import pyautogui
import random
import time

while True:
    x = random.randint(600, 700)
    y = random.randint(600, 700)
    pyautogui.moveto(x,y,0.5)
    time.sleep(2)