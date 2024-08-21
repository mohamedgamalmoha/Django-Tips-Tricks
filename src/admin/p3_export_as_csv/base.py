from typing import List, Tuple

from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _


class BaseCSVModel:
    """
    Base model for handling CSV exports with customizable fields.

    This class provides functionality for specifying which fields should be included or excluded in a CSV export.
    It ensures that either a list of fields to include or exclude is provided, but not both simultaneously.
    """

    csv_fields: List[str] = None
    csv_exclude_fields: List[str] = None

    def get_default_fields(self) -> Tuple[str]:
        """
        Retrieve the default fields of the model.

        This method returns a tuple of all field names defined in the model.

        Returns:
            - Tuple[str]: A tuple containing the names of all model fields.
        """
        return tuple(field.name for field in self.model._meta.fields)

    def get_csv_fields(self) -> List[str]:
        """
        Determine the fields to be included in the CSV export.

        This method returns the fields that should be included in the CSV export. If both `csv_fields` and
        `csv_exclude_fields` are provided, it raises an error.

        Returns:
            - List[str]: A list of field names to be included in the CSV export.

        Raises:
            - ImproperlyConfigured: If both `csv_fields` and `csv_exclude_fields` are provided.
        """
        if self.csv_fields and self.csv_exclude_fields:
            raise ImproperlyConfigured(
                _("Specify either csv_include_fields or csv_exclude_fields, not both.")
            )
        if not self.csv_fields:
            fields = self.get_default_fields()
            if self.csv_exclude_fields:
                fields = [field for field in fields if field not in self.csv_exclude_fields]
            return fields
        return self.csv_fields

    def get_csv_queryset(self, request=None) -> models.QuerySet:
        """
        Retrieve the queryset for CSV export with selected fields.

        This method returns a queryset with only the fields specified by `get_csv_fields`.

        Args:
            - request: The HTTP request object.

        Returns:
            - QuerySet: A queryset with the specified fields for CSV export.
        """
        return self.get_queryset(request).values(*self.get_csv_fields())


class RelatedFieldCSVModel(BaseCSVModel):
    """
    Extended CSV model that includes related fields in the export.

    This class extends `BaseCSVModel` to allow the inclusion of fields from a related model in the CSV export.
    """

    csv_related_field_name: str = None
    csv_related_fields: List[str] = None

    def get_csv_fields(self) -> List[str]:
        """
        Determine the fields to be included in the CSV export, including related fields.

        This method extends the base implementation by adding fields from the related model.

        Returns:
            - List[str]: A list of field names to be included in the CSV export, including related fields.
        """
        fields = super().get_csv_fields()
        if self.csv_related_fields:
            fields.extend(self.csv_related_fields)
        return fields

    def get_csv_queryset(self, request=None) -> models.QuerySet:
        """Retrieve the queryset for CSV export with selected fields and prefetch related fields.

        This method returns a queryset that includes fields from the related model.

        Returns:
            - QuerySet: A queryset with the specified fields and related fields for CSV export.
        """
        queryset = self.get_queryset(request).prefetch_related(self.csv_related_field_name)
        return queryset.values(*self.get_csv_fields())
