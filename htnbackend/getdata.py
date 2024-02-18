import requests
import json
from models import *

def new_entry(data):
    new_user = users(
        name = data['name'],
        email = data['email'],
        company = data['company'],
        phone = data['phone'],
    )

    if users.objects.filter(email=user_data['email']).exists():
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
            skill.frequnecy = skill.frequency + 1
            skill.save()

        #if skill doesn't exist, create new skill
        else:
            skill = skills(
                name=i['skill'],
                frequency=1,
            )

            skill.save()
        
        #add to user skills
        user_skills = user_skills(
            user = user,
            skill = skill,
            rating = i['rating']
        )

        user_skills.save()

#insert data into database
user_data = requests.get("https://gist.githubusercontent.com/DanielYu842/607c1ae9c63c4e83e38865797057ff8f/raw/b84b8bce73fadb341258e86265a6091779908344/HTN_2023_BE_Challenge_Data.json")

for person in user_data:
    new_entry(person)
        