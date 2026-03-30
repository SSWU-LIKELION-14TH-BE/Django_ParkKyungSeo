import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings

# 로컬 파일 import
from .forms import SignUpForm
from .models import CustomUser

# 1. 회원가입
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('signup') # 성공 후 이동할 페이지
        else:
            print(form.errors)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# 2. 로그인
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('signup')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# 3. 로그아웃
def logout_view(request):
    logout(request)
    return redirect('signup')

# 4. 인증번호 이메일 발송
def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()
        
        if user:
            # 6자리 랜덤 인증번호 생성
            auth_code = str(random.randint(100000, 999999))
            
            # 세션에 인증번호와 이메일 저장 (5분 유효 등 설정 가능)
            request.session['auth_code'] = auth_code
            request.session['reset_email'] = email
            
            subject = "[서비스명] 비밀번호 재설정 인증번호"
            message = f"인증번호는 [{auth_code}] 입니다."
            
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
            
            # 인증번호 입력 페이지로 이동
            return render(request, 'password_reset_verify.html') 
        else:
            return render(request, 'password_reset.html', {'error': '등록되지 않은 이메일입니다.'})
    return render(request, 'password_reset.html')

# 5. 인증번호 확인 및 새 비밀번호 설정
def password_reset_confirm(request):
    if request.method == 'POST':
        input_code = request.POST.get('auth_code')
        new_password = request.POST.get('new_password')
        
        # 세션의 인증번호와 대조
        if input_code == request.session.get('auth_code'):
            email = request.session.get('reset_email')
            user = CustomUser.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            
            # 세션 비우기
            del request.session['auth_code']
            del request.session['reset_email']
            
            return redirect('login')
        else:
            return render(request, 'password_reset_verify.html', {'error': '인증번호가 일치하지 않습니다.'})
    return render(request, 'password_reset_verify.html')