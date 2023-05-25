import keyboard
import pyautogui
import pyperclip
import time

def autoinput(string):
    pyperclip.copy(string)
    time.sleep(0.1) 
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.1)
    pyautogui.press("Enter")
    time.sleep(5)

def asmr():
    manul_tup = ('манул', 'манула', 'манулов', 'манулы')
    manul_counter = 1  

    print("АСМР - Автоматический Считатель Манулов Революционный версии 2754 подключается ... ")  

    input("Нажмите Enter чтобы продолжить...")

    for num in range(5):
        print(5 - num) 

    while True:
        if keyboard.is_pressed('Space'):  
            input("Нажмите Enter чтобы продолжить...")
            for num in range(5):
                print(5 - num)

        manul_str = str(manul_counter)
        manul_len = len(manul_str)

        if manul_str == '11':
            string = f"{manul_counter} {manul_tup[2]}"
        elif manul_str[-1] == '1':
            string = f"{manul_counter} {manul_tup[0]}"
        elif manul_str in {'12', '13', '14'}:
            string = f"{manul_counter} {manul_tup[2]}"
        elif '1' < manul_str[-1] <= '4':
            string = f"{manul_counter} {manul_tup[1]}"
        elif manul_str[-1] > '4' or manul_str[-1] == '0':
            string = f"{manul_counter} {manul_tup[2]}"
        else:
            string = f"{manul_counter} {manul_tup[2]}"

        autoinput(string)
        manul_counter += 1

asmr()
