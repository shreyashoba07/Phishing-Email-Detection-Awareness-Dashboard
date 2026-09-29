import re
from html import unescape


def clean_text(text):
    """
    Clean email text for further analysis.
    """

    if not isinstance(text, str):
        return ""

    # Convert HTML entities
    text = unescape(text)

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Convert to lowercase
    text = text.lower()

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_urls(text):
    """
    Extract URLs from email text.
    """

    if not isinstance(text, str):
        return []

    pattern = r"https?://[^\s]+"
    return re.findall(pattern, text)


def preprocess_email(subject, body):
    """
    Combine and clean the subject and body.
    """

    subject = clean_text(subject)
    body = clean_text(body)

    combined_text = f"{subject} {body}".strip()

    urls = extract_urls(combined_text)

    return {
        "subject": subject,
        "body": body,
        "combined_text": combined_text,
        "urls": urls,
    }