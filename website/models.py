from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import load_only
from sqlalchemy import Date, cast
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous.jws import TimedJSONWebSignatureSerializer as Serializer
from . import db,datetime
from . import app

project_users = db.Table('project_users',
    db.Column('user_id', db.Integer, db.ForeignKey('usr.id')),
    db.Column('proiect_id', db.Integer, db.ForeignKey('project.id')))

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('usr.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')))

assignments_users = db.Table('assignments_users',
    db.Column('user_id', db.Integer, db.ForeignKey('usr.id')),
    db.Column('assignment_id', db.Integer, db.ForeignKey('assignment.id')))

class BaseModel:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creation_date = db.Column(db.DateTime(timezone=True), default=func.now())

class Usr(db.Model, BaseModel, UserMixin):     
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    _psw = db.Column(db.String(128), nullable=False)
    
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)    
    
    notifications_sent = db.relationship('Notification', foreign_keys='Notification.sender_id',backref=db.backref('sender'),lazy='dynamic')
    notifications_received = db.relationship('Notification', foreign_keys='Notification.recipient_id',backref=db.backref('recipient'),lazy='dynamic')
    manager_evals = db.relationship('Eval', foreign_keys='Eval.manager_id',backref=db.backref('manager'), lazy='dynamic')
    member_evals = db.relationship('Eval', foreign_keys='Eval.member_id',backref=db.backref('member'), lazy='dynamic')

    roles = db.relationship('Role', secondary=roles_users,
                          backref=db.backref('users'),lazy='dynamic')
    projects = db.relationship('Project', secondary=project_users,
                              backref=db.backref('users'),lazy='dynamic')    
    assignments = db.relationship('Assignment', secondary=assignments_users,
                              backref=db.backref('users'),lazy='dynamic')    

    def __init__(self,name,surname,email,_psw,department_id,total=0):
        self.name = name
        self.surname = surname
        self.email = email
        self._psw = _psw
        # user has no total evaluations at registration
        self.total = total
        self.department_id = department_id

    # transform query item intro list to verify if it contains manager
    def is_manager(self):
        if "manager" in (list(*(self.roles.with_entities(Role.name)))):
            return True
        else:
            return False

    def get_reset_token(self,expires_sec=3600):
        s = Serializer(app.secret_key, expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Usr.query.get(user_id)

    @hybrid_property
    def psw(self):
        return self._psw

    @psw.setter
    def psw(self,password):
        
        self._psw = generate_password_hash(password)
        
    def verify_psw(self,password) -> bool: 
        return check_password_hash(self._psw,password)
    

class Project(db.Model, BaseModel):    
    name = db.Column(db.String(60), nullable=False)
    status = db.Column(db.Integer,default=1)
    
    evals = db.relationship('Eval', backref=db.backref('project'),lazy='dynamic')
    assignments = db.relationship('Assignment',backref=db.backref('project'),lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Proiect: {self.name}'

class Role(db.Model, BaseModel):    
    name = db.Column(db.String(80))    

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Rol: {self.name}'

class Department(db.Model, BaseModel):    
    name = db.Column(db.String(80))
    
    membri = db.relationship("Usr", backref=db.backref('department'),lazy='dynamic')    

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.name}'

class Assignment(db.Model, BaseModel):    
    name = db.Column(db.String(80), nullable=False)
    
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)    

    def __init__(self,name,project_id):
        self.name = name
        self.project_id = project_id

    def __repr__(self):
        return '{}'.format(self.name.title())

class Comment(db.Model, BaseModel):    
    title = db.Column(db.String(35))
    text = db.Column(db.String(1500), nullable=False)
    criteria = db.Column(db.String(21))
    
    user_id = db.Column(db.Integer, db.ForeignKey('usr.id'), nullable=False)
    eval_id = db.Column(db.Integer, db.ForeignKey('eval.id'), nullable=False)
    
    def __init__(self,title,text,criteria,user_id,eval_id):
        self.title = title
        self.text = text
        self.criteria = criteria
        self.user_id = user_id
        self.eval_id = eval_id

    # if the comment has a title display it, else display the start of the text
    def __repr__(self):
        if self.title:
            return '{}'.format(self.title)
        else:
            return '{}..'.format(self.text[0:25])

class Notification(db.Model, BaseModel):    
    title = db.Column(db.String(35))
    text = db.Column(db.String(1500), nullable=False)
    read_status = db.Column(db.Boolean,default=False, nullable=False)
    if_comment = db.Column(db.Boolean,default=False, nullable=False)
    
    sender_id = db.Column(db.Integer, db.ForeignKey('usr.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('usr.id'), nullable=False)
    eval_id = db.Column(db.Integer, db.ForeignKey('eval.id'), nullable=False)    
    
    def __init__(self,title:str,text:str,read_status:bool,if_comment:bool,eval_id:int, sender_id:int, recipient_id:int):
        self.title = title
        self.text = text
        self.read_status = read_status
        self.if_comment = if_comment
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.eval_id = eval_id

    # if the comment has a title display it, else display the start of the text
    def __repr__(self):
        if self.title:
            return '{}'.format(self.title)
        else:
            return '{}..'.format(self.text[0:25])

class Eval(db.Model, BaseModel):    
    row_1 = db.Column(db.Integer, nullable=False)
    row_2 = db.Column(db.Integer, nullable=False)
    row_3 = db.Column(db.Integer, nullable=False)
    row_4 = db.Column(db.Integer, nullable=False)
    row_5 = db.Column(db.Integer, nullable=False)
    row_6 = db.Column(db.Integer, nullable=False)
    row_7 = db.Column(db.Integer, nullable=False)
    row_8 = db.Column(db.Integer, nullable=False)
    row_9 = db.Column(db.Integer, nullable=False)
    row_10 = db.Column(db.Integer, nullable=False)
    row_11 = db.Column(db.Integer, nullable=False)
    row_12 = db.Column(db.Integer, nullable=False)
    row_13 = db.Column(db.Integer, nullable=False)
    row_14 = db.Column(db.Integer, nullable=False)
    row_15 = db.Column(db.Integer, nullable=False)
    row_16 = db.Column(db.Integer, nullable=False)
    row_17 = db.Column(db.Integer, nullable=False)
    row_18 = db.Column(db.Integer, nullable=False)
    row_19 = db.Column(db.Integer, nullable=False)
    row_20 = db.Column(db.Integer, nullable=False)
    row_21 = db.Column(db.Integer, nullable=False)
    row_22 = db.Column(db.Integer, nullable=False)
    row_23 = db.Column(db.Integer, nullable=False)
    row_24 = db.Column(db.Integer, nullable=False)
    
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    
    comments = db.relationship('Comment', backref=db.backref('evaluation'),lazy='dynamic')
    notifications = db.relationship('Notification', backref=db.backref('evaluation'),lazy='dynamic')
    
    manager_id = db.Column(db.Integer, db.ForeignKey('usr.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('usr.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)    

    def __init__(self,scores:dict,start_date:datetime, end_date:datetime,manager_id:int,member_id:int,project_id:int):
        if len(scores) != 24:
            raise ValueError("Expected 24 row values")
                
        for key, value in scores.items():
            setattr(self, key, value)
            
        self.start_date = start_date
        self.end_date = end_date
        self.manager_id = manager_id
        self.member_id = member_id
        self.project_id = project_id
                
    def __repr__(self):
        return f'{self.creation_date}'
            
    def interval(self, start:str, end:str):     
        if not start or not end:
            return False
        start = str(start).rsplit(' ', 1)[0]      
        end = str(end).rsplit(' ', 1)[0]         
            
        eval_date = str(self.creation_date).rsplit(' ', 1)[0]    
        
        try:
            date = datetime.strptime(eval_date, "%Y-%m-%d").date()
            start = datetime.strptime(start,"%Y-%m-%d").date()
            end = datetime.strptime(end,"%Y-%m-%d").date()
        except ValueError:
            return False 
        
        return (date >= start and date <= end)
