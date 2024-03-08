from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
]