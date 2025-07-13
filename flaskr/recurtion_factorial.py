def factorial_recursive(n):
    # Base case: 1! = 1
    if n == 1:
        return 1

    # Recursive case: n! = n * (n-1)!
    else:
        print(n)
        return n * factorial_recursive(n-1)
n1 = 5
print (f"{n1}! =", factorial_recursive(n1)) # 120
