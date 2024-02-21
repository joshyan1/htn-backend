# Hack The North Backend Challenge

## 

## Database 
The Hack The North Backend database currently makes use of 3 tables: `users`, `user_skills`, and `skills`

The `users` table is used to store all user information. It contains the following data fields: 

`userid (int)`: Primary key used as unique identifier for the user \
`name (str)`: User's name \
`company (str)`: User's company \
`email (str)`: User's email. This is a unique field which prevents duplicate registrations with the same email \
`phone (str)`: User's phone number. 

The `skills` table contains the following data fields:

`skillid (int)`: Primary key used as a unique identifier for the skill \
`skill (str)`: Skill's name. Unique field preventing duplicate skills
`frequency (int)`: Number of users with this skill

The `user_skills` table contains the following data:

`id (int)`: Primary key used as a unique identifier for the user-skill relationship \
`user_id (int)`: The ID of the user
`skill_id (int)`: The Id of the skill
`rating (int)`: User's skill rating

## API
`GET /users`: Get all user data, ordered by user ID. Optional ordering by name, email, and company; optional filtering by name. \
`GET /users/<int:user_id>`: Gets user info by ID. \
`PUT /users/<int:user_id>`: Updates user info by ID. \
`GET /insert-data`: Resets tables and inserts data according to selected JSON. \
`POST /register`: Registers a new user. \
`GET /skills`: Get all skills data. Optional filtering by frequency and name. \
`GET /skills/<str:skill_name>`: Get users associated with skill. Optional ordering by rating. 

