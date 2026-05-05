import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError, PermissionDenied
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.contrib import messages
from .forms import UserUpdateForm, SignUpForm, PostForm
from .models import CustomUser, Post, Comment
from django.contrib.auth.decorators import login_required


# 1. 홈 화면
def home_view(request):
    return render(request, 'home.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

# 이메일 발송을 위한 함수 추가
def password_reset_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(username=username, email=email)
            auth_code = str(random.randint(100000, 999999))
            request.session['auth_code'] = auth_code
            request.session['reset_user_id'] = user.id
            send_mail(
                '비밀번호 재설정 인증번호입니다.',
                f'인증번호는 [{auth_code}] 입니다.',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return redirect('password_reset_verify')
        except CustomUser.DoesNotExist:
            return render(request, 'password_reset.html', {'error': '일치하는 유저가 없습니다.'})
    return render(request, 'password_reset.html')

def password_reset_confirm(request):
    if request.method == 'POST':
        input_code = request.POST.get('auth_code')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password != confirm_password:
            return render(request, 'password_reset_verify.html', {'error': '새 비밀번호가 서로 일치하지 않습니다.'})
        
        if input_code == request.session.get('auth_code'):
            user_id = request.session.get('reset_user_id')
            try:
                user = CustomUser.objects.get(id=user_id)
                validate_password(new_password, user=user)
                user.set_password(new_password)
                user.save()
                
                del request.session['auth_code']
                del request.session['reset_user_id']
                return redirect('login')
            except (CustomUser.DoesNotExist, ValidationError) as e:
                error_msg = e.messages if hasattr(e, 'messages') else '오류가 발생했습니다.'
                return render(request, 'password_reset_verify.html', {'error': error_msg})
        else:
            return render(request, 'password_reset_verify.html', {'error': '인증번호가 일치하지 않습니다.'})
            
    return render(request, 'password_reset_verify.html')

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})

@require_POST
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', pk=pk)

@require_POST
def comment_like(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    # comment.post.pk를 사용하여 해당 게시글 상세 페이지로 돌아갑니다.
    return redirect('post_detail', pk=comment.post.pk)

def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        
        if parent_id:
            parent_comment = get_object_or_404(Comment, id=parent_id)
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content,
                parent=parent_comment
            )
        else:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
    return redirect('post_detail', pk=pk)

# 게시물 검색/정렬 기능
def post_list(request):
    search_query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'latest')
    posts = Post.objects.annotate(likes_count=Count('likes')).prefetch_related('tech_stacks', 'author').all()

    #검색 필터링
    if search_query:
        posts = posts.filter(title__icontains=search_query)
        
    # 게시물 정렬
    if sort_by == 'popular':
        # 인기순: 좋아요 많은 순 -> 최신순
        posts = posts.order_by('-likes_count', '-created_at')

    else:
        # 최신순 (기본값)
        posts = posts.order_by('-created_at')

        
    context = {
        'posts': posts,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'post_list.html', context)

# 게시물 상세 페이지
def post_detail(request, pk):
    post = get_object_or_404(
        Post.objects.prefetch_related(
            'comments__replies', 
            'comments__author', 
            'comments__replies__author',
            'tech_stacks'
        ), 
        pk=pk
    )
    
    # 조회수 증가 로직 추가
    post.views += 1
    post.save(update_fields=['views'])
    
    return render(request, 'post_detail.html', {'post': post})

@login_required
def mypage_view(request):
    user_form = UserUpdateForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)

    my_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    
    if request.method == 'POST':
        # 회원정보 수정 처리
        if 'update_info' in request.POST:
            user_form = UserUpdateForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, '회원 정보가 수정되었습니다.')
                return redirect('mypage')
        
        # 비밀번호 변경 처리 (보안 강화)
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                # 비밀번호 변경 후 세션 무효화 방지
                update_session_auth_hash(request, user)
                messages.success(request, '비밀번호가 성공적으로 변경되었습니다.')
                return redirect('mypage')
            else:
                messages.error(request, '비밀번호 변경에 실패했습니다. 규칙을 확인해주세요.')

        

    return render(request, 'mypage.html', {
        'user_form': user_form,
        'password_form': password_form,
        'my_posts': my_posts
    })

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        raise PermissionDenied # 작성자가 아니면 403 에러 처리

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form})


# 게시글 삭제
@require_POST
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        raise PermissionDenied
        
    post.delete()
    messages.success(request, "게시물이 삭제되었습니다.")
    return redirect('post_list')