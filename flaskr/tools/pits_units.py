import pint
import numpy as np

ureg = pint.UnitRegistry()

# works with scalar
mix_units = 3 * ureg.meter + 4 * ureg.cm
print(mix_units) # 3.04 meter
print(mix_units.units) # meter
print(mix_units.to(ureg.cm)) # 304.0 centimeter
print(mix_units.magnitude) # 3.04

# works with arrays
mix_arry_units = [3, 4] * ureg.meter + [4, 3] * ureg.cm
print(mix_arry_units) # [3.04 4.03] meter
print(np.sum(mix_arry_units)) # 7.07 meter
print(np.mean(mix_arry_units)) # 3.535 meter
print(np.std(mix_arry_units)) # 0.4950000000000001 meter
print(list(mix_arry_units.magnitude)) # [3.04, 4.03]
