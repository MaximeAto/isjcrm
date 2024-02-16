from isjcrm import ma

from isjcrm.candidat.models import Candidat
from isjcrm.taches.models import Task
from isjcrm.notifications.models import Notification


from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class MashmallowTask(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
class MashmallowNotif(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Notification

class Mashmallow(ma.SQLAlchemyAutoSchema):

    tasks = ma.Nested(MashmallowTask, many=True)
    notifications = ma.Nested(MashmallowNotif, many=True)
    class Meta:
        model = Candidat