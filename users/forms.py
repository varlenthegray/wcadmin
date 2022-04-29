from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=50, required=True)
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class ProfileForm(forms.ModelForm):
    password_2 = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password_2']
        widgets = {
            'password': forms.PasswordInput(),
            'password_2': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")

        if password != password_2:
            raise forms.ValidationError("Password and confirm password do not match.")
