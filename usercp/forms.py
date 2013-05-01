from django.contrib.auth import forms as auth_forms
from django import forms
from django.contrib.auth.models import User

from captcha.fields import ReCaptchaField


class RegisterForm(auth_forms.UserCreationForm):
    """
    Extends build-in user creation form.
    """

    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError('Username must have at least 3 characters (it has %i).' % len(username))
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('Email address already exists.')
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError('Password must have at least 8 characters (it has %i).' % len(password1))
        return password1

    def save(self, commit=True):
        user = super(auth_forms.UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user


class AccountUpdateForm(auth_forms.UserChangeForm):
    """
    Extends build-in user change form.
    """

    new_password1 = forms.CharField(label='Password', min_length=8, widget=forms.PasswordInput(), required=False)
    new_password2 = forms.CharField(label='Password conformation', min_length=8, widget=forms.PasswordInput(),
                                    required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'new_password1', 'new_password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError('Username must have at least 3 characters (it has %i).' % len(username))
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if self.changed_data and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('Email address already exists.')
        return email

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 != new_password2:
            raise forms.ValidationError('The passwords don\'t match.')
        return new_password2

    # 'password' field exclude bug hack
    def __init__(self, *args, **kwargs):
        super(AccountUpdateForm, self).__init__(*args, **kwargs)
        del self.fields['password']

    def save(self, commit=True):
        user = super(auth_forms.UserChangeForm, self).save(commit=False)
        if self.cleaned_data.get('new_password1'):
            user.set_password(self.cleaned_data.get('new_password1'))
        if commit:
            user.save()
        return user
