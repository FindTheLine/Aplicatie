import re
from flask import Blueprint,render_template,flash,make_response,redirect,request,url_for
from flask_mail import Message
from flask_login import login_user,logout_user,login_required,current_user
from werkzeug.security import generate_password_hash

from .dev_utils import create_departments, create_fake_users, create_roles
from . import db,mail
from .models import Usr, Role, Project,Notification, Assignment
from .utils import no_effect,get_by_roles, send_json_response, get_search_employees, validate_password
from .forms import UserForm,RequestResetForm,SearchForm

auth = Blueprint('auth', __name__)

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    # create_roles()
    # create_departments()
    # create_fake_users(1,"admin",1,1)
    if current_user.is_authenticated:
        return redirect(url_for('views.home', user=current_user))
    if request.method == 'POST':
        email = request.form['email']
        psw = request.form['psw']
        user = Usr.query.filter_by(email=email).first()
        if user:
            if user.verify_psw(psw):
                flash('V-ati logat cu succes', category='succes')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Parola invalida, va rugam reincercati', category='error')    
        else:
            flash('Adresa de email nu este inregistrata', category='error')
        # return render_template('login.html')
    return render_template('login.html')

@auth.route('/adaugare/', methods=["POST", "GET"])
def add():    
    if current_user.is_manager():
        user_form = UserForm()
        form = SearchForm()
        search_employees = get_search_employees()
        new_notifications = Notification.query.filter(Notification.recipient_id==current_user.id, Notification.read_status==False).all()

        department_choices = current_user.department
        project_choices = [project for project in current_user.projects if project.status == 1]
        role_choices = Role.query.order_by(Role.id.desc()).all()

        user_form.department.choices = department_choices
        user_form.project.choices = project_choices
        employees = get_by_roles('member')
        
        if request.method == "POST":
            data = request.get_json()
            if bool(re.search(r'[^a-zA-Z]', data['name'])):
                return make_response(send_json_response('danger', 'Numele trebuie sa contina doar litere', data, label='',error_fields=[('name','name')]),404)
            if bool(re.search(r'[^a-zA-Z]', data['surname'])):
                return make_response(send_json_response('danger', 'Prenumele trebuie sa contina doar litere', data, label='',error_fields=[('surname','surname')]),404)
            
            if len(data['name']) < 3:
                return make_response(send_json_response('danger', 'Numele este prea scurt', data, label='',error_fields=[('name','name')]),404)
            if len(data['surname']) < 3:
                return make_response(send_json_response('danger', 'Prenumele este prea scurt', data, label='',error_fields=[('surname','surname')]),404)

            if len(data['name']) > 30:
                return make_response(send_json_response('danger', 'Numele este prea lung', data, label='',error_fields=[('name','name')]),404)
            if len(data['surname']) > 30:
                return make_response(send_json_response('danger', 'Prenumele este prea lung', data, label='',error_fields=[('surname','surname')]),404)

            if '@' not in data['email']:
                return make_response(send_json_response('danger', 'Email incorect', data, label='',error_fields=[('email','email')]),404)
            if Usr.query.filter_by(email=data['email']).first():
                email = data['email'] # send in separate variable for displaying wrong value
                del data['email'] # empty data dict with valid fields
                data = dict(data)
                return make_response(send_json_response(
                    'danger',
                    'Emailul este deja folosit',
                    data,
                    label='Email',
                    error_fields=[('email', email)]),
                200)

            added_user = Usr(name=data['name'], surname=data['surname'], email=data['email'],_psw=generate_password_hash('admin'),department_id=data['department'])
            role = Role.query.get(data['role'])

            added_user.roles.append(role)
            
            db.session.add(added_user)

            try:
                db.session.commit()
            except Exception as e:
                print(e)
                no_effect(data,message="Utilizatorul nu a putut fi inregistrat, incercati din nou")
            else:
                return make_response(send_json_response(
                    'success', 
                    'Utilizator salvat cu succes',
                    data), 
                200)

        return render_template('add.html', user_form=user_form,form=form,user=current_user, employees=employees, project_choices=project_choices, department_choices=department_choices,role_choices=role_choices,new_notifications=new_notifications,search_employees=search_employees) 
    else:
        return redirect(url_for('views.not_allowed'))

@auth.route('/adaugare/procesare-utilizator/', methods=["POST", "GET"])
@login_required
def add_process():
    if current_user.is_manager():
        return redirect(url_for(add))
    else:
        return redirect(url_for('views.not_allowed'))

@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/profil/utilizator/<id>/', methods=["POST","GET"])
@login_required
def profile(id):
    new_notifications = Notification.query.filter(Notification.recipient_id==current_user.id, Notification.read_status==False).all()

    form = SearchForm()
    search_employees = get_search_employees()
    if current_user.id == int(id):
        if request.method == "POST":
            old_password = request.form['old']
            new_password = request.form['new']
            resub_new_password = request.form['renew']
            if not current_user.verify_psw(old_password):
                flash(message="Parola actuala este gresita", category="error")
            elif old_password == new_password == resub_new_password:
                flash(message="Parola aleasa trebuie sa fie diferita", category="error")
            elif not validate_password(new_password):
                flash('Parola trebuie sa aiba minim 8 caractere, cel putin o cifra si o majuscula', category='error')
            elif new_password != resub_new_password:
                flash(message="Parolele nu corespund", category="error")
            else:
                try:
                    user = Usr.query.get(id)
                    user.psw = new_password
                    db.session.commit()
                    flash(message="Parola a fost schimbata", category="success")
                except Exception as e:
                    print(e)
                    flash(message="A aparut o eroare neprevazuta", category="error")

        return render_template('profile.html', user=current_user,new_notifications=new_notifications,form=form,search_employees=search_employees)
    else:
        return redirect(url_for('views.not_allowed'))

def send_reset_request(user):
    token = user.get_reset_token()
    
    msg = Message('Reseteaza parola',sender='no-reply-gss@outlook.com',recipients=[user.email])
    msg.body = f'''Pentru a iti reseta parola viziteaza acest link:
{url_for('auth.reset_token',token=token, _external=True)},

Daca nu ati facut dvs. cererea, ignorati acest mesaj.'''
    mail.send(msg)

@auth.route("/reseteaza_parola/", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Usr.query.filter_by(email=form.email.data).first()
        
        send_reset_request(user)
        flash('A fost trimis un email cu linkul pentru resetarea parolei', 'info')
        return redirect(url_for('auth.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@auth.route("/reseteaza_parola/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    user = Usr.verify_reset_token(token)
    
    if user is None:
        flash('Tokenul pentru resetarea parolei a expirat', 'warning')
        return redirect(url_for('auth.reset_request'))
    if request.method == 'POST':
        psw = request.form['psw']
        repeat_psw = request.form['psw2']
        
        
        validate_password(psw)
        if not validate_password(psw):
                 
            flash('Parola trebuie sa aiba minim 8 caractere, cel putin o cifra si o majuscula', category='error')
        elif psw == repeat_psw: 
            
                       
            user.psw = psw
            try:
                db.session.commit()
                flash('Parola ta a fost schimbata cu succes!', category='success')
                return redirect(url_for('auth.login'))
            except Exception as e:
                print(e)
                flash(message="A aparut o eroare neprevazuta, parola nu a fost schimbata", category="error")
        else:
                 
            flash('Parolele nu coincid!', category='error')
    return render_template('reset_pass.html', title='Reset Password', token=token)