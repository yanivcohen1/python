
overloading = [
    # Arithmetic
    {'Operator': '+', 'Method': '__add__', 'Example': 'a + b'},
    {'Operator': '-', 'Method': '__sub__', 'Example': 'a - b'},
    {'Operator': '*', 'Method': '__mul__', 'Example': 'a * b'},
    {'Operator': '/', 'Method': '__truediv__', 'Example': 'a / b'},
    {'Operator': '//', 'Method': '__floordiv__', 'Example': 'a // b'},
    {'Operator': '%', 'Method': '__mod__', 'Example': r'a % b'},
    {'Operator': '**', 'Method': '__pow__', 'Example': 'a ** b'},

    # Reverse Arithmetic
    {'Operator': 'r+', 'Method': '__radd__', 'Example': 'b + a'},
    {'Operator': 'r-', 'Method': '__rsub__', 'Example': 'b - a'},
    {'Operator': 'r*', 'Method': '__rmul__', 'Example': 'b * a'},
    {'Operator': 'r/', 'Method': '__rtruediv__', 'Example': 'b / a'},
    {'Operator': 'r//', 'Method': '__rfloordiv__', 'Example': 'b // a'},
    {'Operator': 'r%', 'Method': '__rmod__', 'Example': r'b % a'},
    {'Operator': 'r**', 'Method': '__rpow__', 'Example': 'b ** a'},

    # Bitwise
    {'Operator': '&', 'Method': '__and__', 'Example': 'a & b'},
    {'Operator': '|', 'Method': '__or__', 'Example': 'a | b'},
    {'Operator': '^', 'Method': '__xor__', 'Example': 'a ^ b'},
    {'Operator': '~', 'Method': '__invert__', 'Example': '~a'},
    {'Operator': '<<', 'Method': '__lshift__', 'Example': 'a << b'},
    {'Operator': '>>', 'Method': '__rshift__', 'Example': 'a >> b'},

    # Comparison
    {'Operator': '==', 'Method': '__eq__', 'Example': 'a == b'},
    {'Operator': '!=', 'Method': '__ne__', 'Example': 'a != b'},
    {'Operator': '<', 'Method': '__lt__', 'Example': 'a < b'},
    {'Operator': '<=', 'Method': '__le__', 'Example': 'a <= b'},
    {'Operator': '>', 'Method': '__gt__', 'Example': 'a > b'},
    {'Operator': '>=', 'Method': '__ge__', 'Example': 'a >= b'},

    # Unary
    {'Operator': '-', 'Method': '__neg__', 'Example': '-a'},
    {'Operator': '+', 'Method': '__pos__', 'Example': '+a'},
    {'Operator': 'abs()', 'Method': '__abs__', 'Example': 'abs(a)'},
]

special_methods = [
    {'Action': 'String conversion', 'Method': '__str__', 'Example': 'str(obj)'},
    {'Action': 'Official string', 'Method': '__repr__', 'Example': 'repr(obj)'},
    {'Action': 'Boolean check', 'Method': '__bool__', 'Example': 'bool(obj)'},
    {'Action': 'Hashing', 'Method': '__hash__', 'Example': 'hash(obj)'},
    {'Action': 'Callable object', 'Method': '__call__', 'Example': 'obj()'},

    # Context managers
    {'Action': 'Enter context', 'Method': '__enter__', 'Example': 'with obj:'},
    {'Action': 'Exit context', 'Method': '__exit__', 'Example': 'with obj:'},

    # Containers
    {'Action': 'Length', 'Method': '__len__', 'Example': 'len(obj)'},
    {'Action': 'Indexing', 'Method': '__getitem__', 'Example': 'obj[i]'},
    {'Action': 'Item assignment', 'Method': '__setitem__', 'Example': 'obj[i] = x'},
    {'Action': 'Item deletion', 'Method': '__delitem__', 'Example': 'del obj[i]'},
    {'Action': 'Membership', 'Method': '__contains__', 'Example': 'x in obj'},
    {'Action': 'Iteration', 'Method': '__iter__', 'Example': 'for x in obj'},
    {'Action': 'Next element', 'Method': '__next__', 'Example': 'next(obj)'},

    # Matrix multiplication
    {'Action': 'Matrix multiply', 'Method': '__matmul__', 'Example': 'a @ b'},
]

# example of using the custom operator
# This example demonstrates how to overload the bitwise OR operator (|) to combine two instances of a custom class.
class MyData:
    def __init__(self, value):
        self.value = value

    def __or__(self, other: 'MyData'):
        return MyData(self.value + other.value)

    def __repr__(self):
        return f"MyData is {self.value}"

if __name__ == '__main__':
    data1 = MyData(5)
    data2 = MyData(10)
    data3 = MyData(15)
    result = data1 | data2 | data3  # This will use the overloaded __or__ method
    # result = data1.__or__(data2).__or__(data3)  # Equivalent to the above line
    print(result)  # Output: MyData is 15
