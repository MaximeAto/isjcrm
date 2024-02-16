from isjcrm import ma
from isjcrm.mailmodel.models import Modelemail
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class Mashmallow(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Modelemail