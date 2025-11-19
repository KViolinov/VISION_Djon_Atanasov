import os
import re

# Path to the contacts file
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
CONTACTS_FILE = os.path.join(ROOT_DIR, "contacts.txt")

def find_contact(query: str, field: str = None) -> str | dict | None: # needs work
    """
    Searches the contacts.txt file for a given query (usually a name) and returns
    either the whole contact as a dictionary or a specific field.

    Args:
        query (str): The search term (usually person's name, e.g., "Вероника")
        field (str, optional): Specific field to return. Can be one of:
                               "име", "телефон", "имейл", "линк" (case-insensitive)
                               If not provided, returns the full contact dict.

    Returns:
        dict | str | None: Returns a dictionary with contact data or a single field value.
                           Returns None if the contact or field is not found.
    """

    if not os.path.exists(CONTACTS_FILE):
        print(f"⚠️ File not found: {CONTACTS_FILE}")
        return None

    with open(CONTACTS_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        # Skip comments or empty lines
        if line.strip().startswith("/*") or not line.strip():
            continue

        # Extract all fields using regex
        match = re.search(
            r"\[Име\]:\s*(.*?),\s*\[Телефон\]:\s*(.*?),\s*\[Имейл\]:\s*(.*?),\s*\[Линк\]:\s*(.*?);",
            line.strip()
        )
        if not match:
            continue

        name, phone, email, instagram = [m.strip() for m in match.groups()]
        contact = {
            "име": name,
            "телефон": phone,
            "имейл": email,
            "линк": instagram
        }

        # Check if the search query matches (case-insensitive)
        if query.lower() in name.lower():
            if field:
                # Return specific field if requested
                field = field.lower()
                if field in contact:
                    return contact[field]
                else:
                    print(f"⚠️ Полето '{field}' не е намерено за {name}.")
                    return None
            else:
                # Return the whole contact dictionary
                return contact

    print(f"⚠️ Контакт с '{query}' не е намерен.")
    return None