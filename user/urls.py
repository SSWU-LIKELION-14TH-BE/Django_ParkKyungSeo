from django.urls import path
from . import views # 모든 뷰를 한꺼번에 가져옵니다.

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('password-reset/verify/', views.password_reset_confirm, name='password_reset'), 

    # --- 게시글 관련 경로 ---
    path('posts/', views.post_list, name='post_list'),
    path('posts/new/', views.post_create, name='post_create'),
]
