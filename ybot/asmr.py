import keyboard
import pyautogui
import pyperclip
import time

# Задержка в секундах
time.sleep(1)  


def autoinput(string):  
    """
    Функция автоввода
    """
    pyperclip.copy(string)
    time.sleep(0.1) 
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.1) 
    pyautogui.press("Enter")
    time.sleep(10)  


def asmr():
    manul_list = ['манул', 'манула', 'манулов', 'манулы']
    manul_counter = 2293  

    # Подключение АСМР
    print("АСМР - Автоматический Считатель Манулов Революционный версии 2754 подключается ... ")
    time.sleep(1)  

    input("Нажмите Enter чтобы продолжить...")

    for num in range(5):
        print(5 - num)
        time.sleep(1)  

    while True:
        if keyboard.is_pressed('Space'):  
            # Приостановка
            input("Нажмите Enter чтобы продолжить...")
            for num in range(5):
                print(5 - num)
                time.sleep(1)

        # Обновление значения счетчика
        manul_str = str(manul_counter)
        manul_len = len(manul_str)

        if manul_len == 2 and manul_str[1] == '1':
            string = f"{manul_counter} {manul_list[2]}"
        elif manul_str[-1] == '1':
            string = f"{manul_counter} {manul_list[0]}"
        elif manul_str[-1] in {'2', '3', '4'}:
            string = f"{manul_counter} {manul_list[1]}"
        else:
            string = f"{manul_counter} {manul_list[2]}"

        autoinput(string)
        manul_counter += 1


asmr()
