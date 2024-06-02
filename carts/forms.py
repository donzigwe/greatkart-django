from django import forms


class BillingForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'First Name', 'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Last Name', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email', 'class': 'form-control'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Phone Number', 'class': 'form-control'}))
    address_line_1 = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Address Line 1', 'class': 'form-control'}))
    address_line_2 = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Address Line 2', 'class': 'form-control'}))
    city = forms.ChoiceField(widget=forms.TextInput(attrs={
        'placeholder': 'City', 'class': 'form-control'}))
    state = forms.ChoiceField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'State', 'class': 'form-control'}))
    country = forms.ChoiceField(widget=forms.Select(attrs={
        'placeholder': 'Country', 'class': 'form-control'}))
    order_note = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Order Note', 'class': 'form-control', 'rows': 2}))