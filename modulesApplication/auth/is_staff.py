def is_staff_or_superuser(user):
    """A simple function to pass into @user_passes_test decorators when carrying out access control tests.

    Returns:
        True if the user.is_staff or user.is_superuser flags are set, false otherwise."""
    return user.is_staff or user.is_superuser
