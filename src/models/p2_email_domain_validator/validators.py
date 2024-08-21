from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class DomainEmailValidator(EmailValidator):
    """
    A validator that checks if the email's domain part matches a specific allowed domain.

    The class adds an extra layer of validation on top of the basic email validation by ensuring the domain part of the
    email matches a specified domain. It supports both literal IP addresses and domain names.
    """

    _message = _('Invalid email domain it should {allowed_domain}')

    @property
    def message(self) -> str:
        """
        Retrieves the formatted validation message.

        The message includes the allowed domain, providing a clear indication of the
        requirement for the email address.

        Returns:
            - str: The formatted validation message.
        """
        return self._message.format(allowed_domain=self.allowed_domain)

    @message.setter
    def message(self, value: str) -> None:
        """
        Sets a custom validation message.

        This setter allows for overriding the default validation message.

        Args:
            - value (str): The custom message to be used for validation errors.
        """
        self._message = value

    def __init__(self, allowed_domain: str, *args, **kwargs) -> None:
        """
        Initializes the DomainEmailValidator with a specific allowed domain.

        This constructor sets the domain that email addresses must match and passes any additional arguments to the
        parent `EmailValidator` class.

        Args:
            - allowed_domain (str): The domain that is allowed for the email addresses.
            - *args: Variable length argument list.
            - **kwargs: Arbitrary keyword arguments passed to the parent `EmailValidator`.
         """
        self.allowed_domain = allowed_domain
        super().__init__(*args, **kwargs)

    def validate_domain_part(self, domain_part: str) -> bool:
        """
        Validates the domain part of the email address.

        This method checks if the domain part of the email matches the allowed domain specified during initialization.
        It handles both domain names and literal IP addresses.

        Args:
            - domain_part (str): The domain part of the email address to validate.

        Returns:
            - bool: `True` if the domain part is valid and matches the allowed domain, `False` otherwise.
        """
        if domain_part.lower() == self.allowed_domain.lower():
            return True

        if self.domain_regex.match(domain_part):
            return domain_part.lower() == self.allowed_domain.lower()

        literal_match = self.literal_regex.match(domain_part)
        if literal_match:
            ip_address = literal_match[1]
            try:
                self.validate_ipv46_address(ip_address)
                return True
            except ValidationError:
                ...
        return False
