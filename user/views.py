import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings
from .forms import SignUpForm
from .models import CustomUser

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
def password_reset_request(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        # 아이디와 이메일이 모두 일치하는 유저 찾기
        user = CustomUser.objects.filter(username=username, email=email).first()
        
        if user:
            auth_code = str(random.randint(100000, 999999))
            request.session['auth_code'] = auth_code
            request.session['reset_user_id'] = user.id
            
            subject = "[서비스명] 비밀번호 재설정 인증번호"
            message = f"요청하신 인증번호는 [{auth_code}] 입니다."
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
            
            return render(request, 'password_reset_verify.html') 
        else:
            return render(request, 'password_reset.html', {'error': '아이디 또는 이메일 정보가 일치하지 않습니다.'})
    return render(request, 'password_reset.html')

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