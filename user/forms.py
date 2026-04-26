from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Post,  TechStack

class SignUpForm(UserCreationForm):
    email = forms. EmailField(required=True) # 이메일 필수
    nickname = forms.CharField(required=True)


    class Meta(UserCreationForm.Meta): # Meta도 상속
        model = CustomUser
        # password1, password2는 UserCreationForm이 알아서 처리하므로 fields에 명시x
        fields = ('username', 'nickname', 'email', 'phone_number')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'tech_stacks', 'github_url']
        widgets = {
            'tech_stacks': forms.CheckboxSelectMultiple(), # 체크박스 형태로 표시
            'github_url': forms.URLInput(attrs={'placeholder': 'https://github.com/username/repo'}),
        }


