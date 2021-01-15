from django import forms


class UserRegisterForm(forms.Form):
  email = forms.EmailField()
  username = forms.CharField(max_length=200)
  password1 = forms.CharField(widget=forms.PasswordInput())
  password2 = forms.CharField(widget=forms.PasswordInput())





class UserLoginForm(forms.Form):

  username = forms.CharField(max_length=200)
  password = forms.CharField(widget=forms.PasswordInput())
