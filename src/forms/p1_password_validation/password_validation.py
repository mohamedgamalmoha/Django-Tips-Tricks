from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import (UserAttributeSimilarityValidator, MinimumLengthValidator,
                                                     CommonPasswordValidator, NumericPasswordValidator)

from .mixins import ValidatorMixin


class CustomUserAttributeSimilarityValidator(ValidatorMixin, UserAttributeSimilarityValidator):
    """
    A custom validator to check if the password is too similar to other personal information.

    This class extends `UserAttributeSimilarityValidator` and `ValidatorMixin` to provide custom help text and
    validation messages when the password is similar to the user's personal attributes.
    """
    help_text = _("Your password can’t be too similar to your other personal information.")
    validation_text = _("The password is too similar to the %(verbose_name)s.")


class CustomMinimumLengthValidator(ValidatorMixin, MinimumLengthValidator):
    """
    A custom validator to enforce a minimum password length.

    This class extends `MinimumLengthValidator` and `ValidatorMixin` to provide custom help text and validation
    messages for minimum length enforcement.
    """
    help_text = _("Your password must contain at least %(min_length)d characters.")
    validation_text = help_text


class CustomCommonPasswordValidator(ValidatorMixin, CommonPasswordValidator):
    """
    A custom validator to ensure the password is not a commonly used password.

    This class extends `CommonPasswordValidator` and `ValidatorMixin` to provide custom help text and validation
    messages when the password is too common.
    """
    help_text = _("Your password can’t be a commonly used password.")
    validation_text = _("This password is too common.")


class CustomNumericPasswordValidator(ValidatorMixin, NumericPasswordValidator):
    """
    A custom validator to prevent passwords that are entirely numeric.

    This class extends `NumericPasswordValidator` and `ValidatorMixin` to provide custom help text and validation
    messages when the password is entirely numeric.
    """
    help_text = _("Your password can’t be entirely numeric.")
    validation_text = _("This password is entirely numeric.")
