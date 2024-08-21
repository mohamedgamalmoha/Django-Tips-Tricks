Export Data As CSV
==================

**Title**: Implementing CSV Export Functionality in Django Admin

**Description**:
This implementation provides CSV export functionality for Django models, specifically tailored for the Django admin
interface. It includes several components: a custom `HttpResponse` subclass for serving CSV files, base models for
handling CSV fields, and mixins to integrate CSV export features into Django admin classes.

Context
-------
Files Affected:

- `response.py`

.. literalinclude:: ../../../src/admin/p3_export_as_csv/response.py
   :language: python

- `base.py`

.. literalinclude:: ../../../src/admin/p3_export_as_csv/base.py
   :language: python

- `mixins.py`

.. literalinclude:: ../../../src/admin/p3_export_as_csv/mixins.py
   :language: python

Reproduction Steps
------------------
How to Reproduce:
1. Implement a Django model and admin class that uses `CSVModelAdminMixin` or `RelatedFieldCSVModelAdminMixin`.
2. Register the admin class with the Django admin site.
3. Access the Django admin interface and use the "Export As CSV" action from the list view.
4. Verify that the CSV file is generated with the correct fields and data, and that related fields (if applicable) are included.

Expected vs. Actual Behavior:
- **Expected**: The Django admin should provide an "Export As CSV" action, generating a CSV file with the specified fields and related fields (if applicable).
- **Actual**: The admin interface correctly offers the CSV export action, and the generated file includes the expected data and fields.

Cause
-----
Root Cause:
By default, Django admin does not provide a built-in mechanism for exporting model data as CSV files, particularly with custom field selection and related field handling. This required the development of custom mixins and classes to facilitate CSV export in a flexible and reusable manner.

Solution
--------
Fix Summary:
The solution includes a custom `CSVHttpResponse` class for serving CSV files, base models (`BaseCSVModel`, `RelatedFieldCSVModel`) for managing CSV fields, and admin mixins (`BaseCSVModelAdminMixin`, `CSVModelAdminMixin`, `RelatedFieldCSVModelAdminMixin`) to integrate the CSV export functionality into the Django admin interface.

Code Changes:
This section represents the complete implementation of CSV export functionality, including the response class, base models, and admin mixins. The provided implementation introduces the required functionality from scratch.

Testing
-------
Validation:
- Test the `CSVHttpResponse` to ensure it correctly generates CSV files with the provided fields and data.
- Verify that `BaseCSVModel` and `RelatedFieldCSVModel` correctly handle field selection and exclusion.
- Ensure that `CSVModelAdminMixin` and `RelatedFieldCSVModelAdminMixin` integrate seamlessly with Django admin, providing a functional CSV export option in the admin interface.

Conclusion
----------
Summary:
The CSV export functionality is implemented to enhance Django admin by providing a convenient way to export model data as CSV files. The solution includes components for generating CSV responses, managing CSV fields, and integrating the feature into the admin interface, including support for related fields.

Best Practices:
- Use mixins like `CSVModelAdminMixin` to centralize and reuse CSV export logic across multiple admin classes.
- Ensure that CSV exports are tested for different model configurations, including those with related fields, to guarantee consistent and accurate output.
- Consider the sensitivity of the exported data and implement appropriate permission checks and warnings to ensure secure handling of the CSV files.
