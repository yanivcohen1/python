from dataclasses import dataclass
import json
import marshmallow_dataclass  # pip install marshmallow-dataclass


@dataclass
class Cat:
    name: str
    higth: int


@dataclass
class Animal():
    name: str
    numbers: list[int]
    cats: list[Cat]


AnimalSchema = marshmallow_dataclass.class_schema(Animal)

print("creating list[objs] -------------------------------")
animals_list = [Animal("cat1", [24, 25], [Cat("cat1", 1), Cat("cat2", 2)]),
                Animal("cat2", [23, 24], [Cat("cat11", 11), Cat(name ="cat22",higth=22)])]
# print(f"animal obj: {animals_list}")
obj_to_dict2: str = AnimalSchema(many=True).dumps(animals_list)# to string
print(f"animal0 json: {obj_to_dict2}") # string
animals: list[Animal] = AnimalSchema(many=True).loads(obj_to_dict2)# to object
cat00: Cat = animals[0].cats[0]  # this for auto copmlite
print(f"animal1.cat0.name dict: {cat00.name}")
assert cat00.name == "cat1", "animal1.cat0.name error needed to be cat1"
cat10: Cat = animals[1].cats[0]  # this for auto copmlite
print(f"animal-type: {cat10.name}, animal-higth: {cat10.higth}")
assert cat10.name == "cat11", "animal0.cat0.name error needed to be cat11"
assert animals[1].cats[0].higth == 11, "animal0.cat0.higth error needed to be 11"
