import keyboard
import pyautogui
import pyperclip
import time
import multiprocessing

time.sleep(5)  # Задержка начала выполнения в секундах


def manulomyot():
    s1 = " манул"
    s2 = " манула"
    s3 = " манулов"
    num1 = 10
    num2 = 1
    num3 = 4
    i = 1  # Счетчик манулов, можно ввести свое число для начала отсчета

    while True:

        if keyboard.is_pressed('Space'):  # Зажать пробел чтобы прервать цикл
            break

        elif i == num2:
            string = str(i) + s1
            pyperclip.copy(string)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(1)
            pyautogui.press("Enter")
            time.sleep(1)
            i += 1

        elif i <= num3:
            string = str(i) + s2
            pyperclip.copy(string)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(1)
            pyautogui.press("Enter")
            time.sleep(1)
            i += 1

        elif i // num1 == 0:
            num1 += 10
            num2 += 10
            num3 += 10

        elif i <= 999_999_999_999_999_999:
            string = str(i) + s3
            pyperclip.copy(string)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(1)
            pyautogui.press("Enter")
            time.sleep(1)
            i += 1


if __name__ == "__main__":
    p1 = multiprocessing.Process(target=manulomyot())
    p2 = multiprocessing.Process(target=manulomyot())

p1.start()
p2.start()

p1.join()
p2.join()
