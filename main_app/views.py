from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Meal, Activity
from .forms import MealForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def profile_index(request):
    profile = Profile.objects.filter(user = request.user)
    meal_form = MealForm()
    return render(request, 'profile/index.html', {'profile': profile, 'meal_form': meal_form})

def add_meal(request, profile_id):
    form = MealForm(request.POST)
    if form.is_valid():
        new_meal = form.save(commit=False)
        new_meal.profile_id = profile_id
        new_meal.save()
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

class ActivityUpdate(UpdateView):
  model = Activity
  fields = ['type_activity', 'duration', 'calories_burned', 'date', 'activity_intensity']
  
class ActivityDelete(DeleteView):
  model = Activity
  success_url = '/profile/'