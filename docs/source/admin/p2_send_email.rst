Send Email
==========

**Title**: Custom Email Sending Functionality in Django Admin

**Description**:
This implementation introduces a custom email sending feature within the Django admin interface. The feature includes
a form for sending emails, allowing the exclusion of certain users from the recipient list. It also incorporates a view
to handle the email sending process and integrates this functionality into the Django admin via a custom `AdminSite`
class.

Context
-------
Files Affected:

- `forms.py`

.. literalinclude:: ../../../src/admin/p2_send_email/forms.py
   :language: python

- `views.py`

.. literalinclude:: ../../../src/admin/p2_send_email/views.py
   :language: python

- `sites.py`

.. literalinclude:: ../../../src/admin/p2_send_email/sites.py
   :language: python

- `send_email.html`

.. literalinclude:: ../../../src/admin/p2_send_email/send_email.html
   :language: python

Reproduction Steps
------------------
How to Reproduce:
1. Create a Django project and include the code for `SendEmailForm`, `SendEmailView`, and `CustomAdminSite` as shown.
2. Ensure the `User` model is available and has email fields populated.
3. Configure the admin site to use `CustomAdminSite` by setting `admin.site = admin_site` in your `admin.py`.
4. Navigate to the Django admin interface and use the "Send Email" functionality from the custom admin view.
5. Verify that the emails are sent to all users except those selected for exclusion.

Expected vs. Actual Behavior:
- **Expected**: The custom admin interface should display a form allowing admins to send emails. Excluded users should not receive the email.
- **Actual**: The form correctly excludes selected users and sends emails to the remaining recipients.

Cause
-----
Root Cause:
In a standard Django admin, there is no built-in functionality for sending emails to users based on a custom form with exclusion logic. This required custom implementation to handle user selection, form processing, and integration into the admin interface.

Solution
--------
Fix Summary:
The solution involves creating a custom form (`SendEmailForm`), a corresponding view (`SendEmailView`), and integrating them into the Django admin via a custom `AdminSite` class (`CustomAdminSite`). This setup allows administrators to send targeted emails directly from the Django admin, with the ability to exclude specific users.

Code Changes:
This section represents the complete implementation, including the form, view, and custom admin site configuration. The provided implementation introduces the required functionality from scratch.

Testing
-------
Validation:
- Test the `SendEmailForm` to ensure it correctly excludes selected users and processes valid email data.
- Verify that the `SendEmailView` sends emails to the correct recipients and handles form submission properly.
- Ensure that the custom admin site (`CustomAdminSite`) correctly integrates the email sending functionality and displays the form in the admin interface.

Conclusion
----------
Summary:
The custom email sending functionality enhances the Django admin by allowing administrators to send emails directly from the admin interface, with the added capability of excluding specific users from the recipient list. This feature is integrated seamlessly into the admin through a custom `AdminSite`.

Best Practices:
- When extending the Django admin interface, ensure that custom functionality is intuitive and follows the standard admin patterns.
- Modularize code by separating forms, views, and site configurations to maintain clarity and reusability.
- Test custom admin functionalities thoroughly, especially when dealing with user data and email communications, to ensure correctness and security.
