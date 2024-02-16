from isjcrm import ma
from isjcrm.activities.mashmallow import MashmallowActivity
from isjcrm.taches.models import Task
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class MashmallowTask(ma.SQLAlchemyAutoSchema):
    activities =  ma.Nested(MashmallowActivity, many=True)
    class Meta:
        model = Task