#  https://pypi.org/project/keyboard/
from time import sleep
# Import the keyboard module
import keyboard

# Define a function that sends a text when a hotkey is pressed
def send_text():
    # Use keyboard.write to type the text
    keyboard.write("Hello, this is a text response")

    sleep(0.5)
    # Use keyboard.press_and_release to press the enter key
    keyboard.press_and_release("enter")

# Use keyboard.add_hotkey to hook a hotkey to the function
# For example, use ctrl+alt+t as the hotkey
keyboard.add_hotkey("ctrl+alt+h", send_text)

# Use keyboard.wait to keep the program running until esc is pressed
keyboard.wait("esc")
