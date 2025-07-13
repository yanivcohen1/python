class Fruits(object):
    count = 0
    def __init__(self, name, count):
        self.name = name
        self.count = count
        Fruits.count = Fruits.count + count

def main():
    apples = Fruits("apples", 3)
    pears = Fruits("pears", 4)
    print (apples.count) # 3
    print (pears.count) # 4
    print (Fruits.count) # 7
    print (apples.__class__.count) # 7, This is Fruit.count
    print (type(pears).count) # 7, So is this

if __name__ == '__main__':
    main()