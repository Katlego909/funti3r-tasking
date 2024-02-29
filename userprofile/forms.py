from django import forms
from .models import Userprofile
from tasks.models import Task, Category

class UserProfileForm(forms.ModelForm):

    industry = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)

    class Meta:
        model = Userprofile
        fields = ['is_company', 'profile_picture', 'username', 'email', 'cell_number', 'bio', 'industry']
        widgets = {
            'is_company': forms.CheckboxInput(attrs={'placeholder': 'Is Company'}),
            'profile_picture': forms.FileInput(attrs={'placeholder': 'Profile Picture'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'cell_number': forms.TextInput(attrs={'placeholder': 'Cell Number'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Bio'}),
            'industry': forms.TextInput(attrs={'placeholder': 'Industry'}),
        }