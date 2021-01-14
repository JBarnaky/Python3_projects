import keyboard
import pyautogui
import pyperclip
import time

time.sleep(1)


def autoInput(string):
    pyperclip.copy(string)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)
    pyautogui.press("Enter")
    time.sleep(1)


def manuloMyot228():
    manul_list = ['манул', 'манула', 'манулов', 'манулы']
    manul_counter = 1

    print("Прототип Призывателя Манулов версии 228 подключается ... ")
    time.sleep(1)
    input("Нажмите Enter чтобы продолжить...")

    for num in range(5):
        print(5 - num)
        time.sleep(1)

    while True:

        if keyboard.is_pressed('Space'):
            input("Нажмите Enter чтобы продолжить...")
            for num in range(5):
                print(5 - num)
                time.sleep(1)

        if str(manul_counter) == str(11):
            string = str(manul_counter) + " " + manul_list[2]
            autoInput(string)
            manul_counter += 1

        if str(manul_counter)[-1] == str(1):
            string = str(manul_counter) + " " + manul_list[0]
            autoInput(string)
            manul_counter += 1

        if str(manul_counter) == str(12):
            string = str(manul_counter) + " " + manul_list[2]
            autoInput(string)
            manul_counter += 1

        if str(manul_counter) == str(13):
            string = str(manul_counter) + " " + manul_list[2]
            autoInput(string)
            manul_counter += 1

        if str(manul_counter) == str(14):
            string = str(manul_counter) + " " + manul_list[2]
            autoInput(string)
            manul_counter += 1

        elif str(1) < str(manul_counter)[-1] <= str(4):
            string = str(manul_counter) + " " + manul_list[1]
            autoInput(string)
            manul_counter += 1

        elif str(manul_counter)[-1] > str(4) or str(manul_counter)[-1] == str(0):
            string = str(manul_counter) + " " + manul_list[2]
            autoInput(string)
            manul_counter += 1


manuloMyot228()
