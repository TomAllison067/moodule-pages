def is_staff_or_superuser(user):
    """A simple function to pass into @user_passes_test decorators"""
    return user.is_staff or user.is_superuser
