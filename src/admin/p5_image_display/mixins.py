from django.utils.safestring import mark_safe


class ImageFieldDisplayAdminMixin:
    """
    A mixin to enhance admin interfaces with image display capabilities.

    This mixin augments the Django admin interface for models containing image fields. It automatically adds an
    'image_display' field to the fieldsets and readonly_fields if an 'image' field exists, allowing for the images to
    be displayed directly in the admin interface. The actual display rendering is handled by the `image_display`
    method, which relies on an external `create_image_html` function to generate the HTML for displaying the image.
    """

    def get_fieldsets(self, request, obj=None):
        """
        This method overrides the base implementation to modify the fieldsets used in the admin form. Specifically, it
        checks each fieldset for the presence of an 'image' field. If found, and if the 'image_display' field is not
        already present, it adds 'image_display' to the fieldset. This is useful for displaying images directly in the
        admin interface without making them editable.

        Args:
            - request (HttpRequest): The HttpRequest object. obj (Model instance, optional): The model instance being
              processed. Defaults to None.

        Returns:
            - list of tuple: The modified fieldsets with 'image_display' field added where applicable.
        """
        # Call the base implementation first to get the original fieldsets
        fieldsets = super().get_fieldsets(request, obj)

        # Iterate through the fieldsets and their options
        for name, options in fieldsets:
            # Get the 'fields' list from the options, defaulting to an empty list if not found
            fields = options.get('fields', [])

            # Check if 'image' is in the fields and 'image_display' is not
            if 'image' in fields and 'image_display' not in fields:
                # Add 'image_display' to the fields list
                options['fields'] = fields + ('image_display',)

        # Return the modified fieldsets
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        """
        This method overrides the base implementation to ensure 'image_display' is included in the readonly fields of
        the admin form. 'image_display' is used to show a preview of the image without allowing it to be edited
        directly from its representation in the admin.

        Args:
            - request (HttpRequest): The HttpRequest object. obj (Model instance, optional): The model instance being
              processed. Defaults to None.

        Returns:
            - tuple: The modified readonly fields including 'image_display'.
        """
        # Call the base implementation to get the original readonly fields
        readonly_fields = super().get_readonly_fields(request, obj)

        # Check if 'image_display' is not already in the readonly fields
        if 'image_display' not in readonly_fields:
            # Add 'image_display' to the readonly fields tuple
            readonly_fields += ('image_display',)

        # Return the modified readonly fields
        return readonly_fields

    def image_display(self, obj):
        """
        Generates an HTML string for displaying an image with specific styling.

        This function creates an HTML string that represents an image wrapped in an anchor tag, usually for displaying
        in Django admin or templates. It includes inline styling for size and appearance.

        Args:
            - obj (Model instance): The model instance containing the image to display.

        Returns:
            - str: HTML for displaying the image within the admin interface.
        """
        return mark_safe(
            f"""
                <a href='{obj.image.url}'><img src="{obj.image.url}" style="height:400px; width: 400px; 
                    border-radius: 50%; border: 6px solid gray;">
                </a>
            """
        )

    image_display.short_description = ""
