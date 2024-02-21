# Hack The North Backend Challenge

## Database 

## API
`GET /users`: Get all user data, ordered by user ID. Optional ordering by name, email, and company. \
`GET /users/<int:user_id>`: Gets user info by ID. \
`PUT /users/<int:user_id>`: Updates user info by ID. \
`GET /insert-data`: Resets tables and inserts data according to selected JSON. \
`POST /register`: Registers a new user. \
`GET /skills`: Get all skills data. Optional filtering by frequency and name. \
`GET /skills/<str:skill_name>`: Get users associated with skill. Optional ordering by rating. 

