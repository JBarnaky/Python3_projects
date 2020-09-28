import pyautogui, time, pyperclip, keyboard

pyautogui.countdown(5)

fw = pyautogui.getActiveWindow()
print(fw.title)
print(fw.size)
# fw.minimize()

# pyautogui.mouseInfo()

pyautogui.hotkey('winleft', 'r')
time.sleep(1)
pyautogui.write('firefox')
time.sleep(1)
pyautogui.hotkey('enter')
time.sleep(1)
pyautogui.write('https://www.youtube.com/')
time.sleep(1)
pyautogui.hotkey('enter')
time.sleep(5)
pyautogui.press('tab')
time.sleep(0.1)
pyautogui.press('tab')
time.sleep(0.1)
pyautogui.press('tab')
time.sleep(0.1)
pyautogui.press('tab')
time.sleep(0.1)
pyautogui.write('hololive')
time.sleep(1)
pyautogui.hotkey('enter')
time.sleep(3)
im = pyautogui.screenshot(r"scr\screenshot1.png")

try:
    x, y = pyautogui.locateCenterOnScreen('scr\scr1.png', confidence=0.9) #reqired OpenCV
    pyautogui.click(x, y)
    time.sleep(5)
    pyautogui.scroll(-800)

    im1 = pyautogui.screenshot(r"scr\screenshot2.png")

except:
    print("Can`t find the image")

try:
    x, y = pyautogui.locateCenterOnScreen('scr\scr2.png', confidence=0.9) #reqired OpenCV
    pyautogui.click(x, y)
    time.sleep(5)
    pyautogui.scroll(-800)

    im1 = pyautogui.screenshot(r"scr\screenshot2.png")

except:
    print("Can`t find the image")
    
pyautogui.keyDown('alt'); pyautogui.press('f4'); pyautogui.keyUp('alt')
