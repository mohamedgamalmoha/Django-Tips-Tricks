from django import forms
from django.contrib.auth.backends import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class SendEmailForm(forms.Form):
    """
    Form for sending emails with user exclusion functionality.

    This form is designed to facilitate sending emails, allowing the exclusion of certain users from the recipient
    list. The form includes fields for the email subject, body, and a selection of users to be excluded.
     """
    users_excluded = forms.ModelMultipleChoiceField(
        label=_('Users Excluded'),
        queryset=User.objects.filter(is_superuser=False),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )
    subject = forms.CharField(
        label=_('Subject'),
        max_length=500,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    body = forms.CharField(
        label=_('Body'),
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=True
    )

    def get_users(self):
        """
        Get the list of users excluding the selected ones.

        This method retrieves the list of users who are not selected in the 'users_excluded' field, allowing the
        sender to send the email to everyone except those excluded.

        Returns:
            - QuerySet: A queryset of users that excludes the selected users.
        """
        excluded_ids = self.cleaned_data.get('users_excluded', []).values_list('id', flat=True)
        return self.fields['users_excluded'].queryset.exclude(id__in=excluded_ids)
