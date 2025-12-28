def normalize_command(text):
    """
    Normalize speech text: lowercase, remove extra spaces, minor cleanup
    """
    text = text.lower()
    text = " ".join(text.split())
    return text
