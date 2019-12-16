from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ChangeUserDetailsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',]


class NewUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True,
            label='Email Address',
            error_messages={'exists': 'Sorry. An account attached to this email address already exists.'},
            help_text='A valid email address')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")        

    def save(self, commit=True):
        user = super(NewUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise ValidationError(self.fields['email'].error_messages['exists'])
        return self.cleaned_data['email']