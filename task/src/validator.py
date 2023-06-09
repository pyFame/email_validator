from typing import Tuple, Dict

import string


def validate_email_addr(email_addr: str) -> bool:
    """
    Returns True if the email_addr is valid per specification. Otherwise, return False.
    """

    addr = email_addr.strip()

    if addr.count("@") != 1:
        raise ValueError("Email address must contain a single @")

    # Total length of email too long.
    if len(addr.encode()) > 254:
        raise ValueError("Email address must not exceed 254 bytes")

    # Split the address into local and domain parts
    local_part, domain_part = addr.split("@",1)

    # Check local part length constraints
    if len(local_part.encode()) > 64:
        raise ValueError("Local part of email address must not exceed 64 bytes")

    # Check domain part length constraints
    if len(domain_part.encode()) > 251:
        raise ValueError("Domain part of email address must not exceed 251 bytes")

    # Check valid characters in the email address
    valid_characters = set(string.ascii_letters + string.digits + "@-.") #instead of abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@.
    if not all(char in valid_characters for char in addr ):
        raise ValueError("Invalid characters in the email address")

    # Check that hyphens and dots are not the first or last character of the local part
    if local_part[0] in ["-", "."] or local_part[-1] in ["-", "."]:
        raise ValueError("Hyphens or dots cannot be the first or last character of the local part")

    # Check valid top-level domain (TLD)
    valid_tlds = [".com", ".net", ".org"]
    if not domain_part.endswith(tuple(valid_tlds)):
        raise ValueError("Invalid top-level domain (TLD)")

    # Check that periods (.) are only allowed in the top-level domain (TLD)
    if "." in domain_part[:-4]:
        raise ValueError("Periods (.) are only allowed in the top-level domain (TLD)")

    return True


def validate_email_payload(sender_name: str, sender_addr: str, receiver_name: str, receiver_addr: str, html: str,
                           replacements: Dict) -> bool:
    """
    Returns True if the payload is validated and is safe to send out. Otherwise, return False.
    """
    validate_names(sender_name, receiver_name)

    if not validate_email_addr(sender_addr):
        return False

    if not validate_email_addr(receiver_addr):
        return False

    validate_html_replacements(html,replacements)

    return True


def validate_names(sender_name: str, receiver_name: str) -> None:
    sender_name = sender_name.strip()
    receiver_name = receiver_name.strip()

    if not (5 <= len(sender_name) <= 30):
        raise ValueError("Sender name should be between 5 and 30 characters")
    if not (5 <= len(receiver_name) <= 60):
        raise ValueError("Receiver name should be between 5 and 60 characters")

def validate_html_replacements(html: str, replacements: dict) -> None:
    """
    Validates the HTML and replacements according to the given specifications. Raises ValueError if any validation fails.
    """
    import re


    # Check if all replacement keys are present in the HTML
    for key in replacements.keys():
        if len(replacements[key])==0: raise  ValueError("Replacement values must be non-empty")

        placeholder = "{" + key + "}"
        if placeholder not in html:
            raise ValueError(f"Replacement key '{key}' not found in the HTML")

    # Check if there are any surplus replacement keys not used in the HTML
    for placeholder in re.findall(r"\{(\w+)\}", html):
        if placeholder not in replacements:
            raise ValueError(f"Surplus replacement key '{placeholder}' not used in the HTML")
