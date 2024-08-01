# accounts/urls.py
 
from django.urls import path
from . import views
app_name = 'personaccounts'
urlpatterns = [
    path('sign/', views.sign, name='sign'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('register/',views.register, name = 'register'),
]