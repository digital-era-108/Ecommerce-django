from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.RegisterationView.as_view(), name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.SignoutView.as_view(), name='signout'),
]
