import math
def make_cylinder_volume_func(_radius):
    def volume(_hith):
        return math.pi * _radius * _radius * _hith
    return volume

radius = 10
volume_radius_10 = make_cylinder_volume_func(radius) # input radius of the cylinder
hith = 5
volume = volume_radius_10(hith) # input hith of the cylinder
# print the volume in 2 dig after the point
print(f'Fhe chlinder hith: {hith} and the radius: {radius} = so the volume is:{volume:.2}')
