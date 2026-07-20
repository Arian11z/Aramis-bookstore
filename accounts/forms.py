from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'ایمیل'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'نام کاربری'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'رمز عبور'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'تکرار رمز عبور'
        })
        
        self.fields['username'].help_text = 'حداکثر 150 کاراکتر. فقط حروف، اعداد و @/./+/-/_ مجاز است.'
        self.fields['password1'].help_text = 'رمز عبور باید حداقل 8 کاراکتر باشد.'
        self.fields['password2'].help_text = 'رمز عبور را دوباره وارد کنید.'


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'نام کاربری'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'رمز عبور'
        })
    )