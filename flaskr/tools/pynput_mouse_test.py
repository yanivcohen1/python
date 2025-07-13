from time import sleep
from pynput import keyboard
from pynput.keyboard import Key, Controller
from pyautogui import press, typewrite #, hotkey
from pynput.mouse import Button
from pynput import mouse
from pynput.mouse import Controller as MController
import pyperclip
from pynput.mouse import Button, Controller

mouse_ctrl = Controller()

# sleep(1)
# Set pointer position
mouse_ctrl.position = (10, 400)
# Move pointer relative to current position
mouse_ctrl.move(2000, -40)

# Press and release
mouse_ctrl.press(Button.left)
mouse_ctrl.release(Button.left)

# Double click; this is different from pressing and releasing
# twice on macOS
mouse_ctrl.click(Button.left, 2)

# Scroll two steps down
mouse_ctrl.scroll(0, 2)

class MyException(Exception): pass

def on_click(x, y, button, pressed):
    print('click', button, pressed, x, y)
    # if button == mouse.Button.left:
    #     raise MyException(button)

def on_move(x, y):
    print('Pointer moved to {0}'.format(
        (x, y)))

def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))

# Collect events until released
with mouse.Listener(
        on_click=on_click,
        on_move=on_move,
        on_scroll=on_scroll) as listener:
    try:
        listener.join()
    except MyException as e:
        print('{0} was clicked'.format(e.args[0]))
