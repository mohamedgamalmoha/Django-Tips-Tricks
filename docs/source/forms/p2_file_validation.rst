File Validation
===============

**Title**: Custom File Validators for Django

**Description**:
This implementation introduces custom file validators in Django to ensure that uploaded files adhere to specified size
and content type constraints. The solution includes two validators: `FileSizeValidator` and `FileContentTypeValidator`.
These validators enforce rules on file uploads by checking the file's size and content type, raising validation errors
when the rules are violated.

Context
-------
Files Affected:

- `validators.py`

.. literalinclude:: ../../../src/forms/p2_file_validation/validators.py
   :language: python

Reproduction Steps
------------------
How to Reproduce:
1. Implement the custom file validators in your Django project by defining them as shown in `validators.py`.
2. Apply the validators to file fields in your models or forms.
3. Attempt to upload files that either exceed the specified size limit or have disallowed content types.
4. Observe the validation behavior and the error messages provided by the validators.

Expected vs. Actual Behavior:
- **Expected**: The file upload process should enforce the specified size and content type constraints. If a file violates these constraints, the upload should be rejected with an appropriate error message.
- **Actual**: The validators work as expected, preventing files that exceed the allowed size or have disallowed content types from being uploaded.

Cause
-----
Root Cause:
Django provides basic file field validation but does not include built-in functionality to enforce specific size limits or restrict content types. Custom validators are needed to add these additional constraints to file uploads.

Solution
--------
Fix Summary:
The solution involves creating two custom validators: `FileSizeValidator` and `FileContentTypeValidator`. These validators are deconstructible, meaning they can be serialized and deserialized by Django's migration framework. The validators enforce file size and content type constraints, raising `ValidationError` with customizable messages when the rules are violated.

Code Changes:
This section represents the complete implementation of the custom file validators, including their application to file fields in models or forms. The provided implementation introduces the required functionality from scratch.

Testing
-------
Validation:
- Test the `FileSizeValidator` by uploading files of various sizes to ensure that it correctly enforces the specified size limit.
- Test the `FileContentTypeValidator` by uploading files with different content types to verify that it only allows the specified types.
- Ensure that the validators raise the appropriate `ValidationError` with the correct error message when validation fails.

Conclusion
----------
Summary:
The custom file validators enhance Django's file upload functionality by adding constraints on file size and content type. These validators are easy to apply and provide clear, customizable error messages when validation fails, improving the overall robustness of file handling in Django applications.

Best Practices:
- Use custom validators like these to enforce application-specific rules on file uploads, ensuring that only acceptable files are allowed.
- Customize the error messages to provide clear guidance to users when their uploads are rejected.
- Test the validators thoroughly in various scenarios to ensure they handle edge cases, such as extremely large files or unexpected content types.
