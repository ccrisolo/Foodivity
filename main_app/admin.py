from django.contrib import admin
from .models import Meal, Profile, Activity, ProfilePhoto, MealPhoto 
# Register your models here.
admin.site.register(Activity)
admin.site.register(Meal)
admin.site.register(Profile)
admin.site.register(ProfilePhoto)
admin.site.register(MealPhoto)