from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


class SearchForm(forms.Form):
    q = forms.CharField(label='', max_length=255, required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Search'}))


class UserInfoForm(forms.ModelForm):
    phone_number = forms.CharField(label='', max_length=10, required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}))
    email = forms.EmailField(label='', required=False, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    address1 = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 1'}))
    address2 = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 2'}))
    
    class Meta:
        model = Profile
        fields = ['phone_number', 'email', 'address1', 'address2']


class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_assword2']
        widgets = {
            'new_password1': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}),
            'new_password2': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class':'form-control form-control-lg', 'placeholder':'Password', 'autofocus':True})
        self.fields['new_password2'].widget.attrs.update({'class':'form-control form-control-lg', 'placeholder':'Confirm Password'})
        self.fields['new_password1'].label = ''
        self.fields['new_password2'].label = ''
        self.fields['new_password1'].help_text = '''
            <small class="form-text text-muted">
                Your password must be at least 8 characters long and contain at least one uppercase letter,
                one lowercase letter, and one digit.
            </small>
        '''


class UpdateUserform(UserChangeForm):
	password = None
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), required=False)
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), required=False)
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), required=False)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')	

	def __init__(self, *args, **kwargs):
		super(UpdateUserform, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'User Name'})
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'User Name'})
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': "Confirm Password"})
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email