import typing
from marshmallow import fields
from . import BaseSchema
from marshmallow_sqlalchemy  import auto_field
from marshmallow.fields import Date
from marshmallow_sqlalchemy.fields import Nested
from marshmallow_polyfield import PolyField
from marshmallow_oneofschema import OneOfSchema

from store.models.employee import Driver, Manager, Employee

from store.schemas.role_schema import RoleSchema
from store.schemas.phone_schema import PhoneSchema


class ManagerSchema(BaseSchema):
    class Meta:
        model=Manager
        load_instance=True
        dateformat = '%Y-%m-%dT%H:%M:%S'

    id = auto_field()
    name = auto_field()
    department = auto_field()


class DriverSchema(BaseSchema):
    class Meta:
        model=Driver
        load_instance=True
        dateformat = '%Y-%m-%dT%H:%M:%S'

    id = auto_field()
    name = auto_field()
    manager_id = auto_field()


class EmployeeSchema(OneOfSchema):
    type_schemas = {"manager": ManagerSchema, "driver": DriverSchema}

    def get_obj_type(self, obj):
        if isinstance(obj, Driver):
            return "driver"
        elif isinstance(obj, Manager):
            return "manager"
        else:
            raise Exception("Unknown object type: {}".format(obj.__class__.__name__))
    
