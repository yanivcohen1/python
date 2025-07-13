from string import ascii_letters, digits, punctuation
from itertools import product
import time

start = time.time()
# repeat=4 => takes 3 sec
# repeat=5 => takes 5 min
# repeat=6 => takes 8 hours
firstDig = ""
cont = 0
for passcode in product (ascii_letters + digits + punctuation, repeat=4):
    if passcode[0] != firstDig:
        firstDig = passcode[0]
        cont += 1
        print(round(cont*100/94, 2), "% ;", round(time.time() - start, 2), "sec")
        # print(passcode)

end = time.time()
print("took:", round(end - start, 2), "sec")
