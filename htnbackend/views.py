import requests
from django.http import JsonResponse, HttpResponseNotAllowed
import json
from .models import *

#http://localhost:8000/users
def user_data(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
        
    output = []

    data = users.objects.all().values()
    for e in data:
        uid = e['userid']
        person_skills = {
            'skills': []
        }

        for skill in user_skills.objects.filter(user_id=uid).values():
            skill_object = skills.objects.filter(skillid=skill['skill_id']).values()[0]

            rating = skill['rating']
            skill_name = skill_object['skill']

            person_skills['skills'].append({
                'skill': skill_name,
                'rating':rating,
            })

            e.update(person_skills)    
        output.append(e)

    return JsonResponse(output, status=200, safe=False, json_dumps_params={'indent': 4})


#save data into database by visiting localhost:8000/insert-data
def insert(request):
    #insert data into database
    user_data = requests.get("https://gist.githubusercontent.com/DanielYu842/607c1ae9c63c4e83e38865797057ff8f/raw/b84b8bce73fadb341258e86265a6091779908344/HTN_2023_BE_Challenge_Data.json").json()
    for person in user_data:
        new_entry(person)

    return JsonResponse({'done': "yes"}, status=200)
    
def new_entry(data):
    new_user = users(
        name = data['name'],
        email = data['email'],
        company = data['company'],
        phone = data['phone'],
    )

    if users.objects.filter(email=data['email']).exists():
        print(data['name'] + " is already present in the database")
        return
    
    new_user.save()

    insert_skills(data['skills'], new_user)

def insert_skills(input_skills, user):

    skill = ""

    for i in input_skills:
        #if skill exists, get skill object then update frequency
        if skills.objects.filter(skill=i['skill']).exists():
            skill = skills.objects.filter(skill=i['skill']).first()
            skill.frequency += 1
            skill.save()

        #if skill doesn't exist, create new skill
        else:
            skill = skills(
                skill=i['skill'],
                frequency=1,
            )

            skill.save()
        
        #add to user skills
        new_user_skills = user_skills(
            user = user,
            skill = skill,
            rating = i['rating']
        )

        new_user_skills.save()


        