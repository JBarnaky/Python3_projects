import keyboard
import pyperclip
import pyautogui
import time
import random

manul_tup = ('манул', 'манула', 'манулов')
# manul_tup = ('vfyek', 'vfyekf', 'vfyekjd')
manul_counter = int(input("Автоматический Считатель Манулов Революционный...\nВведите число начало отсчета манулов и нажмите Enter чтобы продолжить: "))
output = f"{manul_counter}  {manul_tup[0]}"

def autoInput(output):

    # pyautogui.hotkey('alt', 'shift')
    # pyautogui.write(output, interval=0.25)
    # pyautogui.hotkey('alt', 'shift')

    for char in output:
        pyperclip.copy(char)
        pyautogui.hotkey('ctrl', 'v', interval=random.uniform(0.01, 0.1))

    pyautogui.press("enter")
    time.sleep(random.uniform(5.0, 6.0))

def asmr(manul_counter, manul_tup):

    for num in range(5, 0, -1):
        print(num)
        time.sleep(1)

    while True:
        if keyboard.is_pressed('space'):  
            input("Нажмите Enter чтобы продолжить...")
            for num in range(5, 0, -1):
                print(num)
                time.sleep(1)
        if keyboard.is_pressed('Esc'):
            break

        manul_str = str(manul_counter)

        if manul_str.endswith(('0', '5', '6', '7', '8', '9', '11', '12', '13', '14')):
            output = f"{manul_counter}  {manul_tup[2]}"
        elif manul_str.endswith('1'):
            output = f"{manul_counter}  {manul_tup[0]}"
        elif '1' < manul_str[-1] <= '4':
            output = f"{manul_counter}  {manul_tup[1]}"
        else:
            output = f"{manul_counter}  {manul_tup[2]}"

        autoInput(output)
        manul_counter += 1

asmr(manul_counter, manul_tup)
