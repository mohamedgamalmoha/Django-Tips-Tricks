Password Validation
===================

**Title**: Custom Password Validators with Customizable Messages

**Description**:
This implementation provides custom password validators in Django, allowing for customizable help texts and validation
messages. The solution includes a `ValidatorMixin` that extends Django's built-in validators to offer enhanced
flexibility, particularly in customizing error messages and help texts. The custom validators are then integrated into
the Django settings for password validation.

Context
-------
Files Affected:

- `mixins.py`

.. literalinclude:: ../../../src/forms/p1_password_validation/mixins.py
   :language: python

- `password_validation.py`

.. literalinclude:: ../../../src/forms/p1_password_validation/password_validation.py
   :language: python

- `settings.py`

.. literalinclude:: ../../../src/forms/p1_password_validation/settings.py
   :language: python

Reproduction Steps
------------------
How to Reproduce:
1. Implement the custom password validators in your Django project by defining them as shown in `password_validation.py` and `mixins.py`.
2. Update the `AUTH_PASSWORD_VALIDATORS` setting in `settings.py` to reference these custom validators.
3. Attempt to create or update a user password that triggers the custom validation logic.
4. Observe the custom help text and validation error messages provided by the validators.

Expected vs. Actual Behavior:
- **Expected**: The Django password validation process should utilize the custom validators, displaying the specified help texts and error messages when validation fails.
- **Actual**: The custom validators work as expected, providing the correct help text during password setup and appropriate error messages when validation criteria are not met.

Cause
-----
Root Cause:
The default Django password validators come with fixed help texts and validation messages, which might not always align with specific project requirements. To address this, custom validators were created to allow for greater flexibility in defining these messages.

Solution
--------
Fix Summary:
The solution involves creating a `ValidatorMixin` that can be applied to Django's built-in password validators. This mixin allows for custom help texts and validation messages, enabling more tailored feedback during the password validation process. The custom validators are then integrated into Django's authentication system through the `AUTH_PASSWORD_VALIDATORS` setting.

Code Changes:
This section represents the complete implementation of the custom password validators, including the mixin, validator classes, and settings configuration. The provided implementation introduces the required functionality from scratch.

Testing
-------
Validation:
- Test the custom validators by setting and changing passwords in the Django admin or through forms that utilize the validators.
- Ensure that the validators enforce the expected rules and that the custom help texts and validation messages are displayed correctly.
- Verify that each validator operates independently and does not interfere with the others.

Conclusion
----------
Summary:
The custom password validation functionality enhances Django's built-in validators by allowing the specification of custom help texts and error messages. This implementation is integrated seamlessly into Django's password validation system, providing more flexibility in enforcing password policies.

Best Practices:
- Use custom validators like these to ensure that error messages and help texts are clear, concise, and aligned with your application's requirements.
- Keep validation messages user-friendly and informative, as they play a crucial role in guiding users to create secure passwords.
- Test custom validators thoroughly to ensure they interact correctly with Django's authentication and form systems.
