
from . import views
from django.urls import path
urlpatterns = [
    path('',views.homeView, name='home'),
    path('signup/',views.signupView, name='signup'),
    path('accounts/login/',views.loginView, name='login'),
    path('logout/',views.log_out,name="logout"),
]