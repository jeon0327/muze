from django import forms
from .models import Concert
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review
from collections import OrderedDict

class UserForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=True, error_messages={'required': '이름을 입력해주세요.'})
    username = forms.CharField(required = True, error_messages={'required': '아이디를 입력해주세요.'})
    email = forms.EmailField(required=True, error_messages={'required': '이메일을 입력해주세요.'})
    rrn = forms.CharField(max_length=13, required=True, error_messages={'required': '주민등록번호를 입력해주세요.'})
    password1 = forms.CharField(required = True, widget=forms.PasswordInput, error_messages = {'required': '비밀번호를 입력해주세요.'})
    password2 = forms.CharField(required = True, widget=forms.PasswordInput, error_messages = {'required': '비밀번호 확인을 입력해주세요.'})

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")
        labels = {
            'username': '',
        }
        error_messages = {
            'username': {
                'unique': "이미 사용 중인 ID입니다.",
            },
            'rrn': "이미 등록된 주민등록번호입니다."
        }

    def clean_rrn(self):
        rrn = self.cleaned_data['rrn']
        if not rrn.isdigit():
            raise forms.ValidationError("주민등록번호는 숫자만 입력해야 합니다.")
        if len(rrn) != 13:
            raise forms.ValidationError("주민등록번호는 13자리여야 합니다.")
        return rrn
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError("비밀번호는 8자리 이상이여야 합니다.")
        return password1
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields = OrderedDict([
            ('name', self.fields['name']),
            ('username', self.fields['username']),
            ('password1', self.fields['password1']),
            ('password2', self.fields['password2']),
            ('email', self.fields['email']),
            ('rrn', self.fields['rrn']),
        ])


class ConcertForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = ['title', 'date', 'location', 'price', 'poster', 'description_image', 'lineup', 'rating', 'runtime', 'performance_times']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'rating', 'content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,  # 줄 수만 조절
            }),
        }
