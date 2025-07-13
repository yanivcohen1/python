""" If you are using python 3.6+, you can use:
pip install marshmallow-enum and
pip install marshmallow-dataclass

Its simple and type safe.

You can transform your class in a string-json and vice-versa:
 """
#https://pypi.org/project/marshmallow-dataclass/
# from marshmallow_dataclass import dataclass
import json
from marshmallow import Schema
# from dataclasses import field
# import datetime
from marshmallow_enum import Enum
# add
from dataclasses import dataclass, field
from typing import List, Optional, ClassVar, Type, Any

import marshmallow
import marshmallow_dataclass

#Class definitions:
@dataclass # for serialization
class OrderStatus(Enum):
    CREATED = 'Created'
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    FAILED = 'Failed'

@dataclass
class User:
    """ def __init__(self, name, orderId, productName, quantity, status):
        self.name = name
        self.orderId = orderId
        self.productName = productName
        self.quantity = quantity
        self.status = status """

    name: str
    orderId: int #| float
    productName: Any
    quantity: List[int]
    status: OrderStatus
    # all_status: List[OrderStatus] = field(default_factory=list)
    # Schema: ClassVar[Type[Schema]] = Schema # For the type checker

#From Object to String Json:
UserSchema = marshmallow_dataclass.class_schema(User)

users = []
users.append(User("Danilo",50,"RedBull",[15, 16],OrderStatus.CREATED))
users.append(User("Danilo1",51,"RedBull1",[16, 17],OrderStatus.CONFIRMED))
user_json_str = UserSchema(many=True).dumps(users)
#user_json_str = user_json.data
print(user_json_str + "\n") #print(user,flush=True)

#From String Json to Object:
json_list = []
json_list.append({"name":"Danilo1", "orderId":501, "productName":"RedBull1", "quantity":[151, 153], "status":"CREATED"})
json_list.append({"name":"Danilo2", "orderId":502, "productName":"RedBull2", "quantity":[152, 154], "status":"PENDING"})
#user2, err = User.Schema().loads(json_str)
users_json_str: str = json.dumps(json_list)
json_dict_list = json.loads(users_json_str)
users: List[User] = UserSchema(many=True).loads(users_json_str)
print(users,flush=True)
if users[1].status == OrderStatus.PENDING:
    print('Pending')
# do it dynamicly
if getattr(users[1], "status") == OrderStatus.PENDING:
    print('Pending..')

