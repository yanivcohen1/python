from enum import IntEnum, Enum

class ColorInt(IntEnum):
    RED = 1
    GREEN = 2
    BLUE = 3
    NOT_FOUND = -1

    @classmethod
    def _missing_(cls, value):
        return cls.NOT_FOUND

print(ColorInt.GREEN.name == "GREEN") # True
print(ColorInt.GREEN.value == 2) # True
print(ColorInt(5) == ColorInt.NOT_FOUND) # True
print(ColorInt(5).name == "NOT_FOUND") # True
enum_list = [elmnt.name for elmnt in list(ColorInt)]
print("All names:", enum_list) # prints ['RED', 'GREEN', 'BLUE', 'NOT_FOUND']
enum_list = [elmnt.value for elmnt in list(ColorInt)]
print("All values:", enum_list) # prints [1, 2, 3, -1]
enum_list = list(map(str, ColorInt))

class ColorStr(Enum):
    RED = "1"
    GREEN = "2"
    BLUE = "3"
    NOT_FOUND = "-1"

    @classmethod
    def _missing_(cls, value):
        return cls.NOT_FOUND

print("-----------------ColorStr-------------------")
print(ColorStr.GREEN.name == "GREEN") # True
print(ColorStr.GREEN.value == "2") # True
print(ColorStr("5") == ColorStr.NOT_FOUND) # True
print(ColorStr("5").name == "NOT_FOUND") # True
enum_list = [elmnt.name for elmnt in list(ColorStr)]
print("All names:", enum_list) # prints ['RED', 'GREEN', 'BLUE', 'NOT_FOUND']
enum_list = [elmnt.value for elmnt in list(ColorStr)]
print("All values:", enum_list) # prints ["1", "2", "3", -"1"]
enum_list = list(map(str, ColorStr))
print("All elements:", enum_list)
# prints ['ColorStr.RED', 'ColorStr.GREEN','ColorStr.BLUE', 'ColorStr.NOT_FOUND']
