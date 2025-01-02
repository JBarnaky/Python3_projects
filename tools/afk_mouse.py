import pyautogui
import random
import time

def main():
    try:
        while True:
            x = random.randint(600, 700)
            y = random.randint(600, 700)
            pyautogui.moveTo(x, y, 0.5)  # Move to the random position
            time.sleep(random.uniform(2, 4))  # Random wait between 2 and 4 seconds
            
            print(f"Moved mouse to: ({x}, {y})")
            
    except KeyboardInterrupt:
        print("Script terminated by user.")

if __name__ == "__main__":
    main()
