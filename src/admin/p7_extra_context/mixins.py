from django.contrib import admin


class AdminContextMixin:
    """
    A mixin for adding extra context to admin views. This mixin ensures that additional context provided via
    `extra_context` is passed to the template context for various admin views.
    """
    extra_context = None

    def get_context_data(self, extra_context=None):
        """
        Updates the context with extra context data if provided.

        - Args:
            - extra_context (dict, optional): Additional context to be merged into the existing context.

        - Returns:
            - dict: The updated context dictionary.
        """
        context = super().get_context_data(extra_context=extra_context)
        if self.extra_context:
            context.update(self.extra_context)
        return context

    @admin.options.csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        """
        Renders the changelist view with additional context.

        - Args:
            - request (HttpRequest): The request object.
            - extra_context (dict, optional): Additional context to pass to the template. Defaults to None.

        - Returns:
            - HttpResponse: The rendered changelist view.
        """
        context = self.get_context_data(extra_context)
        return super().changelist_view(request, context)

    def add_view(self, request, form_url='', extra_context=None):
        """
        Renders the add view with additional context.

        - Args:
            - request (HttpRequest): The request object.
            - form_url (str, optional): The URL for the form submission. Defaults to an empty string.
            - extra_context (dict, optional): Additional context to pass to the template. Defaults to None.

        - Returns:
            - HttpResponse: The rendered add view.
        """
        context = self.get_context_data(extra_context)
        return super().add_view(request, form_url, context)

    def history_view(self, request, object_id, extra_context=None):
        """
        Renders the history view with additional context.

        - Args:
            - request (HttpRequest): The request object.
            - object_id (str): The ID of the object whose history is to be viewed.
            - extra_context (dict, optional): Additional context to pass to the template. Defaults to None.

        - Returns:
            - HttpResponse: The rendered history view.
        """
        context = self.get_context_data(extra_context)
        return super().history_view(request, object_id, context)

    @admin.options.csrf_protect_m
    def delete_view(self, request, object_id, extra_context=None):
        """
        Renders the delete view with additional context.

        - Args:
            - request (HttpRequest): The request object.
            - object_id (str): The ID of the object to be deleted.
            - extra_context (dict, optional): Additional context to pass to the template. Defaults to None.

        - Returns:
            - HttpResponse: The rendered delete view.
        """
        context = self.get_context_data(extra_context)
        return super().delete_view(request, object_id, context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        Renders the change view with additional context.

        - Args:
            - request (HttpRequest): The request object.
            - object_id (str): The ID of the object to be changed.
            - form_url (str, optional): The URL for the form submission. Defaults to an empty string.
            - extra_context (dict, optional): Additional context to pass to the template. Defaults to None.

        - Returns:
            - HttpResponse: The rendered change view.
        """
        context = self.get_context_data(extra_context)
        return super().change_view(request, object_id, form_url, context)
