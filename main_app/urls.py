from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile_index, name='index'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/create/', views.ProfileCreate.as_view(), name='profile_create'),
    path('profile/<int:profile_id>/add_meal/', views.add_meal, name='add_meal'),
    path('meal/<int:pk>/delete/', views.MealDelete.as_view(), name='delete_meal'),
    path('meal/<int:pk>/update/', views.MealUpdate.as_view(), name='update_meal'),
    path('activity/<int:pk>/update/', views.ActivityUpdate.as_view(), name='update_activity'),
    path('activity/<int:pk>/delete/', views.ActivityDelete.as_view(), name='delete_activity'),
    path('profile/<int:profile_id>/activity/create/', views.ActivityCreate.as_view(), name='activity_create'),
    
]