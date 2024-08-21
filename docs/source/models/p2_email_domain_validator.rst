Email Domain Validator
======================


Problem Overview
----------------
**Title**: Custom Domain-Specific Email Validator in Django

**Description**:
This implementation introduces a custom email validator, `DomainEmailValidator`, that extends Django's
`EmailValidator`. The validator ensures that the domain part of an email address matches a specified allowed domain,
adding an extra layer of validation to restrict email addresses to a particular domain. It supports validation for both
domain names and literal IP addresses.

Context
-------
Files Affected:

- `validators.py`

.. literalinclude:: ../../../src/models/p2_email_domain_validator/validators.py
   :language: python

Reproduction Steps
------------------
How to Reproduce:
1. Implement the `DomainEmailValidator` in your Django project by defining it as shown in `validators.py`.
2. Apply the validator to an email field in a Django form or model.
3. Attempt to submit email addresses with different domain parts, some matching the allowed domain and some not.
4. Observe the validation behavior and the error messages provided by the validator.

Expected vs. Actual Behavior:
- **Expected**: The email validation process should enforce that the email address belongs to the specified domain. If the domain part does not match, the validator should raise a `ValidationError` with a clear message.
- **Actual**: The custom validator works as expected, preventing email addresses with disallowed domains from being accepted.

Cause
-----
Root Cause:
Django's default `EmailValidator` checks the general structure of an email address but does not enforce specific domain restrictions. This is often necessary for applications that require email addresses from a particular domain, such as company emails or educational institutions.

Solution
--------
Fix Summary:
The solution involves creating a `DomainEmailValidator` that extends the `EmailValidator`. This custom validator adds domain-specific validation to ensure that the email address matches the allowed domain. The validator is deconstructible, meaning it can be serialized and deserialized by Django's migration framework.

Code Changes:
This section represents the complete implementation of the custom email validator, including its application to email fields in forms or models.

Testing
-------
Validation:
- Test the `DomainEmailValidator` by applying it to an email field and submitting various email addresses.
- Ensure that the validator correctly accepts emails with the allowed domain and rejects those with disallowed domains.
- Verify that the error message is clear and informative when validation fails.

Conclusion
----------
Summary:
The `DomainEmailValidator` enhances Django's email validation by restricting email addresses to a specific domain. This is particularly useful for applications that need to enforce domain-specific email policies. The validator is easy to implement and provides clear feedback to users when their email address does not meet the required domain criteria.

Best Practices:
- Use custom validators like `DomainEmailValidator` to enforce domain-specific email policies, ensuring that only valid email addresses from the desired domain are accepted.
- Customize the validation error message to provide clear guidance to users about the domain requirement.
- Test the validator thoroughly to ensure it handles various edge cases, such as literal IP addresses or unusual domain structures.
