from flask import Blueprint, jsonify, render_template
from datetime import datetime,timedelta
from isjcrm.users.models import User
from isjcrm.taches.models import Task
from isjcrm import db
from flask import request
from random import randint
from faker import Faker

taches = Blueprint('taches', __name__)

fake = Faker()


################################################################################
#Add 100 tasks

def create_fake_task():
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    task = Task(
        titre=fake.sentence(),
        objective=fake.text(),
        deadline=fake.date_time_between(start_date='now', end_date='+30d'),
        priority=randint(1, 5),
        status=fake.random_element(elements=('Not do', 'Outdate', 'Done')),
        assigned=fake.random_element(elements=('maxato', 'sjohnson','jillmartin','lbass')),
        id_user= fake.random_element(elements=('maxato', 'sjohnson','jillmartin','lbass')),
    )

    db.session.add(task)
    db.session.commit()
    
@taches.route("/hundred_task", methods=["POST"])
def hundred_task():
    for _ in range(100):
        create_fake_task()
    return jsonify(message = "les 100 tasks ont été enregistré")
#################################################################################

@taches.route("/create_task", methods=["POST"])
def create_task():
    objective = request.form.get('objective')
    deadline_str = request.form.get('deadline')
    priority = request.form.get('priority')
    status = request.form.get('status')
    id_user = request.form.get('id_user')
    id_candidat = request.form.get('id_candidat')  

    deadline = datetime.strptime(deadline_str, '%Y-%m-%d') if deadline_str else None
    assigned = request.form.get('assigned')

        # Vérifier si l'utilisateur existe
    user = User.query.get(id_user)
    if user is None:
        return "L'utilisateur avec cet ID n'existe pas. Veuillez fournir un ID d'utilisateur valide."

    # Création de la tâche
    new_task = Task(objective=objective, deadline=deadline, priority=priority, status=status, id_user=id_user, id_candidat=id_candidat, assigned=assigned)
    db.session.add(new_task)
    db.session.commit()
    return "le tache a bien ete creer et programmer."

@taches.route("/get_task/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get(task_id)

    if task:
        # Si la tâche existe, renvoyer les données au format JSON
        task_data = {
            'id': task.id,
            'objective': task.objective,
            'deadline': task.deadline.strftime('%Y-%m-%d') if task.deadline else None,
            'priority': task.priority,
            'status': task.status,
            'assigned': task.assigned,
            'id_user': task.id_user,
            'id_candidat': task.id_candidat
        }
        return jsonify(task_data)
    else:
        # Si la tâche n'existe pas, renvoyer un message d'erreur
        return jsonify({'error': 'id de utilisateur inexistant'}), 404

@taches.route("/update_task/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        # Si la tâche n'existe pas, renvoyer un message d'erreur
        return jsonify({'error': 'cette tache est inexistante'}), 404

    # Mettre à jour les champs de la tâche avec les nouvelles données
    task.objective = request.form.get('objective', task.objective)
    deadline_str = request.form.get('deadline')
    task.deadline = datetime.strptime(deadline_str, '%Y-%m-%d') if deadline_str else None
    task.priority = request.form.get('priority', task.priority)
    task.status = request.form.get('status', task.status)
    task.assigned = request.form.get('assigned', task.assigned)
    task.id_user = request.form.get('id_user', task.id_user)
    task.id_candidat = request.form.get('id_candidat', task.id_candidat)

    # Enregistrer les modifications dans la base de données
    db.session.commit()

    # Renvoyer les nouvelles données de la tâche au format JSON
    task_data = {
        'id': task.id,
        'objective': task.objective,
        'deadline': task.deadline.strftime('%Y-%m-%d') if task.deadline else None,
        'priority': task.priority,
        'status': task.status,
        'assigned': task.assigned,
        'id_user': task.id_user,
        'id_candidat': task.id_candidat
    }

    return jsonify(task_data)

@taches.route("/mark_task_as_done/<int:task_id>", methods=["POST"])
def mark_task_as_done(task_id):
    pass

@taches.route("/get_all_tasks", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()

    # Convertir les objets Task en un format JSONifiable
    tasks_data = []
    for task in tasks:
        task_data = {
            'id': task.id,
            'objective': task.objective,
            'deadline': task.deadline.strftime('%Y-%m-%d') if task.deadline else None,
            'priority': task.priority,
            'status': task.status,
            'assigned': task.assigned,
            'id_user': task.id_user,
            'id_candidat': task.id_candidat
        }
        tasks_data.append(task_data)

    return jsonify(tasks_data)

@taches.route("/get_user_tasks/<int:user_id>", methods=["GET"])
def get_user_tasks(user_id) :
    pass

@taches.route("/get_user_tasks/<int:user_id>", methods=["GET"])
def get_overdue_tasks() :
    pass

@taches.route("/delete_tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)

    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Tache supprimer avec succes'})
    else:
        return jsonify({'error': 'Tache inexistante'}), 404