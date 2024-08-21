from django.contrib import messages
from django.contrib.auth import get_permission_codename
from django.utils.translation import gettext_lazy as _

from .response import CSVHttpResponse
from .base import BaseCSVModel, RelatedFieldCSVModel


class BaseCSVModelAdminMixin:
    """
    Mixin to add CSV export functionality to Django Admin classes.

    This mixin enables Django Admin classes to export data as CSV files. It handles file naming, optional warnings
    before export, and defining admin actions.
    """

    csv_dropdown_label: str = _("Export As CSV")
    csv_allow_warning_message: bool = True
    csv_warning_message: str = _('Data downloaded, be careful it might be sensitive')
    actions = ['export_csv']

    def has_export_csv_permission(self, request) -> bool:
        """
        Check if the user has permission to export data as CSV.

        This method verifies if the current user has the permission to perform the 'export_csv' action.

        Args:
            - request: The HTTP request object.

        Returns:
            - bool: True if the user has the 'export_csv' permission, False otherwise.
        """
        opts = self.opts
        codename = get_permission_codename('export_csv', opts)
        return request.user.has_perm('%s.%s' % (opts.app_label, codename))

    def get_csv_file_name(self) -> str:
        """
        Generate a CSV file name based on the model's app label and model name.

        This method constructs the filename for the CSV file using the app label and model name.

        Returns:
            - str: The name of the CSV file to be downloaded.
        """
        return f"{self.model._meta.app_label}_{self.model._meta.model_name}.csv"

    def get_csv_response(self, request) -> CSVHttpResponse:
        """
        Generate the CSV HTTP response.

        This method creates a `CSVHttpResponse` with the appropriate fields and data for the CSV file.

        Args:
            - request: The HTTP request object.

        Returns:
            - CSVHttpResponse: The HTTP response containing the CSV file.
        """
        return CSVHttpResponse(
            fields=self.get_csv_fields(),
            data=self.get_csv_queryset(request),
            filename=self.get_csv_file_name()
        )

    def export_csv(self, request, queryset):
        """
        Handle the CSV export action from the admin interface.

        This method is executed when the 'export_csv' action is triggered. It optionally displays a warning, and
        returns the CSV file.

        Args:
            - request: The HTTP request object.
            - queryset: The queryset of the model to be exported.

        Returns:
            - HttpResponse: The HTTP response containing the CSV file.
        """
        if self.csv_allow_warning_message:
            self.message_user(request, self.csv_warning_message, messages.WARNING)

        self.message_user(request, f'{self.get_csv_queryset(request).count()} of {self.model._meta.model_name} '
                                   f'was successfully downloaded as csv.', messages.SUCCESS)
        return self.get_csv_response(request)

    export_csv.allowed_permissions = ('export_csv',)
    export_csv.short_description = csv_dropdown_label


class CSVModelAdminMixin(BaseCSVModel, BaseCSVModelAdminMixin):
    """
    Mixin to add CSV export functionality to Django Admin models.

    This mixin combines the features of `BaseCSVModel` and `BaseCSVModelAdminMixin` to enable CSV export from the
    Django Admin interface. It handles field selection, permissions, and file generation.
    """


class RelatedFieldCSVModelAdminMixin(RelatedFieldCSVModel, BaseCSVModelAdminMixin):
    """
    Mixin to add CSV export functionality with related fields to Django Admin models.

    This mixin combines the features of `RelatedFieldCSVModel` and `BaseCSVModelAdminMixin` to enable CSV export from
    the Django Admin interface, including related fields. It handles field selection, permissions, related field
    prefetching, and file generation.
    """
