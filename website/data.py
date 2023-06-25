from flask import (Blueprint,request,flash,redirect,url_for,
                   jsonify,make_response)
from flask_login import current_user, login_required
from . import db,csrf
from .models import (Comment, Notification, Usr,Department,
                    Assignment,Project, Eval)
from .utils import send_json_response,no_effect
from datetime import datetime,date
import re

data = Blueprint('data', __name__)

@data.route('/membru/interval/', methods=['POST'])
@login_required
def interval():
    if current_user:
        if request.method == "POST":
            data = request.get_json()
            
            today = date.today()
            
            start_date = datetime.strptime(data['startDate'],"%Y-%m-%d").date()
            end_date = datetime.strptime(data['endDate'],"%Y-%m-%d").date()

            if end_date > today:
                return make_response(send_json_response('danger', 'Data maxima nu este corecta', data, label='',error_fields=[('endDate','endDate')]),404)
            elif start_date > today or start_date > end_date:
                return make_response(send_json_response('danger', 'Data minima nu este corecta', data, label='',error_fields=[('startDate','startDate')]),404)     
            
            redirect_url = f"{start_date}/{end_date}/"
            return make_response(send_json_response('succes', 'Interval activ', url=redirect_url),200)
        
        return redirect(url_for('views.not_allowed')) 
    else:
        return redirect(url_for('views.not_allowed')) 



@data.route('/acasa/adauga-proiect/', methods=['POST'])
@login_required
def add_project():
    if current_user.is_manager():
        if request.method == "POST":
            data = request.get_json()                    
            if len(data['name']) > 3:
                if len(data['name']) <= 60:
                    project = Project.query.filter_by(name=data['name'].lower()).first()

                    if project:          
                        return make_response(send_json_response(
                            "error",
                            f"Proiectul {data['name']} exista deja",
                            error_fields=[('name','name')]),   
                        404)
                    else:
                        try:  
                            if project.name == data['name']:
                                return make_response(send_json_response(
                                    "error",
                                    f"Proiectul {data['name']} exista deja",
                                    error_fields=[('name','name')]),   
                                404)
                        except AttributeError:    
                            pass

                    project = Project(name=data['name'])

                    db.session.add(project)

                    try:
                        db.session.commit()
                    except Exception as e:
                        print(e)
                        no_effect(data,message='Proiectul nu a putut fi salvat')

                    return make_response(send_json_response(
                        "success",
                        f"Proiectul {data['name'].title()} a fost inregistrat",
                        data),   
                    200)
                else:
                    return make_response(send_json_response(
                            "error",
                            "Numele proiectului este prea lung (max 60)",
                            error_fields=[('name','name')]),   
                        404)
            else:
                return make_response(send_json_response(
                        "error",
                        "Numele proiectului este prea scurt (min 4)",
                        error_fields=[('name','name')]),   
                    404)
            
        return redirect(url_for('views.home'))
    else:
        return redirect(url_for('views.not_allowed')) 

@data.route('/acasa/adauga-departament/', methods=['POST'])
@login_required
def add_department():
    if current_user.is_manager():
        if request.method == "POST":
            data = request.get_json()
                                    
            if len(data['name']) > 3:
                if len(data['name']) <= 60:
                    department = Department.query.filter_by(name=data['name'].lower()).first()
                                    
                    if department:                        
                        return make_response(send_json_response(
                            "error",
                            f"Departamentul {data['name']} exista deja",
                            error_fields=[('name','name')]),   
                        404)
                    else:                        
                        try:                             
                            if department.name == data['name']:
                                return make_response(send_json_response(
                                    "error",
                                    f"Departamentul {data['name']} exista deja",
                                    error_fields=[('name','name')]),   
                                404)
                        except AttributeError:                            
                            pass

                    department = Department(name=data['name'])
                    db.session.add(department)

                    try:
                        db.session.commit()
                    except Exception as e:
                        print(e)
                        no_effect(data,message='Departamentul nu a putut fi salvat')
                        
                    return make_response(send_json_response(
                        "success",
                        f"Departamentul {data['name'].title()} a fost inregistrat",
                        data),   
                    200)
                else:
                    return make_response(send_json_response(
                            "error",
                            "Numele departamentului este prea lung (max 60)",
                            error_fields=[('name','name')]),   
                        404)
            else:                
                return make_response(send_json_response(
                        "error",
                        "Numele departamentului este prea scurt (min 4)",
                        error_fields=[('name','name')]),   
                    404)
            
        return redirect(url_for('views.home'))
    else:
        return redirect(url_for('views.not_allowed')) 
    
    

@data.route('/adauga-functie/', methods=['POST'])
@login_required
def add_project_assignment():
    if current_user.is_manager():
        if request.method == "POST":
            data = request.get_json()
            project = Project.query.filter_by(id=data['project']).first()            
            
            if len(data['assignment']) > 3:
                if len(data['assignment']) <= 60:
                    assignment = Assignment.query.filter(Assignment.name==data['assignment'].lower(), Assignment.project_id==project.id).first()
                                    
                    if assignment:                        
                        return make_response(send_json_response(
                            "error",
                            f'Functia "{data["assignment"]}" exista deja',
                            error_fields=[('assignment','assignment')]),   
                        404)                    

                    assignment = Assignment(name=data['assignment'],project_id=project.id)
                    
                    db.session.add(assignment)

                    try:
                        db.session.commit()
                    except Exception as e:
                        print(e)
                        no_effect(data,message="Functia nu a fost adaugata")
                        
                    return make_response(send_json_response(
                        "success",
                        f"Functia a fost inregistrata in {project.name.title()}",
                        data),   
                    200)
                else:
                    return make_response(send_json_response(
                            "error",
                            "Numele functiei este prea lung (max 60)",
                            error_fields=[('assignment','assignment')]),   
                        404)
            else:                
                return make_response(send_json_response(
                        "danger",
                        "Numele functiei este prea scurt (min 4)",
                        error_fields=[('assignment','assignment')]),   
                    404)
                
        return redirect(url_for('views.home'))
    else:
        return redirect(url_for('views.not_allowed')) 

@data.route('/adauga-functie/<id>/', methods=['POST'])
@login_required
def add_user_assignment(id):
    if current_user.is_manager():
        if request.method == "POST":
            data = request.get_json()
            
            user = Usr.query.get(id)
            assignment = Assignment.query.get(data['assignment'])
            if assignment not in user.assignments:
                user.assignments.append(assignment)
            
                try:
                    db.session.commit()
                except Exception as e:
                    print(e)
                    no_effect(data,message='Functia nu a fost atribuita')

                return make_response(send_json_response(
                    "success",
                    f"Functia  {data['assignment']} i-a fost atribuita membrului",
                    data),   
                200)
            else:
                return make_response(send_json_response(
                        "danger",
                        "Membrul are deja functia aleasa",
                        error_fields=[('assignment','assignment')]),   
                    200)
    else:
        return redirect(url_for('views.not_allowed')) 

@data.route('/acasa/activeaza-proiect/', methods=['POST'])
@login_required
def activate_project():
    if current_user.is_manager():
        if request.method == "POST":
            data = request.get_json()
            
            project = Project.query.get(data['project'])
            
            project.status = 1
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                no_effect(data,message='Statusul proiectului nu a putut fi schimbat')

            return make_response(send_json_response(
                "success",
                f"Proiectul {project.name.title()} a fost activat",
                data),   
            200)
            
        return redirect(url_for('views.home'))
    else:
        return redirect(url_for('views.not_allowed')) 

@data.route('/acasa/dezactiveaza-proiect/', methods=['POST'])
@login_required
def deactivate_project():
    if current_user.is_manager():
        if request.method == "POST":
            data = request.get_json()
            
            project = Project.query.get(data['project'])
            project.status = 0

            try:
                db.session.commit()
            except Exception as e:
                print(e)
                no_effect(data,message='Statusul proiectului nu a putut fi schimbat')

            return make_response(send_json_response(
                "success",
                f"Proiectul {project.name.title()} a fost dezactivat",
                data),   
            200)
            
        return redirect(url_for('views.home'))
    else:
        return redirect(url_for('views.not_allowed')) 

# get project selection for user
@data.route('lista-angajati/modifica-proiect/<id>/', methods=['POST'])
@login_required
def modify_project(id):
    if current_user.is_manager():
        # project_form = ProjectForm(request.form)
        if request.method == "POST":
            
            data = request.get_json()
            
            if data['project'] != '':
                selected_member = Usr.query.get(id)
                project = Project.query.get(data['project'])
                
                if project in selected_member.projects:
                    return make_response(send_json_response(
                        "error",
                        f"Membrul selectat este deja in proiectul {project.name}",
                        error_fields=[('project',project.name)]),   
                    404)

                try:
                    selected_member.projects.append(project)
                    db.session.add(selected_member)
                    db.session.commit()
                except Exception as e:
                    no_effect(data,message='Schimbarile facute nu au putut fi salvate')
                    print(e)
                    
                return make_response(send_json_response(
                    "success",
                    f"Membrul selectat a fost adaugat in {project.name.title()}",
                    data),   
                200)
            else:
                return make_response(jsonify({
                        "category":"error",
                        "message":"Formularul este incomplet"
                    }), 404)
            
        return redirect(url_for('views.company'))
    else:
        return redirect(url_for('views.not_allowed')) 

@data.route('lista-angajati/modifica-departament/<id>/', methods=['POST'])
@login_required
def modify_department(id):
    if current_user.is_manager():
        if request.method == "POST":            
            data = request.get_json()
            
            if data['department'] != '':
                selected_member = Usr.query.get(id)

                department = Department.query.get(data['department'])
                
                if department.id == selected_member.department_id:
                    return make_response(send_json_response(
                        "error",
                        f"Faceti deja parte din departamentul {department.name}",
                        error_fields=[('department',department.name)]),   
                    404)

                try:
                    selected_member.department_id = department.id
                    db.session.commit()
                except Exception as e:
                    no_effect(data,message='Schimbarile facute nu au putut fi salvate')
                    print(e)
                    
                return make_response(send_json_response(
                    "success",
                    f"Membrul selectat a fost adaugat in {department.name.title()}",
                    data),   
                200)
            else:
                return make_response(jsonify({
                        "category":"error",
                        "message":"Formularul este incomplet"
                    }), 404)
            
        return redirect(url_for('views.company'))
    else:
        return redirect(url_for('views.not_allowed'))                 
    
@data.route('proiect/evaluare/comentariu/<id>/<eval_id>/<string:criteria>', methods=["POST"])
@login_required
def comment(id,eval_id,criteria):
    if request.method == "POST":
        data = request.get_json()
        title = data['title']
        text = data['text']

        if len(title) < 5:
            return make_response(send_json_response(
                    "error",
                    "Titlul este prea scurt (min 5)",
                    error_fields=[('title','title')]),   
                404)

        if len(title) > 35:
            return make_response(send_json_response(
                    "error",
                    "Titlul este prea lung (max 35)",
                    error_fields=[('title','title')]),   
                404)

        if len(text) < 15:
            return make_response(send_json_response(
                    "error",
                    "Comentariul este prea scurt (min 15)",
                    error_fields=[('text','text')]),   
                404)

        if len(text) > 1500:
            return make_response(send_json_response(
                    "error",
                    "Comentariul este prea lung (max 1500)",
                    error_fields=[('text','text')]),   
                404)

        eval = Eval.query.filter_by(id=eval_id).first()
        eval_date = eval.creation_date

        try:
            eval_date = datetime.strftime(*eval_date,"%Y-%m-%d")
        except TypeError:
            
            eval_date = datetime.strftime(eval_date,"%Y-%m-%d")
        
        manager_id = eval.manager_id

        # name,surname = Usr.query.filter_by(id=id).with_entities(Usr.name,Usr.surname).first()

        comment = Comment(title=title,text=text,criteria=criteria,user_id=id,eval_id=eval_id)
        db.session.add(comment)
        
        received_comment = False

        try:
            db.session.commit()
            received_comment = True
        except Exception as e:
            no_effect(data,message='Comentariul nu a putut fi adaugat')
            print(e)
        else:
            return make_response(send_json_response(
                    "success",
                    "Comentariul a fost adăugat cu succes"),
                200)

        if received_comment == True:                        
            text = f'''Aveti un comentariu nou de la {current_user.name.title()} {current_user.surname.title()} la evaluarea din {eval_date}, criteriul: {criteria.title()}'''

            if current_user.is_manager():
                notification = Notification(title=title,text=text,read_status=0,if_comment=1,sender_id=current_user.id,recipient_id=id,eval_id=eval_id)
            else:                
                notification = Notification(title=title,text=text,read_status=0,if_comment=1,sender_id=current_user.id,recipient_id=manager_id,eval_id=eval_id)
            
            db.session.add(notification)

            try:
                db.session.commit()
            except Exception as e:
                print(e)
                
        else:
            return make_response(jsonify({
                "category":"error",
                "message":"A aparut o eroare in adaugarea comentariului"
            }), 404)

@data.route('/marcheaza-ca-citit/<id>/',methods=['POST'])
@login_required
@csrf.exempt
def mark_as_read(id):    
    if request.method == "POST":
        notifications = Notification.query.filter(Notification.recipient_id==id).all()
        
        if notifications:
            for notification in notifications:
                notification.read_status = 1
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                no_effect(message='Schimbarea nu s-a efectuat')

            flash('Schimbarea a fost salvata',category='succes')

        return redirect(request.referrer) 