from flask import Blueprint


mailmodel = Blueprint('mailmodel', __name__)

@mailmodel.route("/create_model_email", methods=['POST'])    
def create_model_email(model_email_data):
    pass

@mailmodel.route("/get_model_email/<int:model_email_id>", methods=['GET'])    
def get_model_email(model_email_id):
    return str(model_email_id)

@mailmodel.route("/update_model_email", methods=['POST'])    
def update_model_email():
    pass

@mailmodel.route("/delete_model_email/<int:model_email_id>")    
def delete_model_email(model_email_id):
    pass

@mailmodel.route("/get_all_model_emails/<int:user_id>")    
def get_all_model_emails(user_id):
    pass
