from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Meal

# Create your views here.
def home(request):
    return HttpResponse('<h1>Foodivity</h1>')

def about(request):
    return render(request, 'about.html')

def profile_index(request):
    profile = Profile.objects.filter(user = request.user)
    return render(request, 'profile/index.html', {'profile': profile})

def profile_detail(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    return render(request, 'profile/detail.html', {
        'profile': profile,
    })

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
    fields = ['height', 'weight', 'sex', 'activity_level']
    
    def form_valid(self, form):
    # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
        return super().form_valid(form)


