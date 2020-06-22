from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm, AuthenticationForm

from users.models import Profile


class UserRegisterForm(DjangoUserCreationForm):
    email = forms.EmailField(label='', required=True)
    username = forms.CharField(label='', required=True)

    class Meta(DjangoUserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Password confirmation'


class UserLoginForm(AuthenticationForm):

    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Login'}
    ))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}
    ))


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = self.fields['username'].label or 'Enter username'
        self.fields['email'].widget.attrs['placeholder'] = self.fields['email'].label or 'Enter email'


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True, label='')
    message = forms.CharField(widget=forms.Textarea, required=True, label='')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.user_email = self.user.email
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['from_email'] = forms.EmailField(initial=self.user_email, label='From E-mail:')
        self.fields['subject'].widget.attrs['placeholder'] = 'Subject'
        self.fields['message'].widget.attrs['placeholder'] = 'Please Enter Your Message'
