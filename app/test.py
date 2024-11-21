from sqlalchemy import Column, Integer, String, ForeignKey, Double
from app import db
from app.model.BookImage import ImageOfBook
from enum import Enum


class Status(Enum):
    LE = 1
    TAN = 2
    PHAT = 3


# print(Status.LE.value.__eq__('1'))

obj1 = {
    'name': 'phat',
    'age': 12
}

obj2 = {
    'width': 120,
    'height': 102
}

obj1.update(obj2)
print(obj1)
print(obj2)
