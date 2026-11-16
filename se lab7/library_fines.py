MAX_FIELD_LEN = 1000   # guards against absurdly long numeric strings (DoS)


def _to_int(text):
    """Strictly convert an ASCII-decimal string to int, else return None."""
    text = text.strip()
    if text.startswith('-'):
        sign, text = -1, text[1:]
    else:
        sign = 1
    if not text or len(text) > MAX_FIELD_LEN or not (text.isascii() and text.isdigit()):
        return None
    return sign * int(text)


def parse_member_id(member_id):
    """Parse 'STU-1023' -> ('STU', 1023). Returns None for invalid input."""
    if not isinstance(member_id, str):
        return None
    parts = member_id.strip().split('-')
    if len(parts) != 2:
        return None
    member_type, number = parts[0].strip(), parts[1].strip()
    if not member_type or not member_type.isalpha():
        return None
    value = _to_int(number)
    if value is None or value < 0:
        return None
    return member_type.upper(), value


def total_fine(days_csv):
    """Fine = 2 per day beyond 14 for each book. Invalid entries are skipped;
    invalid/non-string input gives a fine of 0."""
    if not isinstance(days_csv, str):
        return 0
    fine = 0
    for item in days_csv.split(','):
        d = _to_int(item)
        if d is not None and d > 14:
            fine += (d - 14) * 2
    return fine


def shelf_code(title):
    """First letters of the first two words, upper-cased.
    Returns '' if the title is not a string or has fewer than two words."""
    if not isinstance(title, str):
        return ""
    words = title.split()
    if len(words) < 2:
        return ""
    return (words[0][0] + words[1][0]).upper()


def main():
    print("==== Running parse_member_id ====")
    user_input = input("Enter a member ID (e.g. STU-1023): ")
    result = parse_member_id(user_input)
    print("Member Type and Number:", result if result is not None else "Invalid member ID")

    print("\n==== Running total_fine ====")
    user_input = input("Enter days kept for each book as CSV (e.g. 10,20,30): ")
    result = total_fine(user_input)
    print("Total Fine:", result)

    print("\n==== Running shelf_code ====")
    user_input = input("Enter a book title with at least two words: ")
    result = shelf_code(user_input)
    print("Shelf Code:", result if result else "Invalid title (need at least two words)")


if __name__ == "__main__":
    main()
