def total(galleons, sickles, knuts):
    return (galleons * 17 + sickles) * 29 + knuts

def total2(*args, **kwargs):
    print("args:", args)
    print("kwargs:", kwargs)

# tuple
coins_tupl = 100, 50, 25
print(total(*coins_tupl), "Knuts")

# *args
coins_lst = [100, 50, 25] # list to tuple
print(total(*coins_lst), "Knuts")

# **kwargs -key:val
coins_dict = {"galleons": 100, "sickles": 50, "knuts": 25}
print(total(**coins_dict), "Knuts")

print("is the same:", total(*coins_lst) == total(**coins_dict))

total2(1,2, a=3, b=4)
