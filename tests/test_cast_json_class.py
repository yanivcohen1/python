from dataclasses import dataclass, field
from typing import List, Optional

import marshmallow
import marshmallow_dataclass


@dataclass
class Building:
    # field metadata is used to instantiate the marshmallow field
    height: float = field(metadata={"validate": marshmallow.validate.Range(min=0)})
    name: str = field(default="anonymous")


@dataclass
class City:
    name: Optional[str]
    buildings: List[Building] = field(default_factory=list)


CitySchema = marshmallow_dataclass.class_schema(City)

city = CitySchema().load(
    {"name": "Paris", "buildings": [{"name": "Eiffel Tower", "height": 324},{"name": "piza", "height": 424}]}
)
print(city)
# => City(name='Paris', buildings=[Building(height=324.0, name='Eiffel Tower')])

city_dict = CitySchema().dump(city)
# => {'name': 'Paris', 'buildings': [{'name': 'Eiffel Tower', 'height': 324.0}]}
print(city_dict)