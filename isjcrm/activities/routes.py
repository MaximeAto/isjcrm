from flask import Blueprint


activities = Blueprint('activities', __name__)

@activities.route("/", methods=['GET'])
def home():
    return 'hello world activities'

@activities.route("/task_is_done/<int:task_id>", methods=['POST'])
def mark_task_as_done(task_id):

    return str(task_id)
    
@activities.route("/create_activity",methods=['POST','GET'])
def create_activity():
    pass

@activities.route("/get_activities_by_member/<int:member_id>", methods=['GET'])
def get_activities_by_member(member_id):
    return str(member_id)

@activities.route("/get_activity_details/<int:activity_id>", methods=['GET'])
def get_activity_details(activity_id):
    return str(activity_id)


@activities.route("/update_activity_details",methods=['POST'])
def update_activity_details():
    pass

@activities.route("/delete_activity/<int:activity_id>", methods=['GET'])
def delete_activity(activity_id):
    return str(activity_id)
