import keyboard
import pyautogui
import pyperclip
import time

time.sleep(1)  # Задержка в секундах


def autoinput(string):  # Функция автоввода
    pyperclip.copy(string)
    time.sleep(0.1)  # Задержка ввода, можно менять значение
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.1)  # Задержка ввода, можно менять значение
    pyautogui.press("Enter")
    time.sleep(10)  # Ожидание ввода, можно менять значение


def asmr():
    manul_list = ['манул', 'манула', 'манулов', 'манулы']
    manul_counter = 2293  # Счетчик манулов, можно менять значение

    print("АСМР - Автоматический Считатель Манулов Революционный версии 228 подключается ... ")
    time.sleep(1)  # Задержка
    input("Нажмите Enter чтобы продолжить...")

    for num in range(5):
        print(5 - num)
        time.sleep(1)  # Задержка

    while True:

        if keyboard.is_pressed('Space'):  # Зажать Пробел чтобы приостановить
            input("Нажмите Enter чтобы продолжить...")
            for num in range(5):
                print(5 - num)
                time.sleep(1)

        if str(manul_counter) == str(11):
            string = str(manul_counter) + " " + str(manul_list[2])
            autoinput(string)
            manul_counter += 1

        if str(manul_counter)[-1] == str(1):
            string = str(manul_counter) + " " + str(manul_list[0])
            autoinput(string)
            manul_counter += 1

        if str(manul_counter) == str(12):
            string = str(manul_counter) + " " + str(manul_list[2])
            autoinput(string)
            manul_counter += 1

        if str(manul_counter) == str(13):
            string = str(manul_counter) + " " + str(manul_list[2])
            autoinput(string)
            manul_counter += 1

        if str(manul_counter) == str(14):
            string = str(manul_counter) + " " + str(manul_list[2])
            autoinput(string)
            manul_counter += 1

        elif str(1) < str(manul_counter)[-1] <= str(4):
            string = str(manul_counter) + " " + str(manul_list[1])
            autoinput(string)
            manul_counter += 1

        elif str(manul_counter)[-1] > str(4) or str(manul_counter)[-1] == str(0):
            string = str(manul_counter) + " " + str(manul_list[2])
            autoinput(string)
            manul_counter += 1


asmr()
