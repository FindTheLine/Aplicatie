from .dao import TableDAO
from . import mail,datetime
from .models import Eval, Project, Role, Usr
from flask_login import current_user
from flask import jsonify,url_for,make_response
from flask_mail import Message
from sqlalchemy import func
from flask_login import current_user
import inspect
from .statistics import SingleAverages, MultiAverages, averages_items_list
from statistics import mean, median, mode

# order of dict matters, single averages occupy 25-33% with and the multi averages occupy the rest

dao = TableDAO()

def averages_dicts_to_list(criteria,start:str=None,end:str=None,team=False):
    if start and end:
        interval = True
        start_param = datetime.strptime(start, "%Y-%m-%d")
        end_param = datetime.strptime(end, "%Y-%m-%d")
    else:
        interval = False   
        
    pie = SingleAverages()
    line = MultiAverages()
    
    if interval:
        try:            
            pie.set_averages(criteria, start_param, end_param)
            line.set_averages(criteria, start_param, end_param)
        except ValueError:
            pie.set_averages(criteria) 
            line.set_averages(criteria)           

    else:
        pie.set_averages(criteria)  
        line.set_averages(criteria)        
    
    pie.average_func = mean
    line.average_func = mean

    try:
        line_mean = line.get_averages()
        pie_mean = pie.calculate()

        pie.average_func = median
        pie_median = pie.calculate_crit_label_averages(ordered=True)
        
        pie.average_func = mode
        pie_mode = pie.calculate_crit_label_averages(ordered=True)
        
    except ValueError:
        pie.set_averages(criteria) 
        line.set_averages(criteria)    
        
        try:
            line_mean = line.get_averages()
            pie_mean = pie.calculate()

            pie.average_func = median
            pie_median = pie.calculate_crit_label_averages(ordered=True)
            
            pie.average_func = mode
            pie_mode = pie.calculate_crit_label_averages(ordered=True)
        except ValueError:
            return None
    
    return averages_items_list(line_mean,pie_mean,pie_median,pie_mode)


            
def get_required_parameters(Table:object, criteria:dict) -> dict:
    parameters = inspect.signature(Table.__init__).parameters
    required_params = dict([(k,v) for k,v in criteria.items() if k in parameters.keys()])   
    
    return required_params
    
def get_optional_parameters(Table):
    constructor_params = inspect.signature(Table.__init__).parameters
    parameters = {key:value for key,value in constructor_params.items()
                if not key.startswith(('average', 'crit_'))}
    del parameters['self']
    
    return parameters

# fast count for query items
def get_count(q):
    count_q = q.statement.with_only_columns([func.count()]).order_by(None)
    count = q.session.execute(count_q).scalar()
    return count

def no_effect(data='',message='Nu s-a putut efectua schimbarea'):
    return make_response(send_json_response(
        "error",
        message,
        data),   
    404)

def get_search_employees():
    users = list()
    for project in current_user.projects:
        if project.status==1:
            for user in project.users:
                if user != current_user:
                    users.append(user)
    return set(users)

def send_json_response(category:str,message:str,data={},label='',error_fields=[],url=""):
    error_fields_dict = dict(error_fields)
    # create response dict 
    response = {
        "category":category,
        "message":message,
        "data":data,
        "label":label,
        "error_fields":error_fields_dict,
        "url":url
    }
    return jsonify(response)

def validate_password(pwd):
    conds = [
        lambda s: any(x.isupper() for x in s),
        lambda s: any(x.islower() for x in s),
        lambda s: any(x.isdigit() for x in s),
        lambda s: len(s) >= 8
    ]
    return all(cond(pwd) for cond in conds)

def assign_id():
    return len(Usr.query.all())+1

def get_by_project(id, eliminate=None):
    project = Project.query.get(id)
    employees = [employee for employee in project.users if not employee.is_manager()]
 
    if eliminate:
        try:
            employees.remove(eliminate)
        except ValueError:
            pass
    return employees

def get_by_roles(name:str):
    role = Role.query.filter_by(name=name).first()
    if name == 'manager':
        employees = [employee for employee in role.users if role.id==1]
    elif name == 'member':
        employees = [employee for employee in role.users if role.id==2]
    return employees

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''Ca sa iti resetezi parola acceseaza acest link::
{url_for('auth.reset_token', token=token, _external=True)}
Daca nu ai facut tu cererea de resetare a parolei, te rugam sa ignori acest mesaj.
'''
    mail.send(msg)

