from django.db import models

class users(models.Model):
    userid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    email = models.EmailField(unique=True, max_length=50)
    phone = models.CharField(max_length=50)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.name

class skills(models.Model):
    skillid = models.AutoField(primary_key=True)
    skill = models.CharField(max_length=50, unique=True)
    frequency = models.IntegerField()

    class Meta:
        db_table = "skills"

    def __str__(self):
        return self.skill

class user_skills(models.Model):
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    skill = models.ForeignKey(skills, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        db_table = "user_skills"

    def __str__(self):
        return f"{self.user.name} - {self.skill.skill}"