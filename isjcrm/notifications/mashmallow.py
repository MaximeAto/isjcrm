from isjcrm import ma
from isjcrm.notifications.models import Notification
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class MashmallowNotif(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Notification