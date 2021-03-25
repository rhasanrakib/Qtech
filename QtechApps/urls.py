
from . import views
from django.urls import path
urlpatterns = [
    path('',views.homeView, name='home'),
    path('signup/',views.signupView, name='signup'),
    
]