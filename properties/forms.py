from django import forms
from .models import Property, UserPreference

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'location', 'property_type', 'price', 'area', 'images']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'property_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control'}),
            'images': forms.FileInput(attrs={'class': 'form-control'})
        }
        
class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ['location', 'property_type', 'min_price', 'max_price']
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'property_type': forms.Select(attrs={'class': 'form-control'}),
            'min_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_price': forms.NumberInput(attrs={'class': 'form-control'})
        }