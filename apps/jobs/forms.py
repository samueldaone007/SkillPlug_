"""
Forms for the jobs app.
"""

from django import forms
from apps.accounts.models import Skill
from .models import Job, Application


class JobPostForm(forms.ModelForm):
    """Form for posting a new job."""
    
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all",
            "placeholder": "e.g., Logo Design for New Restaurant",
        }),
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all resize-none",
            "placeholder": "Describe the project in detail. Include deliverables, timeline, and any specific requirements...",
            "rows": 6,
        }),
    )
    budget_type = forms.ChoiceField(
        choices=Job.BUDGET_TYPE_CHOICES,
        initial="fixed",
        widget=forms.Select(attrs={
            "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all",
        }),
    )
    budget_min = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all",
            "placeholder": "Min budget (NGN)",
        }),
    )
    budget_max = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all",
            "placeholder": "Max budget (NGN)",
        }),
    )
    budget_display = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all",
            "placeholder": "Or enter custom budget text (e.g., ₦5,000 - ₦10,000)",
        }),
    )
    required_skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.filter(is_active=True),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            "class": "form-checkbox h-5 w-5 text-green-600 rounded border-gray-300 focus:ring-green-500",
        }),
    )
    location_preference = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all",
            "placeholder": "e.g., Remote, Lagos, or Any",
        }),
    )
    contact_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all",
            "placeholder": "your@email.com (optional)",
        }),
    )
    contact_whatsapp = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all",
            "placeholder": "2348012345678 (optional)",
        }),
    )
    
    class Meta:
        model = Job
        fields = [
            "title", "description", "budget_type",
            "budget_min", "budget_max", "budget_display",
            "required_skills", "location_preference",
            "contact_email", "contact_whatsapp",
        ]
    
    def clean(self):
        cleaned_data = super().clean()
        budget_min = cleaned_data.get("budget_min")
        budget_max = cleaned_data.get("budget_max")
        
        if budget_min and budget_max and budget_min > budget_max:
            self.add_error("budget_max", "Maximum budget must be greater than minimum budget.")
        
        return cleaned_data


class JobApplicationForm(forms.ModelForm):
    """Form for applying to a job."""
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all resize-none",
            "placeholder": "Explain why you're a great fit for this job. Mention your relevant experience and skills...",
            "rows": 5,
        }),
    )
    proposed_budget = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all",
            "placeholder": "Your proposed budget in NGN (optional)",
        }),
    )
    
    class Meta:
        model = Application
        fields = ["message", "proposed_budget"]
    
    def __init__(self, *args, user=None, job=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.job = job
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Check if user already applied
        if self.user and self.job:
            if Application.objects.filter(student=self.user, job=self.job).exists():
                raise forms.ValidationError("You have already applied for this job.")
        
        return cleaned_data


class JobStatusForm(forms.ModelForm):
    """Form for updating job status (for job poster)."""
    
    status = forms.ChoiceField(
        choices=Job.STATUS_CHOICES,
        widget=forms.Select(attrs={
            "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all",
        }),
    )
    
    class Meta:
        model = Job
        fields = ["status"]
