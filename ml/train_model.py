import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


# ==========================================
# 1. Load the dataset
# ==========================================

df = pd.read_csv("data/phishing_email_dataset.csv")

print("Dataset loaded successfully!")
print("Total records:", len(df))


# ==========================================
# 2. Combine subject and email body
# ==========================================

df["text"] = (
    df["subject"].fillna("") + " " +
    df["body_text"].fillna("")
)


# ==========================================
# 3. Define input and target
# ==========================================

X = df["text"]
y = df["label"]


# ==========================================
# 4. Split dataset into training and testing
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==========================================
# 5. Convert text into TF-IDF features
# ==========================================

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english"
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print("TF-IDF feature extraction completed!")


# ==========================================
# 6. Create Logistic Regression model
# ==========================================

model = LogisticRegression(
    max_iter=1000,
    random_state=42
)


# ==========================================
# 7. Train the model
# ==========================================

model.fit(X_train_tfidf, y_train)

print("Model training completed!")


# ==========================================
# 8. Make predictions
# ==========================================

y_pred = model.predict(X_test_tfidf)


# ==========================================
# 9. Calculate evaluation metrics
# ==========================================

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)


# ==========================================
# 10. Display evaluation results
# ==========================================

print("\n==========================================")
print("        MODEL EVALUATION RESULTS")
print("==========================================")

print(f"Accuracy :  {accuracy:.4f}")
print(f"Precision:  {precision:.4f}")
print(f"Recall   :  {recall:.4f}")
print(f"F1-Score :  {f1:.4f}")


# ==========================================
# 11. Confusion Matrix
# ==========================================

cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:")
print(cm)


# ==========================================
# 12. Classification Report
# ==========================================

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=["Legitimate", "Phishing"],
        zero_division=0
    )
)


# ==========================================
# 13. Save the trained model
# ==========================================

joblib.dump(
    model,
    "models/phishing_email_model.pkl"
)


# ==========================================
# 14. Save the TF-IDF vectorizer
# ==========================================

joblib.dump(
    vectorizer,
    "models/tfidf_vectorizer.pkl"
)

print("\nModel and vectorizer saved successfully!")