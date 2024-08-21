from django.db.models.signals import pre_save, post_save, pre_delete, post_delete


class SignalEnhancedQuerySetMixins:
    """
    Custom QuerySet that sends signals for bulk delete and update operations.

    This QuerySet overrides the default delete and update methods to ensure that Django's `pre_delete`, `post_delete`
    & `pre_save`, `post_save` signals are sent for each object in the queryset.
    """

    def delete(self, *args, **kwargs):
        """
        Deletes all objects in the queryset and sends a `post_delete` signal for each object.

        Args:
            - *args: Variable length argument list.
            - **kwargs: Arbitrary keyword arguments.

        Returns:
            - tuple: A tuple containing the number of objects deleted and a dictionary with the number of deletions per
              object type.
        """
        # Send pre_delete signal for each object
        for obj in self:
            pre_delete.send(sender=obj.__class__, instance=obj)

        # Delete the objects and get the number of deletions
        deleted_count = super().delete(*args, **kwargs)

        # Send post_delete signal for each object
        for obj in self:
            post_delete.send(sender=obj.__class__, instance=obj)

        return deleted_count

    def update(self, **kwargs) -> int:
        """
        Updates all objects in the queryset with the given keyword arguments and sends `pre_save` and `post_save`
        signals for each object.

        Args:
            - **kwargs: Keyword arguments representing the fields to update and their new values.

        Returns:
            - int: The number of rows updated.
        """
        # Send pre_save signal for each object
        for obj in self:
            pre_save.send(sender=obj.__class__, instance=obj, update_fields=kwargs.keys())

        # Update the objects and get the number of updates
        updated_rows = super().update(**kwargs)

        # Update attributes & send post_save signal for each object
        for obj in self:
            for attr, value in kwargs.items():
                # Set the new value for the attribute
                setattr(obj, attr, value)
            # Send the post_save signal
            post_save.send(sender=obj.__class__, instance=obj, created=False, update_fields=kwargs.keys())

        return updated_rows
