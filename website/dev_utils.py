from . import db
from .models import Usr,Role,Department
from werkzeug.security import generate_password_hash
from flask import url_for
import string
import random
from faker import Faker

# populate db  function, can be edited to quickly add many real users
# role is integer: 1 for manager, 2 for member
# project is integer: check data base for needed project id
def create_roles():
    manager = Role(name='manager')
    member = Role(name='member')
    db.session.add(manager)
    db.session.add(member)
    db.session.commit()

def create_departments():
    dpt1 = Department(name='departament1')
    dpt2 = Department(name='departament2')
    db.session.add(dpt1)
    db.session.add(dpt2)
    db.session.commit()

def create_fake_users(n:int,psw:str,role_id:int,start:int):
    faker = Faker()
    for i in range(start,n+start):
        name=faker.name().split()
        
        last=name[0].lower()
        first=name[1].lower()
        
        user = Usr(name=first,surname=last,
                    email=f'{first}.{last}@gmail.com',_psw=generate_password_hash(psw),total=0,department_id=1)
        user.roles.append(Role.query.get(role_id))
        
        db.session.add(user)
        db.session.commit()
    

def generate_random_password():
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    length = random.randint(12,16)

    random.shuffle(characters)
	
    password = []
    for i in range(length):
        password.append(random.choice(characters))

    random.shuffle(password)
	
    return "".join(password)