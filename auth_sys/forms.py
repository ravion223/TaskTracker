from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import CommonPasswordValidator

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError(_('Please enter a username'))
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if not password1:
            raise ValidationError(_('Please enter a password'))
        # Check if the password is too common
        common_validator = CommonPasswordValidator()
        common_validator.validate(password1)
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 == password2:
            return cleaned_data
        raise ValidationError(_('The passwords do not match'))
