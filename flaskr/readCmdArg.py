import sys
print ("This is the name of the script: ", sys.argv[0])
print ("Number of arguments: ", len(sys.argv))
print ("The arguments are: " , str(sys.argv))
print ("The first arguments is: " , str(sys.argv[1]))

# py .\readCmdArg.py y1 y2
# The arguments are:  ['.\\readCmdArg.py', 'y1', 'y2']
# The first arguments is:  y1