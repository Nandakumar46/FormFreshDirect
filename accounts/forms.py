# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class SignUpForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('FARMER', 'I am a Farmer'),
        ('CLIENT', 'I am a Client'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True, widget=forms.RadioSelect)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Update the profile created by the signal
            user.profile.user_type = self.cleaned_data['user_type']
            user.profile.save()
        return user