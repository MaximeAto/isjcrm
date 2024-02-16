from flask import Blueprint


notifications = Blueprint('notifications', __name__)

@notifications.route("/send_email", methods=['POST'])
def send_email():
    pass

@notifications.route("/send_sms")
def send_sms():
    pass

def send_push_notification(user_id: int, message: str):
    pass