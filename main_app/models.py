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
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    height = models.IntegerField()
    weight = models.IntegerField()
    
    activity_level = models.CharField(
        max_length=1,
        choices=ACTIVITY,
        default=[0][0]
    )
    sex = models.CharField(
        max_length=1,
        choices=SEX,
        default=[0][0]
    )

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('index')

class Meal(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=25)
    ingredients = models.CharField(max_length=100)
    calories = models.IntegerField()

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} on {self.date} has {self.calories}"

    def get_absolute_url(self):
        return reverse('index')

