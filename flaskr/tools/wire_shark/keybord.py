import os
import pyshark
import matplotlib.pyplot as plt

# usb.src 2.5.1(keybord) 2.7.3(mouse)
# usb.dst host
# usb.transfer_type 0x01
# usbhid.data 00001a0000000000


def parse_hid_data(hid_data):
    """
    Convert HID report data to readable key presses.
    """
    HID_KEYCODES = {
        # Alphabet Keys
        0x04: "A",  # Keyboard a and A
        0x05: "B",  # Keyboard b and B
        0x06: "C",  # Keyboard c and C
        0x07: "D",  # Keyboard d and D
        0x08: "E",  # Keyboard e and E
        0x09: "F",  # Keyboard f and F
        0x0A: "G",  # Keyboard g and G
        0x0B: "H",  # Keyboard h and H
        0x0C: "I",  # Keyboard i and I
        0x0D: "J",  # Keyboard j and J
        0x0E: "K",  # Keyboard k and K
        0x0F: "L",  # Keyboard l and L
        0x10: "M",  # Keyboard m and M
        0x11: "N",  # Keyboard n and N
        0x12: "O",  # Keyboard o and O
        0x13: "P",  # Keyboard p and P
        0x14: "Q",  # Keyboard q and Q
        0x15: "R",  # Keyboard r and R
        0x16: "S",  # Keyboard s and S
        0x17: "T",  # Keyboard t and T
        0x18: "U",  # Keyboard u and U
        0x19: "V",  # Keyboard v and V
        0x1A: "W",  # Keyboard w and W
        0x1B: "X",  # Keyboard x and X
        0x1C: "Y",  # Keyboard y and Y
        0x1D: "Z",  # Keyboard z and Z
        # Number Keys
        0x1E: "1",  # Keyboard 1 and !
        0x1F: "2",  # Keyboard 2 and @
        0x20: "3",  # Keyboard 3 and #
        0x21: "4",  # Keyboard 4 and $
        0x22: "5",  # Keyboard 5 and %
        0x23: "6",  # Keyboard 6 and ^
        0x24: "7",  # Keyboard 7 and &
        0x25: "8",  # Keyboard 8 and *
        0x26: "9",  # Keyboard 9 and (
        0x27: "0",  # Keyboard 0 and )
        # Special Keys
        0x28: "ENTER",  # Keyboard Return (ENTER)
        0x29: "ESC",  # Keyboard ESCAPE
        0x2A: "BACKSPACE",  # Keyboard DELETE (Backspace)
        0x2B: "TAB",  # Keyboard Tab
        0x2C: "SPACE",  # Keyboard Spacebar
        0x2D: "MINUS",  # Keyboard - and _
        0x2E: "EQUAL",  # Keyboard = and +
        0x2F: "LEFTBRACE",  # Keyboard [ and {
        0x30: "RIGHTBRACE",  # Keyboard ] and }
        0x31: "BACKSLASH",  # Keyboard \ and |
        0x33: "SEMICOLON",  # Keyboard ; and :
        0x34: "APOSTROPHE",  # Keyboard ' and "
        0x35: "GRAVE",  # Keyboard ` and ~
        0x36: "COMMA",  # Keyboard , and <
        0x37: "DOT",  # Keyboard . and >
        0x38: "SLASH",  # Keyboard / and ?
        0x39: "CAPSLOCK",  # Keyboard Caps Lock
        # Position Keys
        0x4F: "RIGHT",  # Keyboard Right Arrow
        0x50: "LEFT",  # Keyboard Left Arrow
        0x51: "DOWN",  # Keyboard Down Arrow
        0x52: "UP",  # Keyboard Up Arrow
        # Standard Keys
        # 0x00: "NONE",  # No key pressed
        0x01: "ERR_OVF",  # Keyboard Error Roll Over
        # Function Keys
        0x3A: "F1",  # Keyboard F1
        0x3B: "F2",  # Keyboard F2
        0x3C: "F3",  # Keyboard F3
        0x3D: "F4",  # Keyboard F4
        0x3E: "F5",  # Keyboard F5
        0x3F: "F6",  # Keyboard F6
        0x40: "F7",  # Keyboard F7
        0x41: "F8",  # Keyboard F8
        0x42: "F9",  # Keyboard F9
        0x43: "F10",  # Keyboard F10
        0x44: "F11",  # Keyboard F11
        0x45: "F12",  # Keyboard F12
        # Control Keys
        0xE0: "LEFTCTRL",  # Keyboard Left Control
        0xE1: "LEFTSHIFT",  # Keyboard Left Shift
        0xE2: "LEFTALT",  # Keyboard Left Alt
        0xE3: "LEFTMETA",  # Keyboard Left GUI
        0xE4: "RIGHTCTRL",  # Keyboard Right Control
        0xE5: "RIGHTSHIFT",  # Keyboard Right Shift
        0xE6: "RIGHTALT",  # Keyboard Right Alt
        0xE7: "RIGHTMETA",  # Keyboard Right GUI
        # Modifier Keys
        # 0x01: "MOD_LCTRL",  # Left Control
        # 0x02: "MOD_LSHIFT",  # Left Shift
        # 0x04: "MOD_LALT",  # Left Alt
        # 0x08: "MOD_LMETA",  # Left Meta
        # 0x10: "MOD_RCTRL",  # Right Control
        # 0x20: "MOD_RSHIFT",  # Right Shift
        # 0x40: "MOD_RALT",  # Right Alt
        # 0x80: "MOD_RMETA",  # Right Meta
    }

    keys = []
    for byte in hid_data:
        key_code = int(byte, 16)
        if key_code in HID_KEYCODES:
            keys.append(HID_KEYCODES[key_code])

    return "+".join(keys)  # ctrl+alt+delete


def capture_usb_keyboard(pcap_file):
    cap = pyshark.FileCapture(pcap_file)  # display_filter="usb.capdata"
    keybord = []
    for packet in cap:
        try:
            # 0x01: Interrupt transfer -> using wireshark copy -> fildName: usb.transfer_type
            if hasattr(packet, "usb") and int(packet.usb.transfer_type, 0) == 1:
                # 2.5.1(keybord) 2.7.3(mouse)
                if packet.usb.src == "2.5.1" and hasattr(packet, "DATA"):
                    # using wireshark copy -> fildName: usbhid.data
                    hid_data = packet.data.usbhid_data.split(":")
                    # Convert hex string to integer
                    keys = parse_hid_data(hid_data)
                    if keys:
                        keybord.append(keys)
        except Exception as e:
            print(f"Error processing packet: {e}")

    return keybord


if __name__ == "__main__":
    # pcap_file = "/mnt/data/mouse.pcap"
    current_directory = os.path.dirname(__file__)
    # pcap_file = current_directory + "/mouse.pcap"
    pcap_file = current_directory + "/keybord_yaniv.pcapng"
    print("user write:", capture_usb_keyboard(pcap_file))
