def calculate_risk(
    sender_result,
    content_result,
    url_results,
    attachment_result
):
    """
    Combine individual analyzer results into one
    explainable phishing risk score.
    """

    sender_score = sender_result.get("score", 0)
    content_score = content_result.get("score", 0)
    attachment_score = attachment_result.get("score", 0)

    # Use the highest URL score when multiple URLs exist
    url_score = 0

    for result in url_results:
        url_score = max(
            url_score,
            result.get("score", 0)
        )

    # Weighted base score
    base_score = (
        sender_score * 0.20
        + content_score * 0.30
        + url_score * 0.35
        + attachment_score * 0.15
    )

    # Additional bonus for multiple strong indicators
    high_risk_components = 0

    if content_score >= 30:
        high_risk_components += 1

    if url_score >= 50:
        high_risk_components += 1

    if attachment_score >= 50:
        high_risk_components += 1

    # Multiple independent high-risk signals increase confidence
    combination_bonus = high_risk_components * 10

    overall_score = base_score + combination_bonus

    overall_score = round(min(overall_score, 100), 2)

    # Overall classification
    if overall_score >= 70:
        classification = "HIGH RISK"
    elif overall_score >= 40:
        classification = "MEDIUM RISK"
    else:
        classification = "LOW RISK"

    # Combine all indicators
    indicators = []

    indicators.extend(
        sender_result.get("indicators", [])
    )

    indicators.extend(
        content_result.get("indicators", [])
    )

    for result in url_results:
        indicators.extend(
            result.get("indicators", [])
        )

    indicators.extend(
        attachment_result.get("indicators", [])
    )

    return {
        "risk_score": overall_score,
        "classification": classification,
        "indicators": indicators,
    }