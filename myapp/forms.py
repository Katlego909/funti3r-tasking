from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ticket

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    username = forms.CharField(max_length=150)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Email'}),
            'username': forms.TextInput(attrs={'placeholder': 'Choose Username'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        }

        for field_name, widget in widgets.items():
            self.fields[field_name].widget = widget

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'status', 'priority', 'customer_name', 'customer_email']

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'rows': 5})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        self.fields['priority'].widget.attrs.update({'class': 'form-control'})
        self.fields['customer_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['customer_email'].widget.attrs.update({'class': 'form-control'})

