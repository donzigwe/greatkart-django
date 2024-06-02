from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password Again',
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = "Enter First Name"
        self.fields['last_name'].widget.attrs['placeholder'] = "Enter Last Name"
        self.fields['email'].widget.attrs['placeholder'] = "Enter Email Address"
        self.fields['phone_number'].widget.attrs['placeholder'] = "Enter Valid Phone Number"
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"

    def clean(self):
        clean_data = super(RegistrationForm, self).clean()
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Passwords does not match!'
            )


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Enter Email', 'class': 'form-control',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password', 'class': 'form-control',
    }))

class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password', 'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password Again', 'class': 'form-control',
    }))

    def clean(self):
        clean_data = super(ResetPasswordForm, self).clean()
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Passwords does not match!'
            )


class ForgotPasswordForm1(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Enter Email', 'class': 'form-control',
    }))


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Current Password', 'class': 'form-control',
    }))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter New Password', 'class': 'form-control',
    }))
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter New Password Again', 'class': 'form-control',
    }))

    def clean(self):
        clean_data = super(ChangePasswordForm, self).clean()
        new_password = clean_data.get('new_password')
        confirm_new_password = clean_data.get('confirm_new_password')

        if new_password != confirm_new_password:
            raise forms.ValidationError(
                'Passwords does not match!'
            )