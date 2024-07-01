from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'address_line_1', 'address_line_2', 'city', 'state', 'country', 'zip_code']
        
        
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['profile_image'].widget.attrs.update({'class': 'form-control d-none' })
        self.fields['address_line_1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Address Line 1'})
        self.fields['address_line_2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Address Line 2'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'placeholder': 'City'})
        self.fields['state'].widget.attrs.update({'class': 'form-control', 'placeholder': 'State'})
        self.fields['country'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Country'})
        self.fields['zip_code'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Zip Code'})
