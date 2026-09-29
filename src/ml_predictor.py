import joblib


# Load the trained ML model
model = joblib.load("models/phishing_email_model.pkl")

# Load the TF-IDF vectorizer
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")


def predict_email(subject, body):
    """
    Predict whether an email is legitimate or phishing.
    """

    # Combine subject and body
    text = f"{subject or ''} {body or ''}".strip()

    # Convert email text into TF-IDF features
    text_tfidf = vectorizer.transform([text])

    # Make prediction
    prediction = model.predict(text_tfidf)[0]

    # Get prediction probability
    probabilities = model.predict_proba(text_tfidf)[0]

    # Probability of phishing (label 1)
    phishing_probability = probabilities[1]

    # Convert prediction to readable classification
    if prediction == 1:
        classification = "PHISHING"
    else:
        classification = "LEGITIMATE"

    return {
        "prediction": int(prediction),
        "classification": classification,
        "phishing_probability": round(
            float(phishing_probability) * 100,
            2
        )
    }