from django import forms
from .models import CompletedTasks, Tasks
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class TasksForm(forms.Form):

    class Meta:
        model = Tasks
        fields = '__all__'


class LoginForm(forms.Form):
	username = forms.CharField(max_length=30)
	password = forms.CharField(widget=forms.PasswordInput)


class SignupForm(UserCreationForm):
	username = forms.CharField(required=True)

	class Meta:
		model = User
		fields = ("username", "first_name", "last_name", "password1", "password2")

	def save(self, commit=True):
		user = super(SignupForm, self).save(commit=False)
		if commit:
			user.save()
		return user



