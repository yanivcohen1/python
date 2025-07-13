thislist = ["0", "1", "2"]
print(thislist[1:2]) # out: ['1'], start = 1, stop = 2-1=1
print(thislist[1:]) # out ['1', '2'], start = 1, stop = end
print(thislist[:2]) # out ['0', '1'] start = 0, stop = 2-1=1
print(thislist[:-1]) # ['0', '1'] start=0, stop = len-1-1=1
print(thislist[-2:]) # ['1', '2'], start= len-2 , stop= end
print(thislist[:]) # ["0", "1", "2"] print all
print(thislist[-2]) # print 1, two from the last
print(thislist[::2]) # ['0', '2'], print in step of 2
print(thislist[::-1]) # ['2', '1', '0'], print in step of -1, reverse the arry
print(thislist[1::-1]) # ['1', '0'], first reverse then start=1, stop=end
print(thislist[:-2:-1]) # ['2'], first reverse then start=0, stop=len-1-2=0
print(thislist[-2::-1]) # ['0'], first reverse then start=len-1-2=0, stop=end

thislist = ["banana", "cherry", "apple"]
list2 = thislist.copy()
list2.append(2)
print(list2) # ['banana', 'cherry', 'apple', 2]
thislist.insert(len(thislist), "bif") # insert last element
thislist.append("bif1") # insert last element the same as above
thislist.pop(-1) # remove last element
thislist.pop() # remove last element the same as above
thislist.sort()
print(thislist) # ['apple', 'banana', 'cherry']
list2.pop()
thislist.extend(list2) # same as zip
for count, value in enumerate(thislist): print(count, value) # thislist + list2
for i in range(len(thislist)): print(thislist[i])  # thislist + list2
# filter
newlist = [x for x in thislist if "a" in x] # 'a' char in str(x)
print(newlist) # ['apple', 'banana', 'banana', 'apple']
print(newlist[1:-2]) # ['banana'], remove the first and the 2 lasts resoults
newlist.remove("apple")
print(newlist) # ['banana', 'banana', 'apple'] remove the first item he find
# filter
print(list(filter(lambda a: a != 'banana', newlist))) # ['apple'] remove all not only first item
print(newlist.index('banana')) # 0, the first he find
# map
print([i for i, x in enumerate(newlist) if x == "banana"]) # [0, 1] find all not only first item
# reduce
from functools import reduce
print( reduce((lambda x, y: x + y), [1, 2, 3, 4]) ) # print 10 - 1+2+3+4 same as sum[1, 2, 3, 4]
sum1 = 0
for x in [1, 2, 3, 4]: sum1 += x
print(sum1) # print 10 - 1+2+3+4 same as sum[1, 2, 3, 4]
for index, num in enumerate([2, 4, 6]): print('index:', index, ' num:', num) # index: 0  num: 2; index: 1  num: 4

# sort list of dict
lst = [{"id":2, "name": "yan"}, {"id":1, "name": "tam"}]
print(sorted(lst, key=lambda lst_i: lst_i['id']))

# list comprehension
a = [0 if i % 2 == 0 else i * 2 for i in range(6) if i < 4]
print(a)

# 2d list comprehension
c = [[(i+1)*(j+1) for i in range(9) if i % 2 == 0] for j in range(9) if j % 2 == 0]
for a in c:
    print(a)

# print as a matrix with 2 spaces between each number
for a in c:
    for b in a:
        print(b if b>9 else ' ' + str(b), end=' ')
    print()

# zip
names = ['Alice', 'Bob', 'Charlie']
ages = [24, 30, 29]

combined = zip(names, ages)
print(list(combined))
# [('Alice', 24), ('Bob', 30), ('Charlie', 29)]

# unzip
zipped = list(zip(names, ages))
print(zipped)  # [('Alice', 24), ('Bob', 30), ('Charlie', 29)]
print(*zipped)  # from list of 3 to tuples of 3 elements ('Alice', 24) ('Bob', 30) ('Charlie', 29)
# Unzipping the list of tuples back into two lists
unzipped = zip(*zipped) # transpose the list of tuples to list of lists
names_unzip, ages_unzip = unzipped
print("names:",names_unzip, "ages:",ages_unzip)
# names: ('Alice', 'Bob', 'Charlie') ages: (24, 30, 29)


my_list = ['a', 'b', 'c']
for i, value in enumerate(reversed(my_list)):
    print(len(my_list) - 1 - i, value)
    # 2 c
    # 1 b
    # 0 a

# insert to sorted list
from sortedcontainers import SortedList, SortedSet

tree_set = SortedList()
tree_set.add(5)
tree_set.add(2)
tree_set.add(8)
tree_set.add(9)
tree_set.remove(9)
tree_set.add(5)
print("sort list:", tree_set)  # SortedSet([2, 5, 5, 8])

tree_set = SortedSet()
tree_set.add(5)
tree_set.add(2)
tree_set.add(8)
tree_set.add(9)
tree_set.remove(9)
tree_set.add(5) # duplicate ignored
print("sort set:", tree_set)  # SortedSet([2, 5, 8])
