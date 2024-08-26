import sys

from pwd import getpwnam


def check_user_exists(user: str) -> bool:
    """
    Check if a user exists in the system.

    :param user: The user to check.
    :return: True if the user exists, False otherwise.
    """
    try:
        getpwnam(user)
        return True
    except KeyError:
        raise KeyError(f"User {user} does not exist on Habrok.")
    
def get_home_fs(user: str) -> str:
    """
    Get the home filesystem of a user.

    :param user: The user to get the home filesystem for.
    :return: The home filesystem of the user.
    """
    try:
        return getpwnam(user).pw_dir
    except KeyError:
        raise KeyError(f"User {user} does not have a home directory on Habrok.")
