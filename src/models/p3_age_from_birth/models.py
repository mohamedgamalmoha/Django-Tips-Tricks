from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import localdate
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class ProfilerQuerySet(models.QuerySet):
    """
    A custom queryset for a profile model that provides additional methods to annotate profiles with age and filter
    profiles based on age range.
    """

    def with_age(self):
        """
        Annotate the queryset with an 'age' field calculated from the date_of_birth field.

        Returns:
            - QuerySet: The annotated queryset with an additional 'age' field.
        """
        # Calculate the current date
        current_date = localdate()
        # Exclude profiles where date of birth is not specified
        return self.exclude(date_of_birth__isnull=True).annotate(
            # Annotate each profile with the calculated age
            age=models.ExpressionWrapper(
                # Calculate age as the difference in years minus 1 if birthday hasn't occurred yet this year
                current_date.year - models.F('date_of_birth__year') -
                models.Case(
                    # Check if the birthday hasn't occurred yet this year
                    models.When(
                        models.Q(date_of_birth__month__gt=current_date.month) |
                        models.Q(date_of_birth__month=current_date.month, date_of_birth__day__gt=current_date.day),
                        then=models.Value(1)
                    ),
                    default=models.Value(0),
                    output_field=models.IntegerField()
                ),
                output_field=models.IntegerField()
            )
        )

    def age_range(self, start: int, end: int):
        """
        Filter the queryset to only include profiles within a specific age range.

        Args:
            - start (int): The start of the age range.
            - end (int): The end of the age range.

        Returns:
           - QuerySet: The filtered queryset including only profiles within the specified age range.
        """
        # Filter the profiles to those within the specified age range
        return self.with_age().filter(age__gte=start, age__lte=end)


class Profile(models.Model):
    """
    Profile model to store additional information for a user. Each user has one unique profile.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name=_('User'))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('Date of Birth'))

    objects = ProfilerQuerySet.as_manager()
