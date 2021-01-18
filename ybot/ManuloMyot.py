import pyautogui
import pyperclip
import time

time.sleep(1)  # Задержка


def autoInput(string):  # Функция автоввода
    pyperclip.copy(string)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)  # Задержка ввода, можно менять значение
    pyautogui.press("Enter")
    time.sleep(1)  # Ожидание ввода, можно менять значение


def manuloMyot228():
    manul_list = ['манул', 'манула', 'манулов', 'манулы']
    manul_counter = 1  # Счетчик манулов, можно менять значение

    print("Призыватель Манулов версии 228 подключается ... ")
    time.sleep(1)  # Задержка
    input("Нажмите Enter чтобы продолжить...")

    for num in range(5):
        print(5 - num)
        time.sleep(1)  # Задержка

    while True:

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
