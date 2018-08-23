from django.contrib.auth.models import User
from watcha.models import Comment, Score
from django import forms


def min_length_3_validator(value):
    if len(value) < 3:
        raise forms.ValidationError('3글자 이상 입력하세요.')


class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.TextInput({"placeholder": "자유롭게 코멘트를 입력하세요 :)"}))

    class Meta:
        model = Comment
        fields = ['comment', ]


class ScoreForm(forms.ModelForm):
    star = forms.CharField(widget=forms.TextInput(attrs={'id': 'star_score'}))

    class Meta:
        model = Score
        fields = ['star', ]


class UserForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput({"placeholder": "이메일"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'username_pw', 'placeholder': '비밀번호'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'id': 'username_id', 'placeholder': '아이디'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput({"placeholder": "아이디"}))
    password = forms.CharField(widget=forms.PasswordInput({"placeholder": "비밀번호"}))

    class Meta:
        model = User
        fields = ['username', 'password']
