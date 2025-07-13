from dataclasses import dataclass, field
from typing import List, Optional
import json

import marshmallow
import marshmallow_dataclass

#pip3 install marshmallow-dataclass[enum,union]
@dataclass
class Building:
    # field metadata is used to instantiate the marshmallow field
    height: float = field(metadata={"validate": marshmallow.validate.Range(min=0)})
    name: str = field(default="anonymous")

@dataclass
class City:
    name: Optional[str]
    buildings: List[Building] = field(default_factory=list)# empty list


CitySchema = marshmallow_dataclass.class_schema(City)

city: list[City] = CitySchema(many=True).load(
    [{"name": "Paris", "buildings":[{"name": "Eiffel Tower", "height": 324.1},
                                    {"name": "piza", "height": 424.2}]}]
)
print(city, '\n')
# => City(name='Paris', buildings=[Building(height=324.0, name='Eiffel Tower')])
print("first building Name: " + city[0].buildings[0].name +
      ", and height:", city[0].buildings[0].height, '\n')
# => first building Name:Eiffel Tower
city_dict: list[City] = CitySchema(many=True).dump(city)
# => {'name': 'Paris', 'buildings': [{'name': 'Eiffel Tower', 'height': 324.0}]}
print(city_dict, '\n')
users_json_str: str = json.dumps(city_dict)
print(users_json_str)

city_dict1: list[City] = [City("Paris", [Building(324.1, "Eiffel Tower"), Building(424.2, "piza")]),
                          City("Paris2", [Building(324.2, "Eiffel Tower2"), Building(424.2, "piza2")])]

print("first building Name: " + city_dict1[1].buildings[0].name +
      ", and height:", city_dict1[1].buildings[0].height, '\n' +
      "in city: " + city_dict1[1].name)
