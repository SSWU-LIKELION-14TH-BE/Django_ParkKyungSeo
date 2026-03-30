from django.urls import path
from .views import signup_view, login_view, logout_view, password_reset_request, password_reset_confirm

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('password-reset/', password_reset_request, name='password_reset'),
    path('password-reset/verify/', password_reset_confirm, name='password_reset_confirm'),
]