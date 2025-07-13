def rev_str(my_str):
    length = len(my_str)
    # reverse the string  range(start_from_end, to 0 include, in step -1)
    for i in range(length - 1, -1, -1):
        yield my_str[i]
        print('after yield')

# For loop to reverse the string
print('-------------------------------')
for char in rev_str("hello"):
    print(char)

# For loop to reverse the string
print('-------------------------------')
gen = rev_str("hello")
for i in range(5):
    char = next(gen)
    print(char)

print('-------------------------------')
def myGenerator(i):
    # i = 1
    def next():
        nonlocal i
        i += 1
        return i
    return next

my_next = myGenerator(1)
while (True):
    n = my_next()
    if (n > 5):
        break
    print(n)

