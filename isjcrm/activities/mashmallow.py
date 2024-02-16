from isjcrm import ma
from isjcrm.activities.models import Activity
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class MashmallowActivity(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Activity