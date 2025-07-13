def inc1(a):
    return a+1

b = None # not must to define it will cereate it enyway

def inc2(a):
    global b
    b = a + 2

print("eval b = ", eval('inc1(2)')) # run one line and return a value
exec("inc2(2)") # run multilines and not return val
print("exec b = ", b)


var1 = "yaniv"
var1_name = f'{var1=}'.split('=')[0] # extract varible name
print(f'{var1_name} = {var1}')
exec(f"{var1_name} = 'something else'")
print(f'exec:\n  {var1_name} = {var1}')
