
from django import forms
from django.core import validators
from recharge_panel_app.models import check_user_exists

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

    user_role =  forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', 'title': 'Select Role'}), required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'title': 'Address'}))
    credit_assigned = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control', 'title': 'Float'}))
    credit_used = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control', 'title': 'Float'}))
    credit_available = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control', 'title': 'Float'}))
    margin = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control', 'title': 'Float'}), required=True)

    def __init__(self, *args, **kwargs):
        user_role = kwargs.pop('user_role')
        print super(CreateUserForms, self).__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['confirm_password'].required = False
        self.fields['user_role'].choices = ((("admin"), ("Admin")), (("distributor"), ("Distributor")),
                                            (("retailer"), ("Retailer")),
        )
        print self.fields['user_role'].choices
        if user_role:
            if user_role == 'distributor':
                  self.fields['user_role'].choices = ((("distributor"), ("Distributor")),
                                            (("retailer"), ("Retailer")),
        )
            elif user_role == 'retailer':
                self.fields['user_role'].choices = (
                                            (("retailer"), ("Retailer")),
        )


    def clean(self):
        # user_already_exists =  check_user_exists({"user_name":self.cleaned_data.get('user_name')})
        # if user_already_exists:
        #     raise forms.ValidationError("User name already exists.")
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        if not password2:
            raise forms.ValidationError("This field is required.")
        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data
