from django.contrib.auth.hashers import make_password
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, UserProfile
                     

class SignupForm(forms.ModelForm):
    
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name','last_name','password')

        widgets = {
            'password': forms.PasswordInput(
                attrs={'placeholder': '***********', 'required': 'required'}),
        }

        labels = {
            'username': _('Username *'),
            'email': _('Email *'),
            'first_name': _('First name *'),
            'last_name': _('Last name *'),
            'password': _('Password *'),
        }

        error_messages = {
            'email': {
                'invalid': _("Please enter a valid email to proceed."),
                'unique': _("Email already exists."),
                'required': _("The email field cannot be empty"),
            },
            'username': {
                'required': _("Username field cannot be empty"),
            },
            'first_name': {
                'required': _("First name field cannot be empty"),
            },
            'last_name': {
                'required': _("Last name field cannot be empty"),
            },
            'password': {
                'required': _("Please provide a password to create an account"),
            }
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        return email.lower()

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is taken, try again.")
        return username
    
    def save(self, commit: True):
        user = super(SignupForm, self).save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):

    error_css_class = 'error'
    required_css_class = 'required'

    username = forms.CharField(
        label='Username *',
        error_messages={'required': _("Please enter a registered username to login")},
    )
    password = forms.CharField(
        label='Password *',
        error_messages={'required': _("Password field cannot be empty")},
        widget=forms.PasswordInput(
            attrs={'placeholder': '************', 'required': 'required'}
        ),
    )

class ProfileForm(forms.ModelForm):

    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = UserProfile
        fields = ('image', 'bio')
        widgets = {
            'image': forms.FileInput(
                attrs={'class': 'hidden', 'x-ref': 'image', 'type': 'file', 'accept': 'image/*',
                       '@change': 'reader = new FileReader();'
                                  'reader.onload = (event) => {'
                                  'imagePreview = event.target.result'
                                  '};'
                                  'reader.readAsDataURL($refs.image.files[0]);'}
            ),
            'bio': forms.Textarea(attrs={
                                        'placeholder': 'e.g. My account bio',
                                         'rows': 3
                                                 }),
        }

        labels = {
            'image': _('Photo *'),
            'bio': _('Bio *')     
        }

    def clean_image(self):
        image = self.cleaned_data.get("image", False)
        if image:
            if image.size > 15 * 1024 * 1024:
                raise forms.ValidationError("Image file too large (must be less than 15mb)")
        return image