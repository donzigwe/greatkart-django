from django import forms


class OrderForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'First Name', 'class': 'form-control', 'name:': 'first_name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Last Name', 'class': 'form-control', 'name:': 'last_name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email', 'class': 'form-control', 'name:': 'email'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Phone Number', 'class': 'form-control', 'name:': 'phone_number'}))
    address_line_1 = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Address Line 1', 'class': 'form-control', 'name:': 'address_line_1'}))
    address_line_2 = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Address Line 2', 'class': 'form-control', 'name:': 'address_line_2'}))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'City', 'class': 'form-control', 'name:': 'city'}))
    state = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'State', 'class': 'form-control', 'name:': 'state'}))
    country = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Country', 'class': 'form-control', 'name:': 'country'}))
    order_note = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'placeholder': 'Order Note', 'class': 'form-control', 'rows': 2, 'name:': 'order_note'}))