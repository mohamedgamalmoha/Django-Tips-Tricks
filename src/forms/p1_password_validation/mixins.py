from django.core.exceptions import ValidationError


class ValidatorMixin:
    """
    A mixin to provide custom validation and help text functionality.

    This mixin allows subclasses to define custom help text and validation messages, which are utilized during the
    validation process. It overrides the standard validation method to raise a ValidationError with a custom message.
    """
    #: A string to be used as the help text for the validator.
    help_text: str
    #: A string to be used as the validation error message.
    validation_text: str

    def __init__(self, *args, help_text: str = None, validation_text: str = None, **kwargs) -> None:
        """
        Initializes the ValidatorMixin with optional help and validation text.

        Args:
            - help_text (str, optional): Custom help text for the validator. Defaults to None.
            - validation_text (str, optional): Custom validation text for errors. Defaults to None.
            - *args: Variable length argument list passed to the superclass.
            - **kwargs: Arbitrary keyword arguments passed to the superclass.
        """
        super().__init__(*args, **kwargs)
        if help_text:
            self.help_text = help_text
        if validation_text:
            self.validation_text = validation_text

    def validate(self, password, user=None):
        """
        Validates the password and raises a custom ValidationError if validation fails.

        Args:
            - password (str): The password to validate.
            - user (optional): The user object related to the password. Defaults to None.

        Raises:
            - ValidationError: If validation fails, this error is raised with a custom message.
        """
        try:
            super().validate(password, user)
        except ValidationError as e:
            raise ValidationError(
                self.get_validation_text(),
                code=e.code,
                params=e.params
            )

    def get_help_text(self) -> str:
        """
        Returns the custom help text.

        Returns:
            - str: The help text associated with the validator.
        """
        return self.help_text

    def get_validation_text(self) -> str:
        """Returns the custom validation error message.

        Returns:
            - str: The validation error message associated with the validator.
        """
        return self.validation_text
