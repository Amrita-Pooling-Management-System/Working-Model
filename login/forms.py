from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
CATEGORIES = (
        ('STUD','Student'),
        ('DRIV','Driver'),
    )
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,help_text='First Name')
    last_name = forms.CharField(max_length=100,help_text='Last Name')
    email = forms.EmailField(max_length=150,help_text='Email')
    phone = forms.CharField(max_length=10,help_text='Contact Number')
    category = forms.ChoiceField(choices=CATEGORIES,required=True)
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')
    def __init__(self, *args, **kwargs):
    
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'sign-control'
        self.fields['password1'].widget.attrs['class'] = 'sign-control'
        self.fields['password2'].widget.attrs['class'] = 'sign-control'