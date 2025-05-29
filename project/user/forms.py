from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Подтвердите пароль")

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password_confirm'):
            self.add_error('password_confirm', 'Пароли не совпадают')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # хешируем пароль
        if commit:
            user.save()
        return user
    
    
class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
