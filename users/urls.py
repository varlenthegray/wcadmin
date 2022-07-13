from django.urls import path
from . import views


urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('profile', views.Profile.as_view(), name='profile'),
    path('change_theme', views.change_theme, name='changeTheme'),
]
