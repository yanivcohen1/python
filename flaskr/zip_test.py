names = ['Alice', 'Bob', 'Charlie']
ages = [24, 30, 29]

combined = zip(names, ages)
print(list(combined))
# [('Alice', 24), ('Bob', 30), ('Charlie', 29)]


# combined = zip(names, ages, ages) # error: different length of list
for name, age in zip(names, ages):
    print(f"{name} is {age} years old.")


# Unzipping
zipped = list(zip(names, ages))
print(zipped)  # [('Alice', 24), ('Bob', 30), ('Charlie', 29)]
print(*zipped)  # form 2d to 1d: ('Alice', 24) ('Bob', 30) ('Charlie', 29)
# Unzipping the list of tuples back into two lists
names_unzip, ages_unzip = zip(*zipped)
print(names_unzip)  # ('Alice', 'Bob', 'Charlie')
print(ages_unzip)   # (24, 30, 29)

#  Zip with Different Lengths
a = [1, 2]
b = [10, 20, 30]
print(list(zip(a, b)))  # [(1, 10), (2, 20)] — stops at shortest
