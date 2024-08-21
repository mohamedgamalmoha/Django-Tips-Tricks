Signal Enhanced
===============

**Title**: Enhanced Django QuerySet with Signal Support for Bulk Operations

**Description**:
This implementation introduces a custom Django QuerySet mixin, `SignalEnhancedQuerySetMixins`, that ensures Django
signals (`pre_save`, `post_save`, `pre_delete`, `post_delete`) are sent for each object during bulk delete and update
operations. By default, Django does not send these signals for bulk operations, so this mixin is particularly useful
for scenarios where signal handling is necessary even in bulk actions.

Context
-------
Files Affected:

- `mixins.py`

.. literalinclude:: ../../../src/models/p1_signal_enhanced/mixins.py
   :language: python

Reproduction Steps
------------------
How to Reproduce:
1. Implement a custom model and apply the `SignalEnhancedQuerySetMixins` to its QuerySet.
2. Perform bulk delete and update operations on the model's QuerySet.
3. Observe the behavior of Django signals by attaching listeners to `pre_save`, `post_save`, `pre_delete`, and `post_delete` signals.
4. Verify that the signals are sent for each object in the QuerySet during the bulk operations.

Expected vs. Actual Behavior:
- **Expected**: During bulk delete and update operations, Django signals (`pre_save`, `post_save`, `pre_delete`, `post_delete`) should be sent for each individual object in the QuerySet.
- **Actual**: The custom QuerySet mixin works as expected, ensuring that the signals are properly sent during bulk operations.

Cause
-----
Root Cause:
In Django, bulk delete and update operations do not send `pre_save`, `post_save`, `pre_delete`, and `post_delete` signals by default. This can lead to scenarios where important side effects, such as cache invalidation or audit logging, are missed during these operations.

Solution
--------
Fix Summary:
The solution involves creating a custom QuerySet mixin, `SignalEnhancedQuerySetMixins`, that overrides the `delete` and `update` methods. This mixin manually triggers the appropriate signals for each object in the QuerySet during bulk operations, ensuring that all related side effects are handled correctly.

Code Changes:
This section represents the complete implementation of the custom QuerySet mixin, ensuring that Django signals are triggered during bulk delete and update operations.

Testing
-------
Validation:
- Test the `delete` method of the QuerySet to ensure that `pre_delete` and `post_delete` signals are sent for each object.
- Test the `update` method of the QuerySet to ensure that `pre_save` and `post_save` signals are sent for each object.
- Verify that the expected side effects (e.g., cache invalidation, logging) occur when the signals are triggered.

Conclusion
----------
Summary:
The `SignalEnhancedQuerySetMixins` mixin provides a solution to a common limitation in Django where signals are not sent during bulk delete and update operations. By applying this mixin to a model's QuerySet, developers can ensure that signals are properly sent, preserving the expected behavior of signal handlers.

Best Practices:
- Use this mixin in scenarios where it's critical to ensure that signals are sent during bulk operations, such as for logging, cache management, or other side effects.
- Test thoroughly to ensure that the signals are being sent as expected and that the associated side effects are occurring correctly.
- Consider the performance implications of sending signals for each object in a large QuerySet and assess whether this approach is appropriate for your use case.
