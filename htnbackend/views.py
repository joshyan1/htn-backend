import requests
from django.http import JsonResponse, HttpResponseNotAllowed
import json
from .models import *
from django.views.decorators.csrf import csrf_exempt


#http://localhost:8000/users/#id
@csrf_exempt #for testing
def user_data(request, user_id):

    try:
        user_initial = users.objects.filter(userid=user_id).values()[0]
        user_obj = users.objects.filter(userid=user_id).first()

         #get request
        if request.method == 'GET':
            data = get_user_data(user_initial)
            return JsonResponse(data, status=200, json_dumps_params={'indent': 4})

        elif request.method == 'PUT':
            try:
                data = json.loads(request.body)

                for key in data:
                    print(key)
                    print(user_initial)
                    if key in user_initial.keys():
                        setattr(user_obj, key, data[key])
                        user_obj.save()

                    #if we're updating skills
                    elif key == 'skills':

                        for skill in data[key]:

                            #cases:
                                #skill exists, user doesn't have skill --> create new user_skill, add to db, update skill freq
                                #skill exists, user has skill --> get old user_skill, update rating
                                #skill doesn't exists --> create new skill, create new user_kill, add to db

                            if skills.objects.filter(skill=skill['skill']).exists():
                                skill_obj = skills.objects.filter(skill=skill['skill']).first()

                                if user_skills.objects.filter(user_id=user_obj, skill_id=skill_obj):
                                    update_skill = user_skills.objects.filter(user_id=user_obj, skill_id=skill_obj).first()
                                    update_skill.rating = skill['rating']
                                    update_skill.save()

                                else:
                                    skill_obj.frequency += 1
                                    skill_obj.save()
                                    
                                    #add to user skills
                                    new_user_skills = user_skills(
                                        user = user_obj,
                                        skill = skill_obj,
                                        rating = skill['rating']
                                    )

                                    new_user_skills.save()

                            else:
                                skill = skills(
                                    skill=skill['skill'],
                                    frequency=1,
                                )

                                skill.save()
                            

                    #ignore invalid keys
                    else:
                        print("key is not a valid data field")

                updated_user = get_user_data(users.objects.filter(userid=user_id).values()[0])

                #print(user_obj)
                #print(updated_user)
                return JsonResponse(updated_user, status=200, json_dumps_params={'indent': 4})

                #return updated user inf
            except json.JSONDecodeError:
                return HttpResponse("Invalid JSON", status=400)
        else:
            return HttpResponse("Invalid HTTP Protocol", status=403)

    except users.DoesNotExist:
        return HttpResponse("User not found", status=404)

   
def get_user_data(user):
    uid = user['userid']
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

        user.update(person_skills)  

    return user

#http://localhost:8000/users
def all_users(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    output = []

    data = users.objects.all().values()
    for e in data:
        output.append(get_user_data(e))

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


        