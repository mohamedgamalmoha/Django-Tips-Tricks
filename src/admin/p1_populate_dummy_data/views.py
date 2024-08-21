from django import forms
from django.urls import reverse
from django.views.generic import FormView
from django.contrib.admin.helpers import AdminForm
from django.utils.translation import gettext_lazy, ngettext


#: An integer used to set a system-wide cap on dummy data entries to maintain performance.
DUMMY_DATA_MAX_LIMIT = 10


class PopulateDummyDataAdminView(FormView):
    """
    A view to populate dummy data for a given model.

    This view integrates with the Django admin and uses a factory class to generate dummy data for a specified model.
    It provides a custom form within the admin interface where the user can specify the number of dummy items to create.
    The form excludes specified fields and ensures that only the desired number of dummy items are created.
    """
    #: The admin interface class for the model for which dummy data is to be created.
    model_admin = None
    #: The factory class used to create dummy instances of the model.
    factory_class = None
    #: A tuple of field names to exclude from the dummy data creation form.
    exclude = None
    #:  The path to the HTML template used to render the view.
    template_name = 'admin/populate_dummy_data.html'

    def __init__(self, *args, model_admin, factory_class, **kwargs):
        """
        Initializes the view with the model admin and factory class.

        Args:
            - model_admin: The admin interface class for the model.
            - factory_class: The factory class used to create dummy instances of the model.
            - **kwargs: Additional keyword arguments passed to the superclass initializer.
        """
        super(PopulateDummyDataAdminView, self).__init__(*args, **kwargs)
        self.model_admin = model_admin
        self.model = self.model_admin.model
        self.factory_class = factory_class

    def get_exclude(self):
        """
        Constructs a tuple of field names to be excluded.

        Returns:
            - A tuple containing the names of fields to be excluded. This includes both fields explicitly listed in
              `self.exclude` and fields in the model marked as unique.
        """
        # Find all field names in the model that are marked as unique.
        unique_fields = tuple(field.name for field in self.model._meta.get_fields() if getattr(field, 'unique', False))
        # Combine the explicitly excluded fields with the unique fields.
        return self.exclude or () + unique_fields

    def get_form_class(self):
        """
        Dynamically creates and returns a form class for dummy data creation.

        This method overrides the default form to include a 'size' field, which specifies the number of dummy instances
        to be created. It also sets all fields inherited from the base form class as not required, except for the
        'size' field which is mandatory and constrained to a range between 1 and 20.

        Returns:
            - MainForm (forms.ModelForm): A dynamically created form class that inherits from the base form class
            associated with the factory model. This form includes an additional 'size' field to specify the number of
            dummy instances to create.
        """
        # Dynamically generate a base form class using the model, excluding specified fields
        FromBase = forms.modelform_factory(
            self.model,
            exclude=self.get_exclude()
        )
        # Get the base fields from the generated form class
        form_fields = FromBase.base_fields

        # Define a new form class that includes a 'size' field and sets all other fields as not required
        class MainForm(FromBase):
            # Define a 'size' field that is required, with a minimum value of 1 and a maximum value of 20
            size = forms.IntegerField(required=True, min_value=1, max_value=DUMMY_DATA_MAX_LIMIT)
            # Specify the order of fields, placing 'size' at the beginning
            field_order = ('size', *form_fields)

            def __init__(self, *args, **kwargs):
                # Call the superclass initializer
                super(MainForm, self).__init__(*args, **kwargs)
                # Iterate over the form fields and set them as not required
                for field in form_fields:
                    self.fields[field].required = False

        # Return the dynamically created form class
        return MainForm

    def get_admin_form(self):
        """
        Creates and returns an admin form for the dummy data creation.

        Returns:
            - AdminForm: The admin form with fields for dummy data creation.
        """
        form = self.get_form()
        return AdminForm(
            form=form,
            fieldsets=list([(None, {'fields': form.field_order})]),
            prepopulated_fields={},
            readonly_fields=(),
            model_admin=self.model_admin
        )

    def get_context_data(self, **kwargs):
        """
        Adds the admin form to the context data.

        Args:
            - **kwargs: Additional keyword arguments passed to the superclass method.

        Returns:
            - dict: Context data including the admin form.
        """
        context = super().get_context_data(**kwargs)
        context['adminform'] = self.get_admin_form()
        return context

    def form_valid(self, form):
        """
        Handles valid form submission, creating dummy data using the factory class.

        Args:
            - form: The submitted form with valid data.

        Returns:
            - HttpResponseRedirect: A redirect response to the success URL.
        """
        cleaned_data = {k: v for k, v in form.cleaned_data.items() if v}
        self.factory_class.create_batch(**cleaned_data)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        """
        Generates a success message after creating dummy data.

        Args:
            - cleaned_data: The cleaned data from the submitted form.

        Returns:
            - str: A success message indicating the number of objects created.
        """
        return gettext_lazy(
                ngettext(
                    "%d %s object was successfully created.",
                    "%d %s objects were successfully created.",
                    cleaned_data['size'],
                ) % (cleaned_data['size'], self.model._meta.model_name)
            )

    def get_success_url(self):
        """
        Returns the URL to redirect to after successfully creating dummy data.

        Returns:
            - str: A URL to redirect to after form submission.
        """
        info = self.model._meta.app_label, self.model._meta.model_name
        return reverse('admin:%s_%s_changelist' % info)
