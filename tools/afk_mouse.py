import pyautogui
import random
import time
import argparse

// How to Use the Script: python afk_mouse.py --width 800 --height 600 --min_interval 1.5 --max_interval 3.5
def main():
    parser = argparse.ArgumentParser(description="Move mouse cursor randomly within specified resolution and interval.")
    
    # Resolution parameters
    parser.add_argument('--width', type=int, default=pyautogui.size().width, help='Width of the screen resolution (default: current system default)')
    parser.add_argument('--height', type=int, default=pyautogui.size().height, help='Height of the screen resolution (default: current system default)')
    
    # Interval parameters
    parser.add_argument('--min_interval', type=float, default=2.0, help='Minimum interval between movements in seconds (default: 2.0 seconds)')
    parser.add_argument('--max_interval', type=float, default=4.0, help='Maximum interval between movements in seconds (default: 4.0 seconds)')
    
    args = parser.parse_args()
    
    try:
        while True:
            x = random.randint(0, args.width)
            y = random.randint(0, args.height)
            pyautogui.moveTo(x, y, duration=0.5)  # Move to the random position
            interval = random.uniform(args.min_interval, args.max_interval)  # Random wait between specified intervals
            
            //print(f"Moved mouse to: ({x}, {y})")
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("Script terminated by user.")

if __name__ == "__main__":
    main()
