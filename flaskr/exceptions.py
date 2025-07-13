import sys
import os
import traceback
import random

def fun(ins):
    b = 5
    b/ins
    print('end fun')

try:
    fun(0)
except Exception as ex :
    print("error desc: ", ex)
    print("full error path:")
    traceback.print_exc()

print("********************")

try:
    ser = 5/0
    raise Exception("can't divide by zero")
except Exception as ex:
    print("'exceptions' module: Error (%s)." % str(ex))
    print("********************")
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print("exc_type:",exc_type)
    print("error in file name:",fname)
    print("error in line num:", exc_tb.tb_lineno)
    # for forword the error
    # raise Exception(str(ex))
