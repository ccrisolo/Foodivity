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
INTENSITY= ( 
    ('L', 'light'),
    ('M', 'moderate'),
    ('S', 'strenuous'),
    ('V', 'very strenuous')
)
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

    class Meta:
        ordering = ['-date']


class Activity(models.Model):
    date = models.DateField(
        blank=True,
        null=True
    )
    type_activity =  models.CharField(max_length=100)
    duration = models.IntegerField()
    calories_burned = models.IntegerField(
        blank=True,
        null=True
    )
    # changed to autofill calories based on duration and intensity 
    activity_intensity = models.CharField(
        max_length=1,
        choices=INTENSITY, 
        default=[0][0]
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    def __str__(self):
        return self.type_activity
    
    def get_absolute_url(self):
        return reverse('index')
    
class ProfilePhoto(models.Model):
    url = models.CharField(max_length=200)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.url

class MealPhoto(models.Model):
    url = models.CharField(max_length=200)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.url