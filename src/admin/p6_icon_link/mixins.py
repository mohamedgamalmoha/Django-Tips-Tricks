from django.db import models
from django.utils.safestring import mark_safe


class URLFieldShowLinkAdminMixin:
    """
    A mixin for adding icon links to URL fields in Django admin. This mixin provides methods to automatically replace
    URL fields in the Django admin list display with clickable icons. It maps certain field names to specific icons and
    allows for customization of the icon displayed next to a URL. The mixin works by overriding the  `get_list_display`
    method to include a custom display function for URL fields, which  renders an HTML link with an icon based on the
    field's name.
    """
    #: This dictionary maps field names to icon names, it`s used to customize the icons displayed in the admin list display.
    field_icon_map = {
        'video': 'youtube',
    }

    def get_field_icon_name(self, field_name: str) -> str:
        """
        Retrieves the icon name for a given field name.

        Args:
            - field_name (str): The name of the field for which to get the icon name.

        Returns:
            - str: The name of the icon associated with the field name, or the field name itself if no specific icon is
              mapped.
        """
        return self.field_icon_map.get(field_name, field_name)

    def get_url_fields(self) -> tuple:
        """
        Identifies URL fields in the model associated with this admin.

        This method iterates over all fields of the model and selects those that are instances
        of `URLField`.

        Returns:
            - tuple: A tuple containing the names of all URL fields in the model.
        """
        return tuple(field.name for field in self.model._meta.fields if isinstance(field, models.URLField))

    def create_url_field_display_func(self, field_name: str):
        """
        Creates a function to display a URL field with an associated icon in the admin list.

        Args:
            - field_name (str): The name of the URL field for which to create the display function.

        Returns:
            - function: A function that takes an object as its only argument and returns HTML code to display the URL
              field value with an icon link.
        """
        # Define the display function that will be used in admin list display
        def url_field_display_func(obj):
            # Retrieve the URL from the object using the field name
            url = getattr(obj, field_name)
            # Determine the icon name based on the field name, using a predefined mapping
            icon = self.get_field_icon_name(field_name)
            # Generate and return the HTML string with the icon link
            return mark_safe(f"""<a href="{url}" title="{icon} link"><i class="fab fa-{icon}"></i></a>""")

        # Return the dynamically generated function
        return url_field_display_func

    def get_list_display(self, request) -> list:
        """
        Overrides the Django admin's `get_list_display` method to include custom display functions for URL fields.

        This method extends the base implementation by checking if any of the fields in the
        original `list_display` are URL fields and, if so, replaces them with a custom function
        that renders the URL as an icon link.

        Args:
            - request: The HTTP request object.

        Returns:
            - list: A list of field names or custom display functions to be used in the admin list display.
        """
        # Inherits the base implementation of `get_list_display` to start with the default list display configuration.
        list_display = super().get_list_display(request)

        # Retrieves a tuple of all URL field names in the model by calling `get_url_fields`.
        url_fields = self.get_url_fields()

        # Initializes an empty list to hold the updated list display configuration.
        updated_list_display = []

        # Iterates over each field name in the original `list_display`.
        for field_name in list_display:
            # Checks if the current field name is one of the URL fields.
            if field_name in url_fields:
                # Retrieves the Field instance for the URL field using Django's field lookup.
                field = self.model._meta.get_field(field_name)

                # Creates a custom display function for the URL field that will output HTML for an icon link.
                url_field_display_func = self.create_url_field_display_func(field_name)

                # Sets the `short_description` attribute of the display function to the verbose name of the field,
                # which is used as its display name in the admin.
                url_field_display_func.short_description = field.verbose_name

                # Adds the custom display function to the list of fields to be displayed.
                updated_list_display.append(url_field_display_func)
            else:
                # If the field is not a URL field, adds it directly to the list of fields to be displayed.
                updated_list_display.append(field_name)

        # Returns the updated list of fields and custom display functions to be used in the admin list display.
        return updated_list_display
