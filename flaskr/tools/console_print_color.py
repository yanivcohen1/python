class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print("this is white")

print(f'''{bcolors.WARNING}Warning: No active frommets remain. Continue?
y/n {bcolors.ENDC}''')

print(f'''{bcolors.FAIL}Error: No active frommets remain.{bcolors.ENDC}''')

print("this is white")
