import keyboard
import pyautogui
import pyperclip
import time
import multiprocessing
import platform

print(platform.python_implementation())

time.sleep(5)  # Задержка начала выполнения в секундах

def manulomyot2054():
    s1 = " манул"
    s2 = " манула"
    s3 = " манулов"
    s4 = " Мануломёт2054 подключается ... "
    s5 = " Цель захвачена "
    s6 = " Открываю огонь манулами на поражение "
    num1 = 1
    num2 = 4
    i = 2792  # Счетчик манулов, можно ввести свое число для начала отсчета

    pyperclip.copy(s4)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)
    pyautogui.press("Enter")
    time.sleep(1)

    pyperclip.copy(s5)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)
    pyautogui.press("Enter")
    time.sleep(1)

    pyperclip.copy(s6)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)
    pyautogui.press("Enter")
    time.sleep(1)

    while True:

        if keyboard.is_pressed('Space'):  # Зажать пробел чтобы прервать цикл
            break

        if i == num1:
            string = str(i) + s1
            pyperclip.copy(string)
            pyautogui.hotkey("ctrl", "v")
            # time.sleep(1)
            pyautogui.press("Enter")
            # time.sleep(1)
            i += 1

        if i <= num2:
            string = str(i) + s2
            pyperclip.copy(string)
            pyautogui.hotkey("ctrl", "v")
            # time.sleep(1)
            pyautogui.press("Enter")
            # time.sleep(1)
            i += 1

        if i > num2:
            string = str(i) + s3
            pyperclip.copy(string)
            pyautogui.hotkey("ctrl", "v")
            # time.sleep(1)
            pyautogui.press("Enter")
            # time.sleep(1)
            i += 1


if __name__ == "__main__":
    p1 = multiprocessing.Process(target=manulomyot2054())
    p2 = multiprocessing.Process(target=manulomyot2054())
    p3 = multiprocessing.Process(target=manulomyot2054())
    p4 = multiprocessing.Process(target=manulomyot2054())

p1.start()
p2.start()
p3.start()
p4.start()

p1.join()
p2.join()
p3.join()
p4.join()
