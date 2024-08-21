Age From Birth
==============

**Title**: Custom QuerySet for Annotating and Filtering Profiles by Age

**Description**:
This implementation introduces a custom `ProfilerQuerySet` for the `Profile` model, providing methods to annotate
profiles with an age field and to filter profiles based on a specific age range. The custom QuerySet enhances the
functionality of the `Profile` model by making it easier to work with age-related data directly within the Django ORM.

Context
-------
Files Affected:

- `models.py`

.. literalinclude:: ../../../src/models/p3_age_from_birth/models.py
   :language: python

Reproduction Steps
------------------
How to Reproduce:
1. Implement the `Profile` model and the `ProfilerQuerySet` as shown in `models.py`.
2. Use the `with_age` method to annotate the queryset with an `age` field calculated from the `date_of_birth`.
3. Use the `age_range` method to filter profiles based on a specific age range.
4. Query the `Profile` model to test the age-related annotations and filters.

Expected vs. Actual Behavior:
- **Expected**: The `with_age` method should annotate each profile with an `age` field, and the `age_range` method should filter profiles based on the specified age range.
- **Actual**: The custom QuerySet methods work as expected, providing accurate age calculations and filtering profiles within the desired age range.

Cause
-----
Root Cause:
Django's ORM does not natively support age calculations or filtering based on age. Custom QuerySet methods are needed to provide these capabilities directly within the ORM, allowing for more powerful and expressive queries.

Solution
--------
Fix Summary:
The solution involves creating a custom QuerySet, `ProfilerQuerySet`, that adds two methods: `with_age` and `age_range`. The `with_age` method calculates the age of each profile based on the `date_of_birth` field, and the `age_range` method filters profiles to include only those within a specified age range. These methods enhance the `Profile` model by allowing age-based annotations and filters to be applied directly in queries.

Code Changes:
This section represents the complete implementation of the custom QuerySet and its integration with the `Profile` model. The provided implementation introduces the required functionality from scratch.

Testing
-------
Validation:
- Test the `with_age` method by querying the `Profile` model and verifying that the `age` annotation is calculated correctly.
- Test the `age_range` method by filtering profiles within a specific age range and confirming that the results match the expected age criteria.
- Ensure that the custom QuerySet methods work seamlessly with other Django ORM features, such as filtering, ordering, and aggregation.

Conclusion
----------
Summary:
The `ProfilerQuerySet` provides powerful tools for working with age-related data in the `Profile` model. By allowing profiles to be annotated with an `age` field and filtered by age range, this custom QuerySet enhances the expressiveness and flexibility of queries involving age.

Best Practices:
- Use custom QuerySets like `ProfilerQuerySet` to encapsulate complex query logic, making your models more powerful and easier to work with.
- When calculating age, account for edge cases, such as leap years and dates near the start or end of the year, to ensure accuracy.
- Test custom QuerySet methods thoroughly, especially when dealing with date and time calculations, to ensure they handle all possible scenarios correctly.
