import pyautogui, time, pyperclip, keyboard

time.sleep(5)

while True:
    try:
        f = open("comments.txt", mode = "r", encoding = "utf-8")
                
        if keyboard.is_pressed('q'):
            break
            f.close()
        
        for word in f:
            pyperclip.copy(word)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(1)
            pyautogui.press("Enter")
            time.sleep(65)
            
    except:
        break

    finally:
        f.close()
