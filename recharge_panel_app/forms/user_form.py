
from django import forms
from django.core import validators


class CreateUserForms(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'title': 'User Name'}),
                                required=True)
    email_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'title': 'Email-ID'}),
                               required=True,
                               validators=[validators.validate_email])
    mobile_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'title': 'Mobile Number'}),
                                    min_length=10,
                                    max_length=12,
                                    required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'title': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                         'title': 'Confirm Password'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'title': 'Address'}))

    def clean(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        email = self.clean_data.get('email_id', '')
        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data
