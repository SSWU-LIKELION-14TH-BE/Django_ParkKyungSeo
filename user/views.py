import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings
from .forms import SignUpForm, PostForm
from .models import CustomUser, Post
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


# 0. 홈 화면 (로그인 여부에 따라 버튼 분기)
def home_view(request):
    return render(request, 'home.html')

# 1. 회원가입 (로그인 버튼 삭제는 template에서 처리)
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home') # 회원가입 후 홈으로
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# 2. 로그인 (성공 시 홈으로 이동)
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home') # 로그인 후 홈으로
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# 3. 로그아웃
def logout_view(request):
    logout(request)
    return redirect('home')

# 4. 비밀번호 재설정 요청 (아이디 + 이메일 일치 확인)
def password_reset_confirm(request):
    if request.method == 'POST':
        input_code = request.POST.get('auth_code')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # 1. 비밀번호 일치 여부 확인
        if new_password != confirm_password:
            return render(request, 'password_reset_verify.html', {'error': '새 비밀번호가 서로 일치하지 않습니다.'})
        
        # 2. 인증번호 확인
        if input_code == request.session.get('auth_code'):
            user_id = request.session.get('reset_user_id')
            user = CustomUser.objects.get(id=user_id)
            
            # [수정된 부분] Django 보안 규칙에 따라 비밀번호 검사
            try:
                validate_password(new_password, user=user)
            except ValidationError as e:
                # 규칙에 어긋나면 에러 메시지(예: 너무 짧음, 너무 쉬움 등)를 화면에 전달
                return render(request, 'password_reset_verify.html', {'error': e.messages})

            # 검사를 통과했을 때만 저장
            user.set_password(new_password)
            user.save()
            
            del request.session['auth_code']
            del request.session['reset_user_id']
            return redirect('login')
        else:
            return render(request, 'password_reset_verify.html', {'error': '인증번호가 일치하지 않습니다.'})
    return render(request, 'password_reset_verify.html')

# 5. 인증번호 및 새 비밀번호 확인 (비밀번호 재확인 로직 추가)
def password_reset_confirm(request):
    if request.method == 'POST':
        input_code = request.POST.get('auth_code')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # 1. 비밀번호 일치 여부 확인
        if new_password != confirm_password:
            return render(request, 'password_reset_verify.html', {'error': '새 비밀번호가 서로 일치하지 않습니다.'})
        
        # 2. 인증번호 확인
        if input_code == request.session.get('auth_code'):
            user_id = request.session.get('reset_user_id')
            user = CustomUser.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()
            
            del request.session['auth_code']
            del request.session['reset_user_id']
            return redirect('login')
        else:
            return render(request, 'password_reset_verify.html', {'error': '인증번호가 일치하지 않습니다.'})
    return render(request, 'password_reset_verify.html')



# 게시글 목록
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'post_list.html', {'posts': posts})

# 게시글 작성
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES) # 사진 파일 처리를 위해 request.FILES 필요
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user # 로그인한 유저를 작성자로 저장
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})