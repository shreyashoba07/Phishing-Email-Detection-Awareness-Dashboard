URGENCY_WORDS = [
    "urgent",
    "immediately",
    "right now",
    "act now",
    "as soon as possible",
    "within 24 hours",
    "final warning",
    "action required",
]

CREDENTIAL_WORDS = [
    "password",
    "login",
    "username",
    "credentials",
    "verify your account",
    "confirm your account",
    "security code",
    "otp",
]

THREAT_WORDS = [
    "suspended",
    "blocked",
    "locked",
    "terminated",
    "deactivated",
    "penalty",
]


def analyze_content(subject, body):
    """
    Analyze email subject and body for common
    phishing-style language patterns.
    """

    subject = (subject or "").lower()
    body = (body or "").lower()

    text = f"{subject} {body}"

    indicators = []
    score = 0

    # Check urgency
    urgency_matches = [
        word for word in URGENCY_WORDS
        if word in text
    ]

    if urgency_matches:
        indicators.append(
            f"Urgency language detected: {', '.join(urgency_matches)}"
        )
        score += min(len(urgency_matches) * 10, 30)

    # Check credential/account requests
    credential_matches = [
        word for word in CREDENTIAL_WORDS
        if word in text
    ]

    if credential_matches:
        indicators.append(
            f"Credential/account-related wording detected: "
            f"{', '.join(credential_matches)}"
        )
        score += min(len(credential_matches) * 15, 40)

    # Check threatening language
    threat_matches = [
        word for word in THREAT_WORDS
        if word in text
    ]

    if threat_matches:
        indicators.append(
            f"Threatening account language detected: "
            f"{', '.join(threat_matches)}"
        )
        score += min(len(threat_matches) * 10, 20)

    # Check excessive exclamation marks
    if text.count("!") >= 3:
        indicators.append("Excessive exclamation marks detected")
        score += 5

    # Keep score between 0 and 100
    score = min(score, 100)

    if score >= 50:
        risk_level = "HIGH"
    elif score >= 25:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "score": score,
        "risk_level": risk_level,
        "indicators": indicators,
    }