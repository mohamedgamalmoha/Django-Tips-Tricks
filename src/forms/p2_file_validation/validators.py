from typing import List

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

DEFAULT_SIZE_MB = 5  # MB
MB_TO_BYTES = 1024 * 1024  # Conversion rate from MB to bytes


@deconstructible
class FileSizeValidator:
    """
    Validator to ensure a file's size does not exceed a specified limit.

    This validator checks if the uploaded file's size is within the allowed limit. If the file exceeds the specified
    size, a ValidationError is raised.
    """
    #: Default error message for exceeding size limit.
    default_message = _('File size exceeds the limit of %(max_size)s.')
    #: The error code used when the size limit is exceeded.
    code = 'size_limit'
    #: Default error message for failed validation.
    fail_message = _('File size validation failed with error: %(error)s')
    #: The error code used when validation fails unexpectedly.
    fail_code = 'validation_fail'

    def __init__(self, size_limit: int = DEFAULT_SIZE_MB, message: str = None, code: str = None) -> None:
        """
        Initialize the FileSizeValidator with a size limit.

        Args:
            - size_limit (int): The maximum allowed file size in MB. Defaults to DEFAULT_SIZE_MB.
            - message (str, optional): Custom error message for exceeding size limit. Defaults to None.
            - code (str, optional): Custom error code for exceeding size limit. Defaults to None.
        """
        self.size_limit = size_limit
        self.message = message or self.default_message
        self.code = code or self.code

    def __call__(self, value) -> None:
        """
        Validate the file size.

        This method checks if the file size exceeds the specified limit and raises a ValidationError if it does.

        Args:
            - value: The file being validated.

        Raises:
            - ValidationError: If the file size exceeds the limit or if there's an issue during validation.
        """
        try:
            if value.size > self.size_limit_in_bytes:
                raise ValidationError(
                    self.message,
                    code=self.code,
                    params={'max_size': self.size_limit_str},
                )
        except (AttributeError, ValueError) as e:
            raise ValidationError(
                self.fail_message,
                code=self.fail_code,
                params={'error': str(e)},
            )

    @property
    def size_limit_in_bytes(self) -> int:
        """
        Convert the size limit from MB to bytes.

        Returns:
            - int: The size limit in bytes.
        """
        return self.size_limit * MB_TO_BYTES

    @property
    def size_limit_str(self) -> str:
        """
        Return the size limit as a string with 'MB' suffix.

        Returns:
            - str: The size limit as a string.
        """
        return f'{self.size_limit} MB'

    def __eq__(self, other: 'FileSizeValidator') -> bool:
        """
        Check equality between two FileSizeValidator instances.

        Args:
            - other: Another instance of FileSizeValidator.

        Returns:
            - bool: True if both instances are equal, otherwise False.
        """
        if not isinstance(other, FileSizeValidator):
            return False
        return (
            self.size_limit == other.size_limit and
            self.message == other.message and
            self.code == other.code and
            self.fail_message == other.fail_message and
            self.fail_code == other.fail_code
        )


@deconstructible
class FileContentTypeValidator:
    """
    Validator to ensure a file's content type is allowed.

    This validator checks if the uploaded file's content type is within the allowed types. If the file's content type
    is not allowed, a ValidationError is raised.
    """
    #: Default error message for invalid content type.
    default_message = _('File content type %(content_type)s is not allowed. Allowed types: %(allowed_types)s.')
    #: The error code used when the content type is invalid.
    code = 'invalid_type'
    #: Default error message for failed validation.
    fail_message = _('File content validation failed with error: %(error)s')
    #: The error code used when validation fails unexpectedly.
    fail_code = 'validation_fail'

    def __init__(self, allowed_types: List[str], message: str = None, code: str = None) -> None:
        """
        Initialize the FileContentTypeValidator with allowed content types.

        Args:
            - allowed_types (List[str]): The list of allowed content types.
            - message (str, optional): Custom error message for invalid content type. Defaults to None.
            - code (str, optional): Custom error code for invalid content type. Defaults to None.
        """
        self.allowed_types = allowed_types
        self.message = message or self.default_message
        self.code = code or self.code

    def __call__(self, value) -> None:
        """
        Validate the file's content type.

        This method checks if the file's content type is within the allowed types and raises a ValidationError if it is
        not.

        Args:
            - value: The file being validated.

        Raises:
            - ValidationError: If the content type is not allowed or if there's an issue during validation.
        """
        try:
            if value.content_type not in self.allowed_types:
                raise ValidationError(
                    self.message,
                    code=self.code,
                    params={'content_type': value.content_type, 'allowed_types': ', '.join(self.allowed_types)},
                )
        except (AttributeError, ValueError) as e:
            raise ValidationError(
                self.fail_message,
                code=self.fail_code,
                params={'error': str(e)},
            )

    def __eq__(self, other: 'FileContentTypeValidator') -> bool:
        """
        Check equality between two FileContentTypeValidator instances.

        Args:
            - other: Another instance of FileContentTypeValidator.

        Returns:
            - bool: True if both instances are equal, otherwise False.
        """
        if not isinstance(other, FileContentTypeValidator):
            return False
        return (
            self.allowed_types == other.allowed_types and
            self.message == other.message and
            self.code == other.code and
            self.fail_message == other.fail_message and
            self.fail_code == other.fail_code
        )
