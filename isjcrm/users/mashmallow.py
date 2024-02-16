from isjcrm import ma
from isjcrm.users.models import User
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class Mashmallow(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User