# filter(key>1) and map(val/10) the result is list: [2.0, 3.0]
dic = {1: 10, 2: 20, 3: 30}
print(dic.get(1, "optional defalt form any type if not exist"))
print(dic.get(5, "optional defalt form any type if not exist"))
print([dic[key] / 10 for key in dic if key > 1])  # [2.0, 3.0]
print({key: dic[key] / 10 for key in dic if key > 1})  # {2: 2.0, 3: 3.0}
firstKey = next(iter(dic))
print(
    "first key is:", firstKey, " first val is:", dic[firstKey]
)  # first key is: 1  first val is: 10

thisdict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964,
    "nest": {"inner": "innerval"},
    "arry": [1, 2, 3],
}
if "brand" in thisdict:
    print("brand: ", thisdict["brand"])
del thisdict["brand"]  # del brand
print("brand deleted: ", not ("brand" in thisdict))
print("numbers of items: ", len(thisdict.items()))
print("first of item: " + list(thisdict.keys())[0] + ": " + list(thisdict.values())[0])
print("the nested items: ", thisdict["nest"]["inner"])
print("the arry secend item: ", thisdict["arry"][1])
# loop by order
for key in thisdict:
    print(key, ":", thisdict[key])
# loop by values
for val in thisdict.values():
    print("val: ", val)
# loop by keys
for key in thisdict.keys():
    print("key: ", key)
# loop by key value
for key, val in thisdict.items():
    print(key, ":", val)

# concatenate dict
dicts = {1: "2"}
dicts |= {3: "4"}
print(dicts)

# concatenate dict in dict
dicts = {1: "2"}
dicts["dict"] = {3: "4"}
print(dicts)

# concatenate tuple
tupl = (1, "2")
tupl += (3, "4")
print(tupl)

# concatenate tuple in tuple
tupl = (1, "2")
tupl = (tupl, 3, "4")
print(tupl)

# concatanet list
lists = [1, "2"]
lists += [3, "4"]
print(lists)

# concatanet list in list
lists = [1, "2"]
lists.extend([3, "4"])
print(lists)


# add index by key
def build_dict(seq, key):
    return dict((d[key], d) for (index, d) in enumerate(seq))


list_to_be_sorted = [
    {"name": "yan1", "val": 1},
    {"name": "yan", "val": 0},
    {"name": "yan2", "val": 2},
]
newlist = build_dict(list_to_be_sorted, "name")
print(newlist)
print(newlist["yan"])  # find in list by key

myDict = {1: "2", 3: "4", 4: "3", 2: "1", 0: "0"}
myKeys = list(myDict.keys())
myKeys.sort()
sorted_dict = {key: myDict[key] for key in myKeys}
print(sorted_dict)

my_dict = {'c': 3, 'a': 1, 'b': 2}
# Sort by keys
tuples = my_dict.items() # [('a', 1), ('b', 2), ('c', 3)]
sorted_by_keys = dict(sorted(tuples, reverse=False)) # from tuples to dict
print("Dict sorted by keys:", sorted_by_keys)

# Sort by values
sorted_by_values = dict(sorted(tuples, key=lambda item: item[1], reverse=False)) # item[1] are the values
print("Dict sorted by values:", sorted_by_values)


from sortedcontainers import SortedDict
sd = SortedDict({"b": 2, "d": -3, "a": 1, "c": 1})  # sort by key
print("sort dict:", sd)  # SortedDict({'a': 1, 'b': 2, 'c': 1, 'd': -3})
print("print from the start:", sd.peekitem(0))  #  from the start ('a', 1)
print("print from the end:", sd.popitem(index=-1))  # from the end ('d', -3)

from collections import OrderedDict
# insert to order dict
od = OrderedDict()
od["c"] = 3
od["b"] = 2
od["a"] = 1
od["d"] = 4
val = od.pop('d', None)
od.move_to_end("b")
print("ordere dict:", od)  # OrderedDict({'c': 3, 'a': 1, 'b': 2})
lst = list(od.keys())
print("print from the start:", lst[0])  # from the start ('a', 1)
print("print from the end:", lst[-1])  # from the End ('d', 2)
print("pop from the start:", od.popitem(last=False))  # from the start ('c', 3)
print("pop from the end:", od.popitem(last=True))  # from the End ('c', 3)


my_dict = {'a': 1, 'b': 2, 'c': 3}
items = list(my_dict.items())
j=0
for (key, value) in reversed(items):
    print(f"{len(items)-1-j}, {key}: {value}")
    j += 1
    # 2, c: 3
    # 1, b: 2
    # 0, a: 1

# Get the 1st element (index 0)
key, value = items[0]
print(f"Index 0 -> {key}: {value}")

# insert in sort order
from sortedcontainers import SortedDict

tree_map = SortedDict()
tree_map['b'] = 2
tree_map['a'] = 1
tree_map['c'] = 3

for k, v in tree_map.items():
    print(k, v)
