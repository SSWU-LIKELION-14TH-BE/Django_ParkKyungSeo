from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
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

# 4. 비밀번호 찾기 및 변경 (단순 아이디 매칭 방식)
def password_reset_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        try:
            user = CustomUser.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return redirect('login')
        except CustomUser.DoesNotExist:
            return render(request, 'password_reset.html', {'error': '일치하는 아이디가 없습니다.'})
    return render(request, 'password_reset.html')