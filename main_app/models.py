from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


SEX = (
    ('M', 'male'),
    ('F', 'female')
)
ACTIVITY = (
    ('L', 'low'),
    ('M', 'moderate'),
    ('H', 'high')
)
# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    height = models.IntegerField()
    weight = models.IntegerField()
    
    activity_level = models.CharField(
        max_length=1,
        choices = ACTIVITY
    )
    sex = models.CharField(
        max_length=1,
        choices = SEX
    )




class Meal(models.Model):
    date = models.DateField(date.today())
    name = models.CharField(max_length=25)
    ingredients = models.CharField(max_length=100)
    calories = models.IntegerField()

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} on {self.date} has {self.calories}"

