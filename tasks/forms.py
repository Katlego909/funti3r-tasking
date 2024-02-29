from .models import Task, Application
from django import forms

class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'short_description', 'long_description', 'amount', 'company_name', 'company_address', 'company_zipcode', 'company_location',  'company_country', 'company_size', 'company_website','company_logo','image', 'attached_file', 'status', "category", "experience",]

        # Add this method to handle image upload
    def save(self, commit=True):
        task = super().save(commit=False)

        # Check if 'image' key is in cleaned_data
        if 'image' in self.cleaned_data:
            task.image = self.cleaned_data['image']

        if commit:
            task.save()
        return task

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'experience', 'email', 'linkedin_profile','resume']

class TaskSearchForm(forms.Form):
    search_short_description = forms.CharField(label='Search for task', required=False)