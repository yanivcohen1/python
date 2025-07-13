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
animals_list = [Animal("cat1", [24, 25], [Cat("cat1", 23), Cat("cat2", 24)]),
                Animal("cat2", [23, 24], [Cat("cat11", 23), Cat(name ="cat22",higth=24)])]
# print(f"animal obj: {animals_list}")
obj_to_dict2: str = AnimalSchema(many=True).dumps(animals_list)# to string
print(f"animal0 json: {obj_to_dict2}") # string
animals: list[Animal] = AnimalSchema(many=True).loads(obj_to_dict2)# to object
print(f"animal0.cat0.name dict: {animals[1].cats[0].name}")
cat: Cat = animals[0].cats[0]  # this for auto copmlite
print(f"animal-type: {cat.name}, animal-higth: {cat.higth}")
