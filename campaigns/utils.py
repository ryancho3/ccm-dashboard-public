from django.contrib.auth.models import User
from .models import Manager, School, Impression


def register_check(input):
    if input['username'] == '':
        return "Username cannot be empty."
    elif input['password'] == '':
        return "Password cannot be empty"
    elif input['repeat_password'] == '':
        return "Repeat password cannot be empty"
    elif input['school'] == '':
        return "Please select your school."
    elif input['first_name'] == '':
        return "First Name cannot be empty"
    elif input['last_name'] == '':
        return "Last Name cannot be empty"
    elif input['email'] == '':
        return "Email cannot be empty"
    
    user = User.objects.filter(username=input['username']).first()
    if user:
        return "username taken"
        

    if input['password'] != input['repeat_password']:
        return "Passwords do not match."

    return "valid"

def register_manager_from_post(post):
    user = User()
    user.first_name = post['first_name']
    user.last_name = post['last_name']
    user.username = post['username']
    user.set_password(post['password'])
    user.email = post['email']
    user.save()
    school = School.objects.get(code=post['school'])
    manager = Manager(user=user)
    manager.save()
    manager.school.add(school)
    manager.save()
    return user


def get_school_impressions(user, campaign):
    
    if user.is_staff or user.is_superuser:
        school_list = School.objects.all()
    else:
        school_list = user.manager.school.all()
    school_impressions = []
    for school in school_list:
        school_impressions.append((school.name, school.code, Impression.objects.filter(campaign=campaign, school=school).count()))
    recent_impressions = Impression.objects.filter(campaign=campaign).order_by('datetime')[0:10]

    return school_impressions, recent_impressions