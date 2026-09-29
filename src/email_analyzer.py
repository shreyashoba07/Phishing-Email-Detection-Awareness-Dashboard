from src.preprocessing import preprocess_email
from src.sender_analyzer import analyze_sender
from src.content_analyzer import analyze_content
from src.url_analyzer import analyze_url
from src.attachment_analyzer import analyze_attachment
from src.risk_engine import calculate_risk


def generate_recommendation(classification):
    if classification == "HIGH RISK":
        return (
            "Do not open attachments or follow links. "
            "Verify the sender through a trusted channel."
        )

    if classification == "MEDIUM RISK":
        return (
            "Be cautious. Verify the sender and email content "
            "before taking any action."
        )

    return (
        "No major phishing indicators detected. "
        "Continue following normal email security practices."
    )


def analyze_email(sender, subject, body, attachment=""):

    # Step 1: Preprocess email
    processed = preprocess_email(subject, body)

    # Step 2: Analyze sender
    sender_result = analyze_sender(sender)

    # Step 3: Analyze content
    content_result = analyze_content(
        processed["subject"],
        processed["body"]
    )

    # Step 4: Analyze URLs
    url_results = [
        analyze_url(url)
        for url in processed["urls"]
    ]

    # Step 5: Analyze attachment
    attachment_result = analyze_attachment(attachment)

    # Step 6: Calculate overall risk
    risk_result = calculate_risk(
        sender_result,
        content_result,
        url_results,
        attachment_result
    )

    # Step 7: Generate recommendation
    recommendation = generate_recommendation(
        risk_result["classification"]
    )

    # Step 8: Return complete analysis
    return {
        "sender": sender_result,
        "content": content_result,
        "urls": url_results,
        "attachment": attachment_result,
        "risk": risk_result,
        "recommendation": recommendation
    }