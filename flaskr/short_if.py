# single line if else assignment
a=2
result = a+1 if a > 1 else "is smaller"
print(result) # print 3
print('Alarm is ' + ("ON" if a < 1 else "OFF")) # print off

# single line if else statment
print("a=2") if 1 < a < 3 else print("a!=2") # print a=2

# single line if statment
if a==2: print("pass") # print pass

arry = [1, 2, 3, 4, 5]
# filter items and return multiply by 2
print( [2*item for item in arry if item % 2 == 1] ) # print [2, 6, 10]
print(list(filter(lambda item: item % 2 == 1, arry))) # same with filter print [1, 3, 5]
print([2*item for item in arry]) # print [2, 4, 6, 8, 10]
print(list(zip([1, 2, 3], ['yan', 'tam', 'yar']))) # combine arrays [(1, 'yan'), (2, 'tam'), (3, 'yar')]

from functools import reduce # reduce
print( reduce((lambda x, y: x * y), [1, 2, 3, 4]) ) # print 24 - 1*2*3*4
rom = 'yan' 
print(rom or 'tam') # print 'yan' but if rom = None print 'tam'
print(list(2 * n + y for n in range(10) for y in [4, 2, 1])) # print total 10*3 times (2n + y) n from 0 to 9

# in javascript
# var timeout = settings !== null ? settings.timeout : 1000; // single line if else assignment
# (a==2) ? alert("please give me") : alert("then give me a beer") // single line if else statment
# if (a==2) alert("please give me a lemonade") // single line if statment

# in java
# Object bar = foo.isSelected() ? foo : baz; // single line if else assignment
# (a==2) ? alert("please give") : alert("then give me a beer") // single line if else statment
# if (name == null) name = "N/A"; // single line if statment