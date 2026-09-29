import re
from urllib.parse import urlparse


SUSPICIOUS_TLDS = {
    "zip",
    "mov",
    "click",
    "work",
    "country",
}


def analyze_url(url):
    """
    Analyze a URL without visiting or connecting to it.
    """

    url = (url or "").strip()

    indicators = []
    score = 0

    if not url:
        return {
            "url": url,
            "score": 0,
            "risk_level": "LOW",
            "indicators": [],
        }

    parsed = urlparse(url)

    # Check HTTP instead of HTTPS
    if parsed.scheme.lower() == "http":
        indicators.append("URL uses HTTP instead of HTTPS")
        score += 15

    # Check whether hostname looks like an IP address
    hostname = parsed.hostname or ""

    ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}$"

    if re.match(ip_pattern, hostname):
        indicators.append("URL uses a raw IP address")
        score += 30

    # Extract domain/TLD
    domain_parts = hostname.lower().split(".")

    if len(domain_parts) >= 2:
        tld = domain_parts[-1]

        if tld in SUSPICIOUS_TLDS:
            indicators.append(
                f"Suspicious-looking top-level domain: .{tld}"
            )
            score += 20

    # Check for suspicious URL keywords
    suspicious_words = [
        "login",
        "verify",
        "account",
        "password",
        "confirm",
        "secure",
    ]

    matched_words = [
        word for word in suspicious_words
        if word in url.lower()
    ]

    if matched_words:
        indicators.append(
            f"Sensitive-action wording in URL: {', '.join(matched_words)}"
        )
        score += min(len(matched_words) * 10, 30)

    # Limit score
    score = min(score, 100)

    if score >= 50:
        risk_level = "HIGH"
    elif score >= 25:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "url": url,
        "score": score,
        "risk_level": risk_level,
        "indicators": indicators,
    }