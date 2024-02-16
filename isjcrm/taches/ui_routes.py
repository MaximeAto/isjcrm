
from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required
from isjcrm.candidat.mashmallow import Mashmallow
from isjcrm.users.mashmallow import Mashmallow as Mashmallow2
from isjcrm.taches.mashmallow import MashmallowTask
from isjcrm.candidat.models import Candidat
from sqlalchemy.exc import SQLAlchemyError

from isjcrm.users.models import User
from isjcrm.taches.models import Task

ui_tasks = Blueprint('ui_tasks', __name__)


@ui_tasks.route("/get_all_tasks", methods=['GET'])
def get_all_tasks():
  
  username = current_user.username
  users = User.query.filter().all()
  tasks = Task.query.filter().all()
  task_mashmallow = MashmallowTask(many=True)
  tasks = task_mashmallow.dump(tasks)
  name = current_user.first_name + " " + current_user.last_name
  
  return render_template("tasks/taskspage.html", name = name, users = users, tasks = tasks)
