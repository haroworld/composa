from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, ValidationError
from .models import Message, User

class RegisterForm(UserCreationForm):

    error_messages = {
            "password_mismatch": ("The two password fields didn't match."),
        }

    class Meta:
        model = User
        fields = ['name','email','username','bio','location','dob','profile_image','password1','password2']


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch'
            )
        return password2

    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'w-full focus:outline-none border-none focus-none'})
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter name : Surname First'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['bio'].widget.attrs.update({'placeholder': 'Details about you'})
        self.fields['bio'].widget.attrs.update({'class': 'no-resize w-full focus:outline-none border-none focus-none'})
        self.fields['location'].widget.attrs.update({'placeholder': 'Your Location'})
        self.fields['dob'].widget.attrs.update({'placeholder': 'yyyy:mm:dd'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter password'})
        self.fields['password1'].widget.attrs.update({'id': 'show-password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'confirm password'})
        self.fields['password2'].widget.attrs.update({'id': 'show-password2'})
        self.fields['profile_image'].widget.attrs.update({'class':'hidden'})
        self.fields['profile_image'].widget.attrs.update({'id':'profile_image'})

class EditProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['name','username','bio','location','dob','profile_image']

    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'w-full focus:outline-none border-none focus-none'})
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter name : Surname First'})
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['bio'].widget.attrs.update({'placeholder': 'Details about you'})
        self.fields['bio'].widget.attrs.update({'class': 'no-resize w-full focus:outline-none border-none focus-none'})
        self.fields['location'].widget.attrs.update({'placeholder': 'Your Location'})
        self.fields['dob'].widget.attrs.update({'placeholder': 'yyyy-mm-dd'})
        self.fields['profile_image'].widget.attrs.update({'class':'hidden'})
        self.fields['profile_image'].widget.attrs.update({'id':'profile_image'})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body','image']

    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        
        self.fields['body'].widget.attrs.update({'placeholder':'Write Message','rows':1})
        self.fields['body'].label = ""
        self.fields['image'].label = ""
        self.fields['body'].widget.attrs.update({'class':'w-full bg-darkBlue focus:outline-none text-white no-resize over-hidden'})
        self.fields['image'].widget.attrs.update({'class':'hidden'})
        self.fields['image'].widget.attrs.update({'id':'image'})