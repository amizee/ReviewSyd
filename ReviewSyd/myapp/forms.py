from django import forms
from django.core.exceptions import ValidationError

class EmailForm(forms.Form):
    email = forms.EmailField(
        required=True,
        error_messages={
            'required': 'This is not a valid email address.',
            'invalid': 'This is not a valid email address.'
        }
    )

class PasswordResetForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        error_messages={
            'required': 'Password cannot be empty.'
        }
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        error_messages={
            'required': 'Password cannot be empty.'
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password:
            if new_password != confirm_password:
                raise ValidationError("Passwords do not match.")

        return cleaned_data
