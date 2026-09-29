from src.email_analyzer import analyze_email
from src.ml_predictor import predict_email


def analyze_hybrid(sender, subject, body, attachment=""):
    """
    Combine rule-based detection and ML prediction.
    """

    # ------------------------------------------
    # 1. Rule-based analysis
    # ------------------------------------------

    rule_result = analyze_email(
        sender,
        subject,
        body,
        attachment
    )

    rule_score = rule_result["risk"]["risk_score"]


    # ------------------------------------------
    # 2. ML analysis
    # ------------------------------------------

    ml_result = predict_email(
        subject,
        body
    )

    ml_probability = ml_result["phishing_probability"]


    # ------------------------------------------
    # 3. Convert ML probability to score
    # ------------------------------------------

    ml_score = ml_probability


    # ------------------------------------------
    # 4. Combine both scores
    # ------------------------------------------

    hybrid_score = (
        rule_score * 0.60
        + ml_score * 0.40
    )

    hybrid_score = round(
        min(hybrid_score, 100),
        2
    )


    # ------------------------------------------
    # 5. Classification
    # ------------------------------------------

    if hybrid_score >= 70:
        classification = "HIGH RISK"

    elif hybrid_score >= 40:
        classification = "MEDIUM RISK"

    else:
        classification = "LOW RISK"


    # ------------------------------------------
    # 6. Recommendation
    # ------------------------------------------

    if classification == "HIGH RISK":

        recommendation = (
            "Do not open attachments or follow links. "
            "Verify the sender through a trusted channel."
        )

    elif classification == "MEDIUM RISK":

        recommendation = (
            "Be cautious. Verify the sender and email "
            "content before taking any action."
        )

    else:

        recommendation = (
            "No major phishing indicators detected. "
            "Continue following normal email security practices."
        )


    # ------------------------------------------
    # 7. Return hybrid result
    # ------------------------------------------

    return {
        "rule_based": {
            "risk_score": rule_score,
            "classification": rule_result["risk"]["classification"]
        },

        "ml_based": {
            "phishing_probability": ml_probability,
            "classification": ml_result["classification"]
        },

        "hybrid": {
            "risk_score": hybrid_score,
            "classification": classification,
            "recommendation": recommendation
        },

        "indicators": rule_result["risk"]["indicators"]
    }