from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import TrelloUser
from django.contrib.auth import get_user_model


class TrelloUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        # field_classes = {"username": UsernameField}
    
    def save(self, commit=True):
        user = super(TrelloUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()

        return user


