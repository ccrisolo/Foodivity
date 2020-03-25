from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

import uuid
import boto3

from .models import Profile, Meal, Activity, ProfilePhoto, MealPhoto
from .forms import MealForm

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'foodivity'

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def profile_index(request):
    profile = Profile.objects.get(user = request.user)
    meal_form = MealForm()
    meals = Meal.objects.filter(profile = profile)
    activities = Activity.objects.filter(profile = profile)
    suggested_cal_male = ((10 * profile.weight) + (6.25 * profile.height) + 5)
    suggested_cal_female = ((10 * profile.weight) + (6.25 * profile.height) - 161)
    total_calories = sum(meal.calories for meal in meals)
    burned_calories = sum(activity.calories_burned for activity in activities)
    remaining_calories = (total_calories - burned_calories)
    return render(request, 'profile/index.html', {'profile': profile, 'meal_form': meal_form, 'total_calories': total_calories, 'burned_calories': burned_calories, 'remaining_calories': remaining_calories, 'suggested_cal_male': suggested_cal_male, 'suggested_cal_female': suggested_cal_female})

def add_meal(request, profile_id):
    form = MealForm(request.POST)
    if form.is_valid():
        new_meal = form.save(commit=False)
        new_meal.profile_id = profile_id
        new_meal.save()
    return redirect('index')

def add_photo_profile(request, profile_id):
    print(profile_id)
    photo_file = request.FILES.get('photo-file', None)
    print(photo_file)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = ProfilePhoto(url=url, profile_id=profile_id)
            print(photo)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('index')

def add_photo_meal(request, meal_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = MealPhoto(url=url, meal_id=meal_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('index')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('profile_create')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class ProfileCreate(CreateView):
  model = Profile
  fields = ['first_name', 'last_name', 'height', 'weight', 'sex', 'activity_level']
  
  def form_valid(self, form):
      form.instance.user = self.request.user
      return super().form_valid(form)

class ProfileUpdate(UpdateView):
  model = Profile
  fields = ['first_name', 'last_name', 'height', 'weight', 'sex', 'activity_level']

class MealUpdate(UpdateView):
  model = Meal
  fields = ['date', 'name', 'ingredients', 'calories']

class MealDelete(DeleteView):
  model = Meal
  success_url = '/profile/'
  
class ActivityCreate(CreateView):
  model = Activity 
  fields = ['type_activity', 'duration', 'calories_burned', 'date', 'activity_intensity']
  success_url = '/profile/'
  
  def form_valid(self, form):
    form.instance.user = self.request.user
    # url params are available as a kwarg on self as follows
    form.instance.profile_id = self.kwargs['profile_id']
    return super().form_valid(form)

class ActivityUpdate(UpdateView):
  model = Activity
  fields = ['type_activity', 'duration', 'calories_burned', 'date', 'activity_intensity']
  
class ActivityDelete(DeleteView):
  model = Activity
  success_url = '/profile/'
  
class ProfilePhotoDelete(DeleteView):
  model = ProfilePhoto
  success_url = '/profile/'

class MealPhotoDelete(DeleteView):
  model = MealPhoto
  success_url = '/profile/'