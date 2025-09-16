from django import forms
from accounts.models import MyUser as User

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 'profile_picture', 'phone_number', 'gender', 'location', 'bio']

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error("confirm_password", "Password and Confirm Password do not match")

        if password and len(password) < 8:
            self.add_error("password", "Password must be at least 8 characters long.")

        if password and not any(char.isdigit() for char in password):
            self.add_error("password", "Password must contain at least one numeral.")

        if password and not any(char.isalpha() for char in password):
            self.add_error("password", "Password must contain at least one letter.")

        if password and not any(char.isupper() for char in password):
            self.add_error("password", "Password must contain at least one uppercase letter.")

        if User.objects.filter(username=cleaned_data.get('username')).exists():
            self.add_error("username", "Username already exists.")

        if User.objects.filter(email=cleaned_data.get('email')).exists():
            self.add_error("email", "Email already registered.")

        return cleaned_data
    

class UserSignInForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)
        if not User.objects.filter(username=username).exists():
            self.add_error("username", "Username does not exist.")
        elif user is None:
            self.add_error("password", "Incorrect password.")
        self._user = user
        return cleaned_data

    def get_user(self):
        return getattr(self, '_user', None)

    