class Base:
    pass

class Derive(Base):
    pass

base = Base()
print(type(base))
# <class '__main__.Base'>
derive = Derive()
print(type(derive))
# <class '__main__.Derive'>
print(type(derive) is Derive)
# True
print(type(derive) is Base)
# False
print(isinstance(derive, Derive))
# True
print(isinstance(derive, Base))
# True
print(isinstance(1, int))
# True
print(type(1) is int)
# True
print(isinstance("test", str))
# True
print(type("test") is str)
# True

# test if is scalar or arry
N = [1,"2"]
print(type(N) == list)
# TRUE
N = 2
print(type(N) == int or type(N) == str)
# TRUE
rows, cols = (5, 5)
arry2d = [[0]*cols]*rows
print(type(arry2d) == list)
# TRUE

# test the arry dimention
a = [1, 2, 3, 4]
print(isinstance(a[0], list))
# FALSE
a = [[1,2,3], [4, 5, 6], [7, 8, 9]]
print(isinstance(a[0], list))
# TRUE

def test(a):
    try:
        a[0]
        print("a is a list")
    except:
        print("a is a scalar")
test(1)
# "a is a scalar"
