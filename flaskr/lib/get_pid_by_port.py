import psutil

def find_process_by_port(port: int):
    # Loop through all the processes
    for process in psutil.process_iter():
        # Try to get the connections of the process
        try:
            connections = process.connections()
        except psutil.AccessDenied:
            # Skip the process if access is denied
            continue
        # Loop through the connections of the process
        for connection in connections:
            # Check if the connection matches the port number
            if connection.laddr.port == port:
                # Print the name of the process
                print(f"Process name: {process.name()}")
                print(f"Process ID: {process.pid}")
                try:
                    print(f"User name: {process.username()}")
                except:
                    pass
                # ch = input("Wanna Close: (y/n) ")
                # if ch.lower() == 'y':
                #     process = psutil.Process(process.pid) # find process by ID
                #     process.terminate()
                # Exit the loop
                break
        
if __name__ == '__main__':
    # Ask the user to input a port number
    find_process_by_port(int(input("Enter a port number: ")))