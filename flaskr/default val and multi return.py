# defoult val
def greet(name="yaniv", msg="Good morning!"):
    print("Hello", name + ', ' + msg)

greet(msg="How are you?")
greet("Bruce", "How do you do?")

# multi return ------------------------------------

def retXY():
    x1=1
    x2=2
    return x1,x2

x1,x2 = retXY()
print(x1)
print(x2)

# nonlocal ------------------------------------

def outer():
    x = "local"

    def inner():
        nonlocal x
        x = "nonlocal"
        print("inner:", x)

    inner()
    print("outer:", x)

outer()