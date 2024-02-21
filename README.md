# Hack The North Backend Challenge
Hi, this is my HTN Backend Challenge submission. I hope you guys like it. Thanks for your time and consideration.

Me and you guys when we work on HTN together.
![t1](https://pbs.twimg.com/media/ELO6--zVAAA3woI.jpg)

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
`skill (str)`: Skill's name. Unique field preventing duplicate skills \
`frequency (int)`: Number of users with this skill

The `user_skills` table contains the following data:

`id (int)`: Primary key used as a unique identifier for the user-skill relationship \
`user_id (int)`: The ID of the user \
`skill_id (int)`: The ID of the skill \
`rating (int)`: User's skill rating

## API Endpoints
[`GET /users`](#get-user-data): Get all user data. Optional ordering by name, email, and company; optional filtering by name. \
[`GET /users/<int:user_id>`](#get-users-by-id): Gets user info by ID. \
[`PUT /users/<int:user_id>`](#update-user-info): Updates user info by ID. \
[`GET /insert-data`](#insert-data): Resets tables and inserts data according to selected JSON. \
[`POST /register`](#register): Registers a new user. \
[`GET /skills`](#get-skills): Get all skills data. Optional filtering by frequency and name. \
[`GET /skills/<str:skill_name>`](#get-skill-by-name): Get users associated with skill. Optional ordering by rating. 

### Get User Data
Returns list of all user data as JSON. Data is ordered by UID by default 

Parameters (optional):
- `order`: ordering of user data (options include `name`, `email`, and `company`)
- `name`: filters data by substring provided

#### Examples:
Example Request:
```shell
GET /users
```
Example Response:
```json
{
  [
    {
      "userid": 1,
      "name": "Breanna Dillon",
      "company": "Jackson Ltd",
      "email": "lorettabrown@example.net",
      "phone": "+1-924-116-7963",
      "skills": [
        {
          "skill": "Swift",
          "rating": 4
        },
        {
          "skill": "OpenCV",
          "rating": 1
        }
      ]
    },
    {
      "userid": 2,
      "name": "Kimberly Wilkinson",
      "company": "Moon, Mendoza and Carter",
      "email": "frederickkyle@example.org",
      "phone": "(186)579-0542",
      "skills": [
        {
          "skill": "Foundation",
          "rating": 4
        },
      ]
    },
  ...
  ]
}
```

#### Examples:
Example Request:
```shell
GET /users?order=email&name=Aaron
```

Example Response:
```json
[
  {
    "userid": 664,
    "name": "Aaron Moore",
    "company": "Jones, Bailey and Woods",
    "email": "lewissamuel@example.org",
    "phone": "001-299-875-9008x37941",
    "skills": [
      {
        "skill": "Ember.js",
        "rating": 4
      },
      {
        "skill": "AutoHotkey",
        "rating": 4
      },
      {
        "skill": "Assembly",
        "rating": 1
      }
    ]
  },
  {
    "userid": 651,
    "name": "Aaron Edwards",
    "company": "Clark-Smith",
    "email": "lisa90@example.com",
    "phone": "831.759.4513",
    "skills": [
      {
        "skill": "Flask",
        "rating": 3
      },
      {
        "skill": "Ant Design",
        "rating": 2
      },
      {
        "skill": "COBOL",
        "rating": 2
      }
    ]
  },
  ...
]
```

### Get Users by ID
Returns user's data searched by ID

Example Request:
```shell
GET /users/123
```

Example Response:
```json
{
  "userid": 123,
  "name": "Lisa Ho",
  "company": "Watson, Johnson and Beck",
  "email": "wbrown@example.org",
  "phone": "8894076542",
  "skills": [
    {
      "skill": "Prolog",
      "rating": 2
    },
    {
      "skill": "Buefy",
      "rating": 4
    }
  ]
}
```

### Update User Info
Takes JSON data applicable to the `user` table and updates the information provided. Keys in the JSON data that are not a part of the `user` table are ignored. If skills are provided, then the user either updates their rating for the skill if they previously had it or has it added in. The `user_skills` and `skills` tables are then updated to reflect these new skills.

Example Request:
```shell
PUT /users/123
{
    "phone": "250-507-6991",
    "skills": [
            {
                "skill": "Python",
                "rating": 3
            },
            {
                "skill": "Fortnite"
                "rating": 1
            },
        ]

}
```

Example Response:
```json
{
  "userid": 123,
  "name": "Lisa Ho",
  "company": "Watson, Johnson and Beck",
  "email": "wbrown@example.org",
  "phone": "250-507-6991",
  "skills": [
    {
      "skill": "Prolog",
      "rating": 2
    },
    {
      "skill": "Buefy",
      "rating": 4
    },
    {
      "skill": "Python",
      "rating": 3
    },
    {
      "skill": "Fortnite",
      "rating": 1
    }
  ]
}
```

### Insert Data
Used for setup purposes only. All tables are reset, then populated using the data provided. 

```shell
GET /insert-data
```

### Register
Takes a complete user profile to insert into the database. If the database already contains the user's email, an HTTP Response will notify that the email has already been used. Can be used to manually register new users.

#### Examples
Example Request:
```shell
PUT /register
{
  "name": "Jeffery Dillon",
  "company": "Jackson Ltd",
  "email": "jefferyesemail@example.net",
  "phone": "+1-924-116-7963",
  "skills": [
      {
          "skill": "Swift",
          "rating": 4
      },
      {
          "skill": "Github",
          "rating": 1
      }
  ]
}
```

### Get Skills
Returns all skills data. Default ordering is by UID.

Parameters (optional):
- `min-freq`: Filters skills with frequency greater than or equal to 
- `max-freq`: Filters skills with frequency less than or equal to
- `name`: Filters skills containing this substring (case insensitive)

#### Examples:
Example Request:
```shell
GET /skills?min-freq=22&max-freq=30&name=Er
```

Example Response:
```json
{
  "Ember.js": {
    "frequency": 28
  },
  "Materialize": {
    "frequency": 25
  },
  "Keras-RL": {
    "frequency": 29
  },
  "Keras": {
    "frequency": 22
  }
}
```

### Get Skill by Name
Returns data about users for the skill name provided. The skill is case sensitive

Parameters (optional):
- `order`: order results (options: `rating`)

#### Examples
Example Request:
```shell
GET /skills/Ada
```

Example Response:
```json
{
  "Ada": {
    "frequency": 15,
    "users": {
      "Robin Harvey": {
        "rating": 4,
        "email": "browndouglas@example.net"
      },
      "Angela Johnson": {
        "rating": 2,
        "email": "fjames@example.com"
      },
      "Jean Ramirez DDS": {
        "rating": 3,
        "email": "micheal93@example.org"
      },
      "Melanie Trevino": {
        "rating": 2,
        "email": "tknox@example.net"
      },
      "Chelsey Meadows": {
        "rating": 1,
        "email": "shane25@example.org"
      },
      ...
    }
  }
}
```