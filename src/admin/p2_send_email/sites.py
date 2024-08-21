from django.urls import path
from django.contrib.admin import AdminSite
from django.utils.functional import LazyObject

from .views import SendEmailView


class CustomAdminSite(AdminSite):
    """
    A custom AdminSite class that includes a view for sending emails.
    """
    final_catch_all_view = False

    def send_email_view(self, request, extra_context=None):
        """
        A view to handle sending emails, using the 'SendEmailView' class-based view.

        Args:
            - request (HttpRequest): The current request object.
            - extra_context (dict, optional): Additional context to pass to the view. Defaults to None.

        Returns:
            - HttpResponse: The rendered view response.
        """
        # Combine the default context with any extra context provided
        context = {**self.each_context(request), **(extra_context or {})}

        # Set the current app to ensure correct template rendering
        request.current_app = self.name

        # Return the SendEmailView response with the combined context
        return SendEmailView.as_view(extra_context=context, template_name='admin/send_email.html')(request)

    def get_urls(self):
        """
        Extend the default admin URLs with custom URLs.

        Returns:
            - list: The updated list of urlpatterns.
        """
        # Retrieve the default admin URLs
        urlpatterns = super().get_urls()

        # Add a custom URL pattern for the send email view
        custom_urls = [
            path("send-email/", self.send_email_view, name="send_email"),
        ]

        # Combine default and custom URLs
        return urlpatterns + custom_urls


class DefaultAdminSite(LazyObject):
    """
    A lazy-loaded default admin site that wraps around the CustomAdminSite.
    """

    def _setup(self):
        """
        Initialize the CustomAdminSite instance.
        """
        self._wrapped = CustomAdminSite()

    def __repr__(self):
        """
        Provide a string representation of the wrapped object.
        """
        return repr(self._wrapped)


# Instantiate the default admin site using the lazy-loaded wrapper
admin_site = DefaultAdminSite()
