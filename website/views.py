from flask import (Blueprint,render_template,request,flash,redirect,url_for,
                    session,jsonify,make_response,abort,render_template_string,Response)
from flask_login import current_user, login_required
from sqlalchemy import  or_
from . import db
from .models import (Comment, Notification, Usr,Department,
                    Project, Eval
)
from .statistics import SingleAverages
from .utils import (averages_dicts_to_list, get_by_project, get_by_roles,send_json_response,no_effect,get_search_employees)
from .forms import SearchForm, ProjectForm, CommentForm
import re
from datetime import datetime,date
from dateutil import relativedelta
from operator import attrgetter


views = Blueprint('views', __name__)

@views.route('/pagina-inaccesibila')
@login_required
def not_allowed():
    abort(Response('Pagina este restrictionata'))

@views.route('/')
@views.route('/acasa/')
@views.route('/<start>/<end>')
@views.route('/acasa/<start>/<end>')
@login_required
def home(start:str=None,end:str=None):
    if not current_user and not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    active_projects = [project for project in sorted(current_user.projects, key=attrgetter('id')) if project.status == 1]
    inactive_projects = [project for project in sorted(current_user.projects, key=attrgetter('id')) if project.status == 0]
    
    new_notifications = Notification.query.filter(Notification.recipient_id==current_user.id, Notification.read_status==False).all()
    if current_user.is_manager():
        form = SearchForm()
        search_employees = get_search_employees()
        if active_projects:
            if len(active_projects)==1:
                project_name=active_projects[0].name
                project_id=active_projects[0].id

                employees = get_by_project(project_id)
                
                criteria = {'project_id':project_id}
                
                team_averages = averages_dicts_to_list(criteria,start,end)

                return render_template('index.html', user=current_user, employees=employees,active_projects=active_projects,
                                        inactive_projects=inactive_projects, project_name=project_name, project_id=project_id,
                                        new_notifications=new_notifications,form=form, search_employees=search_employees,team_averages=team_averages) 
            
            elif len(active_projects) > 1:
                return redirect(url_for('views.home_filter', project_id=active_projects[0].id))
        else:
            if inactive_projects:
                return render_template('index.html', user=current_user,inactive_projects=inactive_projects,new_notifications=new_notifications,form=form, search_employees=search_employees) #removed len of list
            else:
                return render_template('index.html', user=current_user,new_notifications=new_notifications,form=form, search_employees=search_employees)

    else:
        comment_form = CommentForm(request.form)
        
        if len(active_projects)==1:            
            evals = Eval.query.filter_by(member_id=current_user.id,project_id=active_projects[0].id).all()
            
            if len(evals) > 0:
                criteria = {'member_id':current_user.id}
                
                all_averages = averages_dicts_to_list(criteria,start,end)
                
                comments = Comment.query.join(Comment.evaluation).filter(
                        or_(Eval.manager_id==current_user.id,\
                            Eval.member_id==current_user.id)).all()

                return render_template('home.html',user=current_user,comment_form=comment_form,comments=comments,evals=evals, all_averages=all_averages,
                                        active_projects=active_projects,new_notifications=new_notifications)
            else:
                return render_template('home.html',user=current_user,comment_form=comment_form,evals=evals,active_projects=active_projects,new_notifications=new_notifications)
        
        elif len(active_projects)>1:
            return redirect(url_for('views.home_filter',project_id=active_projects[0].id))
        else:            
            if inactive_projects:
                return render_template('home.html', user=current_user,inactive_projects=inactive_projects,new_notifications=new_notifications) #removed len of list
            else:
                return render_template('home.html', user=current_user,new_notifications=new_notifications)

# gave url args a type   
@views.route('/proiect/<project_id>/')
@views.route('/proiect/<project_id>/<start>/<end>/')
@login_required
def home_filter(project_id,start:str=None,end:str=None):
    active_projects = [project for project in sorted(current_user.projects, key=attrgetter('id')) if project.status == 1]
    inactive_projects = [project for project in sorted(current_user.projects, key=attrgetter('id')) if project.status == 0]
    
    check_inactive_id = Project.query.filter_by(id=project_id,status=0).with_entities(Project.id).first()

    new_notifications = Notification.query.filter(Notification.recipient_id==current_user.id, Notification.read_status==False).all()
    if check_inactive_id is not None:
        if check_inactive_id[0] == project_id:
            return redirect(url_for('views.home'))
    else:
        pass
    current_project = Project.query.get(project_id)
    project_name = current_project.name
    if current_user.is_manager():
        form = SearchForm()
        search_employees = get_search_employees()
        
        if current_user in current_project.users:
            if len(active_projects) > 1:
                employees = get_by_project(project_id)
                
                criteria = {'project_id':project_id}
                team_averages = averages_dicts_to_list(criteria,start,end,True)

                return render_template('index.html', user=current_user, employees=employees, project_name=project_name,new_notifications=new_notifications,team_averages=team_averages,
                                        project_id=project_id,inactive_projects=inactive_projects,active_projects=active_projects,form=form,search_employees=search_employees) 
            else:
                return redirect(url_for('views.home'))
        else:
            return redirect(url_for('views.not_allowed'))
    else:
        comment_form = CommentForm(request.form)
        evals = Eval.query.filter_by(member_id=current_user.id,project_id=project_id).all()
        assignments = [assignment for assignment in current_user.assignments if assignment.project_id == project_id]

        if Eval.query.filter_by(member_id=current_user.id).first():
            comments = Comment.query.join(Comment.evaluation).filter(
                    or_(Eval.manager_id==current_user.id,\
                        Eval.member_id==current_user.id)).all()
                        
            criteria = {'member_id':current_user.id}
            
            all_averages = averages_dicts_to_list(criteria,start,end)
                            
            evals = Eval.query.filter_by(member_id=current_user.id,project_id=project_id).all()
            if len(evals) > 0:
                criteria = {'member_id':current_user.id, 'project_id':current_project.id}

                project_averages =  averages_dicts_to_list(criteria,start,end)

                return render_template('home.html',user=current_user,comment_form=comment_form,comments=comments,evals=evals,inactive_projects=inactive_projects,project_name=project_name
                            ,active_projects=active_projects,new_notifications=new_notifications, assignments=assignments,all_averages=all_averages,project_averages=project_averages) 

            else:
                return render_template('home.html',user=current_user,comment_form=comment_form,evals=evals,inactive_projects=inactive_projects,project_name=project_name
                            ,active_projects=active_projects,new_notifications=new_notifications, assignments=assignments,all_averages=all_averages,comments=comments) 

            
        return render_template('home.html',user=current_user,comment_form=comment_form,active_projects=active_projects,inactive_projects=inactive_projects,
                    evals=evals,project_name=project_name,new_notifications=new_notifications,assignments=assignments)

# long routes can be replaced with 'path:', generate paths in jinja 
@views.route('/proiect/<project_id>/membri/<id>/<start>/<end>/', methods=["POST","GET"])
@views.route('/proiect/<project_id>/membri/<id>/', methods=["POST","GET"])
@login_required
def employee(project_id,id,start:str=None,end:str=None):
    if current_user.is_manager():
        current_employee = Usr.query.get(id)
        current_project = Project.query.get(project_id)
        
        if current_employee in current_project.users and current_user in current_project.users:
            project_name = current_project.name
            new_notifications = Notification.query.filter(Notification.recipient_id==current_user.id, Notification.read_status==False).all()    
            
            if current_employee.assignments:
                assignments = [assignment for assignment in current_employee.assignments if assignment.project_id == current_project.id]

            form = SearchForm()
            comment_form = CommentForm(request.form)
            
            active_projects = [project for project in current_employee.projects if project.status == 1]
            search_employees = get_search_employees()
            employees = get_by_project(project_id, current_employee)
            if Eval.query.filter_by(member_id=current_employee.id).first():                
                criteria = {'member_id':current_employee.id}
                all_averages = averages_dicts_to_list(criteria,start,end)

                evals = Eval.query.filter_by(member_id=id,project_id=project_id).all()
                if len(evals) > 0:
                    criteria = {'member_id':current_employee.id, 'project_id':current_project.id}
                    
                    project_averages = averages_dicts_to_list(criteria,start,end)

                    comments = Comment.query.join(Comment.evaluation).filter(
                        or_(Eval.manager_id==current_user.id,\
                            Eval.member_id==current_user.id)).all()

                    return render_template('employee.html', user=current_user, current_employee=current_employee,
                            employees=employees,comment_form=comment_form,current_project=current_project,project_name=project_name,
                            project_id=project_id,evals=evals,search_employees=search_employees,                                                          
                            comments=comments,active_projects=active_projects,all_averages=all_averages,project_averages=project_averages,
                            new_notifications=new_notifications,form=form,assignments=assignments)

                else:
                    return render_template('employee.html', user=current_user, current_employee=current_employee,all_averages=all_averages,
                                            employees=employees,comment_form=comment_form,current_project=current_project, project_name=project_name, search_employees=search_employees,
                                            project_id=project_id,evals=evals,active_projects=active_projects,new_notifications=new_notifications,
                                            form=form,assignments=assignments)
            else:
                return render_template('employee.html', user=current_user, current_employee=current_employee,employees=employees,comment_form=comment_form,
                                            current_project=current_project, project_name=project_name, search_employees=search_employees,
                                            project_id=project_id,active_projects=active_projects,new_notifications=new_notifications,
                                            form=form,assignments=assignments)
        else:
            return redirect(url_for('views.not_allowed'))
    else:
        return redirect(url_for('views.not_allowed'))
    
@views.route('/redirectionare-catre-user/<id>')
@login_required
def employee_redirect(id):
    if current_user.is_manager():
        current_employee = Usr.query.get(id)
        projects = [project for project in current_employee.projects if project in current_user.projects and project.status == 1]
        
        if len(projects)>0:
            return redirect(url_for('views.employee',project_id=projects[0].id,id=id))
        else:
            return redirect(request.referrer)
    else:
        return redirect(url_for('views.not_allowed'))

@views.route('/proiect/<project_id>/membri/<id>/evaluare/', methods=['POST', 'GET'])
@login_required
def evaluation(id, project_id):
    if current_user.is_manager():
        current_employee = Usr.query.get(id)
        current_project = Project.query.get(project_id)

        employees = get_by_project(project_id)
        form = SearchForm()
        search_employees = get_search_employees()
        
        if current_employee in current_project.users and current_user in current_project.users:
            new_notifications = Notification.query.filter(Notification.recipient_id==current_user.id, Notification.read_status==False).all()
            assignments = [assignment for assignment in current_employee.assignments if assignment.project_id == current_project.id]
            
            if request.method == "POST":
                data = request.get_json()

                error_fields = [f'eval-check-{i}' for i in range(1,31) if str(i) not in [re.sub('-','',key[-2:]) for key,_ in data.items()]]
                error_fields = dict(map(lambda x:(x,x), error_fields))

                today = date.today()
                
                start_date = datetime.strptime(data['startDate'],"%Y-%m-%d").date()
                end_date = datetime.strptime(data['endDate'],"%Y-%m-%d").date()

                if len(data) < 1:
                    return make_response(send_json_response('danger', 'Formularul este gol', data, label='',error_fields=error_fields),404)
                elif len(data) < 26: 
                    return make_response(send_json_response('danger', 'Formularul este incomplet', data, label='',error_fields=error_fields),404)
                elif end_date > today:
                    error_fields['endDate'] = 'endDate'                
                    return make_response(send_json_response('danger', 'Data sfarsirii proiectului nu este corecta', data, label='',error_fields=[('endDate','endDate')]),404)
                elif start_date > today or start_date > end_date:
                    error_fields['startDate'] = 'startDate'
                    return make_response(send_json_response('danger', 'Data inceperii proiectului nu este corecta', data, label='',error_fields=[('startDate','startDate')]),404)
                    
                row_names = [f"row_{i}" for i in range (1,25)]
                scores = [value for key,value in data.items() if key.startswith("eval-check-")]
                scores_dict = {row_names[i]:scores[i] for i in range(len(scores))}
                
                evaluation = Eval(scores=scores_dict,start_date=start_date,end_date=end_date,
                                  manager_id=current_user.id,member_id=id,project_id=project_id)
                    
                db.session.add(evaluation)
                
                try: 
                    db.session.commit()
                except Exception as e:
                    print(e)
                    no_effect(data,message='Evaluarea nu a fost salvata')
                    
                else:                    
                    notification = Notification(title="Evaluare Noua",text=f"Ai primit o evaluare de la {current_user.name.title()} {current_user.surname.title()}",read_status=0,if_comment=0,sender_id=current_user.id,recipient_id=id,eval_id=evaluation.id)
                    db.session.add(notification)                                       
                    db.session.commit()                                
  
                return make_response(send_json_response('success', 'Evaluare salvata cu success', data),200)
            current_project = Project.query.get(project_id)
            
            return render_template('evaluation.html', user=current_user, form=form,
                                   current_employee=current_employee,employees=employees, 
                                   project_id=project_id, current_project=current_project,new_notifications=new_notifications,
                                   assignments=assignments,search_employees=search_employees) #removed len of list
        else:
            return redirect(url_for('views.not_allowed'))
    else:
        return redirect(url_for('views.not_allowed'))

# see all employees in the company and edit their project
@views.route('/firma/')
@login_required
def company():
    if current_user.is_manager():        
        new_notifications = Notification.query.filter(Notification.recipient_id==current_user.id, Notification.read_status==False).all()        
        
        form = SearchForm()
        search_form = SearchForm(request.form)
        project_form = ProjectForm(request.form)
        
        search_employees = get_search_employees()
        
        all_employees = get_by_roles('member')
        
        project_choices = [project for project in current_user.projects if project.status==1]
        active_projects = [project for project in sorted(current_user.projects, key=attrgetter('id')) if project.status == 1]
        inactive_projects = [project for project in sorted(current_user.projects, key=attrgetter('id')) if project.status == 0]    
        
        projects = Project.query.all()
        departments = Department.query.all()
        if search_form.validate_on_submit() and request.method == "POST":

            employee.searched = search_form.searched.data
            searched_employees = [user for user in search_employees
                if  employee.searched.lower() in str(user.name).lower() 
                or employee.searched.lower() in str(user.surname).lower()]
            

            return render_template("company.html",
                                    user=current_user,
                                    form=form,
                                    search_form=search_form,
                                    project_form=project_form,
                                    searched_employees=searched_employees,
                                    search=employee.searched,
                                    search_employees=search_employees,
                                    all_employees=all_employees,
                                    projects=projects,new_notifications=new_notifications,
                                    project_choices=project_choices,departments=departments,
                                    active_projects=active_projects,inactive_projects=inactive_projects)

        return render_template("company.html",
            user=current_user,
            form=form,
            search_form=search_form,
            project_form=project_form,
            search_employees=search_employees,
            project_choices=project_choices,
            all_employees=all_employees,
            projects=projects,new_notifications=new_notifications,departments=departments,
            active_projects=active_projects,inactive_projects=inactive_projects)
    else:
        return redirect(url_for('views.not_allowed'))

        