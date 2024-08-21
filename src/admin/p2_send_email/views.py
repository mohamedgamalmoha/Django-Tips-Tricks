from django.conf import settings
from django.core.mail import send_mail
from django.views.generic.edit import FormView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin

from .forms import SendEmailForm


class SendEmailView(SuccessMessageMixin, FormView):
    """
    A view for sending emails using a form. Displays a success message upon successful submission.
    """
    form_class = SendEmailForm
    success_message = _('Emails are sent successfully')
    success_url = '/'

    def form_valid(self, form):
        """
        Processes the form when valid. Sends emails to the list of users who are not excluded.

        Args:
            - form (SendEmailForm): The form instance with validated data.

        Returns:
            - HttpResponse: The response indicating the form was successfully processed.
        """
        # Get the list of users to email
        users = form.get_users()

        # Extract subject and message from the form's cleaned data
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['body']

        # Set the sender email
        from_email = settings.DEFAULT_FROM_EMAIL

        # Create a list of recipient emails
        recipient_list = [user.email for user in users]

        # Send the email to the recipient list
        send_mail(subject, message, from_email, recipient_list)

        # Return the default form_valid response
        return super().form_valid(form)
