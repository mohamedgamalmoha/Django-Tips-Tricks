Populate Dummy Data
===================

**Title**: Populating Dummy Data in Django Admin

**Description**:
This implementation introduces functionality for generating dummy data within the Django admin interface. It provides a
custom view (`PopulateDummyDataAdminView`) and a mixin (`PopulateDummyDataAdminMixin`) to allow admin users to populate
models with dummy data. This is particularly useful for development or testing purposes.

Context
-------
Files Affected:

- `views.py`

.. literalinclude:: ../../../src/admin/p1_populate_dummy_data/views.py
   :language: python

- `mixins.py`

.. literalinclude:: ../../../src/admin/p1_populate_dummy_data/mixins.py
   :language: python

- `populate_dummy_data.html`

.. literalinclude:: ../../../src/admin/p1_populate_dummy_data/populate_dummy_data.html
   :language: django

Reproduction Steps
------------------
How to Reproduce:
1. Implement a Django model and admin class that uses `PopulateDummyDataAdminMixin`.
2. Register the admin class with the Django admin site.
3. Create a custom factory class that generates dummy data for the model.
4. Access the Django admin interface and navigate to the custom URL for populating dummy data.
5. Specify the number of dummy records to create and submit the form.
6. Verify that the dummy data is created and populated in the model.

Expected vs. Actual Behavior:
- **Expected**: The Django admin should provide an option to populate the model with dummy data. The specified number of dummy records should be generated and saved to the database.
- **Actual**: The admin interface correctly offers the dummy data population form, and the generated records are successfully saved in the model.

Cause
-----
Root Cause:
Django admin does not have built-in functionality for generating and populating models with dummy data. This feature is often necessary during development and testing phases, so a custom solution is required.

Solution
--------
Fix Summary:
The solution includes a custom view (`PopulateDummyDataAdminView`) that handles the form for specifying the number of dummy records to create. Additionally, a mixin (`PopulateDummyDataAdminMixin`) integrates this functionality into the Django admin by adding a custom URL and view for dummy data population.

Code Changes:
This section represents the complete implementation, including the view, mixin, and template. The provided implementation introduces the required functionality from scratch.

Testing
-------
Validation:
- Test the `PopulateDummyDataAdminView` to ensure it correctly handles form submissions and generates the specified number of dummy records.
- Verify that `PopulateDummyDataAdminMixin` integrates seamlessly with Django admin, providing the necessary URL and view for dummy data generation.
- Ensure that the form in `populate_dummy_data.html` renders correctly and allows users to input the desired number of dummy records.

Conclusion
----------
Summary:
The dummy data population functionality enhances Django admin by providing a convenient way to generate and populate models with dummy data. This feature is integrated seamlessly into the admin interface, making it useful for development and testing scenarios.

Best Practices:
- Use mixins like `PopulateDummyDataAdminMixin` to centralize and reuse dummy data generation logic across multiple admin classes.
- Ensure that dummy data generation is restricted to development and testing environments to avoid unintended consequences in production.
- Test the functionality thoroughly to ensure it handles edge cases, such as generating large amounts of data or excluding specific fields.
