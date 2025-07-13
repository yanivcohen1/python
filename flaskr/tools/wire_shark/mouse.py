import os
import pyshark
import matplotlib.pyplot as plt

def extract_mouse_movements(pcap_file):
    cap = pyshark.FileCapture(pcap_file) # display_filter="usb.capdata"

    x, y = 0, 0
    x_data, y_data = [x], [y]

    for packet in cap:
        try:
            # 0x01: Interrupt transfer -> using wireshark copy -> fildName: usb.transfer_type
            if hasattr(packet, 'usb') and int(packet.usb.transfer_type, 0) == 1:
                # 2.5.1(keybord) 2.6.3(mouse)
                if hasattr(packet, 'DATA'): # and packet.usb.src == "2.6.3":
                    # using wireshark copy -> fildName: usbhid.data
                    hid_data = packet.data.usbhid_data
                    # Convert hex string to integer
                    data_bytes = bytes(int(b, 16) for b in hid_data.split(':'))
                    if len(data_bytes) < 3 : # or len(data_bytes) > 5:
                        raise ValueError("Invalid HID data format")
                    # Extract X and Y movement values (signed 8-bit integers)
                    # Return the integer represented by the given array of bytes
                    left_button = int.from_bytes([data_bytes[0]], byteorder='little', signed=True)
                    dx = int.from_bytes([data_bytes[1]], byteorder='little', signed=True)
                    dy = int.from_bytes([data_bytes[2]], byteorder='little', signed=True)
                    wheel = int.from_bytes([data_bytes[3]], byteorder='little', signed=True)
                    x += dx
                    y -= dy
                    if left_button == 1: # left button pressed
                        x_data.append(x)
                        y_data.append(y)
        except Exception as e:
            print(f"Error processing packet: {e}")

    return x_data, y_data

def plot_mouse_movements(x_data, y_data):
    # y_flipped = np.flip(y_data)
    plt.figure(figsize=(8, 6))
    plt.scatter(x_data, y_data, marker='.', color='b')
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.title("Mouse Movement Path")
    plt.grid()
    plt.show()

def save_position_to_file(x, y, file_path="positions.txt"):
    # Save the current x and y position to a file
    with open(file_path, "a") as f:  # Open file in append mode
        f.write(f"{x},{y}\n")  # Write x, y values to file in CSV format

if __name__ == "__main__":
    # pcap_file = "/mnt/data/mouse.pcap"
    current_directory = os.path.dirname(__file__)
    # pcap_file = current_directory + "/mouse.pcap"
    pcap_file = current_directory + "/mouse_yaniv.pcapng"
    x_data, y_data = extract_mouse_movements(pcap_file)
    # save_position_to_file(x_data, y_data)
    # print(x_data, y_data)
    plot_mouse_movements(x_data, y_data)

# https://www.amazon.com/Wacom-Bamboo-Splash-Tablet-CTL471/dp/B0089VGPII

# Byte Index	Value (Hex)	Meaning
# 0	01	Button state (1 means left button pressed)
# 1	80	X movement (0x80 in signed 8-bit is -128)
# 2	00	Y movement (0x00 in signed 8-bit is 0)
# 3	FD	Wheel movement (0xFD in signed 8-bit is -3)
# Mouse Position Movement:
# X movement: 0x80 (interpreted as -128 in signed 8-bit format)
# Y movement: 0x00 (interpreted as 0)
# Scroll movement: -3 (if relevant)
