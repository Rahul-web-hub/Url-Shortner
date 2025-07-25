import random
import string
import validators

def generate_short_code(existing_codes: set, length: int = 6) -> str:
    """
    Create a unique alphanumeric short code.

    Args:
        existing_codes (set): Short codes already in use.
        length (int): Desired length of the short code (default: 6).

    Returns:
        str: A new, unused short code.
    """
    alphabet = string.ascii_letters + string.digits
    while True:
        code = "".join(random.choices(alphabet, k=length))
        if code not in existing_codes:
            return code


def is_valid_url(url: str) -> bool:
    """
    Check if a URL is well-formed.

    Uses the validators library for robust validation.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    # validators.url returns True on success, otherwise a ValidationFailure
    return validators.url(url) is True
