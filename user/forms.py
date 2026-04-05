from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Post

class SignUpForm(UserCreationForm):
    email = forms. EmailField(required=True) # 이메일 필수
    nickname = forms.CharField(required=True)


    class Meta(UserCreationForm.Meta): # Meta도 상속받는 것이 좋습니다.
        model = CustomUser
        # password1, password2는 UserCreationForm이 알아서 처리하므로 fields에 명시하지 않아도 됩니다.
        fields = ('username', 'nickname', 'email', 'phone_number')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image'] # 유저가 입력할 항목