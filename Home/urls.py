
from django.urls import path
from .views import login_page,oauth2callback,get_data
urlpatterns = [
    path('login/',login_page,name="login"),
    path('oauth2callback',oauth2callback,name="oauthcallback"),
    path('',get_data,name="home")
    
]
