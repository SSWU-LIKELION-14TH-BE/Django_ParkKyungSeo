from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # 1단계: 이메일 입력 페이지
    path('password-reset/', views.password_reset_view, name='password_reset'),
    
    # 2단계: 인증번호 및 새 비밀번호 입력 페이지
    path('password-reset/verify/', views.password_reset_confirm, name='password_reset_verify'),


    # --- 게시글 관련 경로 ---
    path('posts/', views.post_list, name='post_list'),
    path('posts/new/', views.post_create, name='post_create'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),

    path('posts/<int:pk>/like/', views.post_like, name='post_like'),
    path('posts/<int:pk>/comment/', views.comment_create, name='comment_create'),
    path('comments/<int:pk>/like/', views.comment_like, name='comment_like'),
    path('mypage/', views.mypage_view, name='mypage'),
    path('post/<int:pk>/update/', views.post_update, name='post_update'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
 
    path('guestbook/<str:username>/', views.guestbook_view, name='guestbook'),
]
