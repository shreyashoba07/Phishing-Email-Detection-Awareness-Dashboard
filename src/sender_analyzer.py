import re


SAFE_DOMAINS = {
    "example.com",
    "example.org",
    "example.net",
    "invalid.test",
}


def analyze_sender(sender):
    """
    Analyze an email sender address using simple defensive rules.
    """

    sender = (sender or "").strip().lower()

    indicators = []
    score = 0

    # Check whether the address has a valid basic format
    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.match(email_pattern, sender):
        indicators.append("Invalid or unusual sender email format")
        score += 20

    if "@" not in sender:
        return {
            "sender": sender,
            "score": score + 20,
            "risk_level": "HIGH",
            "indicators": indicators + ["Sender address is missing a domain"],
        }

    local_part, domain = sender.split("@", 1)

    # Check for suspicious-looking words in the sender
    suspicious_words = [
        "verify",
        "security",
        "alert",
        "urgent",
        "support",
        "account",
    ]

    matched_words = [
        word for word in suspicious_words
        if word in local_part
    ]

    if matched_words:
        indicators.append(
            f"Sender contains security-related wording: {', '.join(matched_words)}"
        )
        score += 10

    # Check whether the domain is outside our safe fictional domains
    if domain not in SAFE_DOMAINS:
        indicators.append("Sender domain is outside the project's trusted test domains")
        score += 20

    # Check for excessive numbers in the sender
    if sum(char.isdigit() for char in local_part) >= 3:
        indicators.append("Sender contains multiple digits")
        score += 10

    # Keep score within 0-100
    score = min(score, 100)

    if score >= 50:
        risk_level = "HIGH"
    elif score >= 25:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "sender": sender,
        "score": score,
        "risk_level": risk_level,
        "indicators": indicators,
    }