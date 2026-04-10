# bank_app/forms.py
from django import forms
from .models import BankApplication

class BankApplicationForm(forms.ModelForm):
    agree_terms = forms.BooleanField(required=True, label="I agree to the Terms and Conditions")
    
    class Meta:
        model = BankApplication
        fields = '__all__'
        widgets = {
            'nominee_dob': forms.DateInput(attrs={'type': 'date'}),
            'address_line': forms.Textarea(attrs={'rows': 2}),
        }