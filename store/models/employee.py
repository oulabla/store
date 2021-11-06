import datetime
from sqlalchemy import Column, String, Integer, DateTime, Table
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from . import BaseModel



class Employee(BaseModel):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    type = Column(String(64))

    __mapper_args__  = {
        'polymorphic_identity': 'employee',
        'polymorphic_on': type
    }


class Manager(Employee):
    __tablename__ = "managers"
    id = Column(Integer, ForeignKey('employees.id'), primary_key=True)
    department = Column(String(32), default="default")

    __mapper_args__ = {
        'polymorphic_identity': 'manager',
    }

class Driver(Employee):
    __tablename__ = "drivers"
    id = Column(Integer, ForeignKey('employees.id'), primary_key=True)
    manager_id = Column(Integer, ForeignKey('managers.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'driver',
    }