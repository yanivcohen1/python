# https://www.youtube.com/watch?v=MtG9cueB548
import vpython as vp
import numpy as np
import sys

args = sys.argv  # a list of the arguments provided (str)
if len(args) > 1:
    print("running two_digits.py", args)
    # a, b = int(args[1]), int(args[2])
    py_file = args[1]
else:
    py_file = 'flaskr/tools/vpython_lib/3Dpen.npy'

# np.save('3Dpen', np.array([x1,y1,z1,x2,y2,z2]))
x1, y1, z1, x2, y2, z2 = np.load(py_file)
ball1 = vp.sphere(color = vp.color.green, radius = 0.3, make_trail=True, retain=20)
ball2 = vp.sphere(color = vp.color.blue, radius = 0.3, make_trail=True, retain=20)
rod1 = vp.cylinder(pos=vp.vector(0,0,0),axis=vp.vector(0,0,0), radius=0.05) # the stick
rod2 = vp.cylinder(pos=vp.vector(0,0,0),axis=vp.vector(0,0,0), radius=0.05) # the stick
base  = vp.box(pos=vp.vector(0,-4.25,0),axis=vp.vector(1,0,0),
            size=vp.vector(10,0.5,10) ) # the base is the platform
s1 = vp.cylinder(pos=vp.vector(0,-3.99,0),axis=vp.vector(0,-0.1,0), radius=0.8, color=vp.color.gray(luminance=0.7))# shadow
s2 = vp.cylinder(pos=vp.vector(0,-3.99,0),axis=vp.vector(0,-0.1,0), radius=0.8, color=vp.color.gray(luminance=0.7))# shadow

print('Start')
i = 0
while True:
    vp.rate(30)
    i = i + 1
    i = i % len(x1)
    ball1.pos = vp.vector(x1[i], z1[i], y1[i])
    ball2.pos = vp.vector(x2[i], z2[i], y2[i])
    rod1.axis = vp.vector(x1[i], z1[i], y1[i])
    rod2.pos = vp.vector(x1[i], z1[i], y1[i])
    rod2.axis = vp.vector(x2[i]-x1[i], z2[i]-z1[i], y2[i]-y1[i])
    s1.pos = vp.vector(x1[i], -3.99, y1[i])
    s2.pos = vp.vector(x2[i], -3.99, y2[i])
