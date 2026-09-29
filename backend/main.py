from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from email import policy
from email.parser import BytesParser
import re

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

from src.hybrid_detector import analyze_hybrid
from backend.database import create_table, get_connection


# --------------------------------------------------
# FastAPI Application
# --------------------------------------------------

app = FastAPI(
    title="Phishing Email Detection API",
    description="AI-powered phishing email detection and awareness API",
    version="1.0.0",
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Database
# --------------------------------------------------

create_table()


# --------------------------------------------------
# Request Model
# --------------------------------------------------

class EmailRequest(BaseModel):
    sender: str
    subject: str
    body: str
    attachment: str = ""


# --------------------------------------------------
# Sender Normalization
# --------------------------------------------------

def normalize_sender(sender):
    sender = (sender or "").strip()

    if not sender:
        return ""

    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(email_pattern, sender)

    if match:
        return match.group(0)

    return sender


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Phishing Email Detection API is running!"
    }


# --------------------------------------------------
# ML Model Metrics
# --------------------------------------------------

@app.get("/ml-metrics")
def get_ml_metrics():

    dataset_path = "data/phishing_email_dataset.csv"
    model_path = "models/phishing_email_model.pkl"
    vectorizer_path = "models/tfidf_vectorizer.pkl"

    try:
        df = pd.read_csv(dataset_path)

        df["text"] = (
            df["subject"].fillna("")
            + " "
            + df["body_text"].fillna("")
        )

        X = df["text"]
        y = df["label"]

        _, X_test, _, y_test = train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y,
        )

        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)

        X_test_tfidf = vectorizer.transform(X_test)

        predictions = model.predict(X_test_tfidf)

        accuracy = accuracy_score(y_test, predictions)
        precision = precision_score(
            y_test,
            predictions,
            zero_division=0,
        )
        recall = recall_score(
            y_test,
            predictions,
            zero_division=0,
        )
        f1 = f1_score(
            y_test,
            predictions,
            zero_division=0,
        )

        matrix = confusion_matrix(
            y_test,
            predictions,
        )

        return {
            "dataset_records": int(len(df)),
            "training_samples": int(len(df) - len(X_test)),
            "testing_samples": int(len(X_test)),
            "accuracy": round(float(accuracy) * 100, 2),
            "precision": round(float(precision) * 100, 2),
            "recall": round(float(recall) * 100, 2),
            "f1_score": round(float(f1) * 100, 2),
            "confusion_matrix": matrix.tolist(),
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Could not calculate ML metrics: {error}",
        )


# --------------------------------------------------
# Save Analysis
# --------------------------------------------------

def save_analysis(request, result):

    connection = get_connection()
    cursor = connection.cursor()

    clean_sender = normalize_sender(request.sender)

    cursor.execute(
        """
        INSERT INTO email_analysis (
            sender,
            subject,
            risk_score,
            classification,
            ml_classification,
            phishing_probability,
            recommendation
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            clean_sender,
            request.subject,
            result["hybrid"]["risk_score"],
            result["hybrid"]["classification"],
            result["ml_based"]["classification"],
            result["ml_based"]["phishing_probability"],
            result["hybrid"]["recommendation"],
        ),
    )

    connection.commit()
    connection.close()


# --------------------------------------------------
# Analyze Normal Email
# --------------------------------------------------

@app.post("/analyze")
def analyze_email(request: EmailRequest):

    clean_sender = normalize_sender(request.sender)

    result = analyze_hybrid(
        sender=clean_sender,
        subject=request.subject,
        body=request.body,
        attachment=request.attachment,
    )

    clean_request = EmailRequest(
        sender=clean_sender,
        subject=request.subject,
        body=request.body,
        attachment=request.attachment,
    )

    save_analysis(clean_request, result)

    return result


# --------------------------------------------------
# Analyze Uploaded TXT / EML File
# --------------------------------------------------

@app.post("/analyze-file")
async def analyze_file(file: UploadFile = File(...)):

    filename = file.filename or ""

    if not filename.lower().endswith((".txt", ".eml")):
        raise HTTPException(
            status_code=400,
            detail="Only .txt and .eml files are supported.",
        )

    file_data = await file.read()

    if len(file_data) > 1_000_000:
        raise HTTPException(
            status_code=400,
            detail="File is too large. Maximum size is 1 MB.",
        )

    sender = ""
    subject = ""
    body = ""

    # --------------------------------------------------
    # EML
    # --------------------------------------------------

    if filename.lower().endswith(".eml"):

        try:

            message = BytesParser(
                policy=policy.default
            ).parsebytes(file_data)

            sender = message.get("From", "")
            subject = message.get("Subject", "")

            if message.is_multipart():

                parts = []

                for part in message.walk():

                    if part.get_content_type() == "text/plain":

                        try:
                            parts.append(part.get_content())
                        except Exception:
                            pass

                body = "\n".join(parts)

            else:

                try:
                    body = message.get_content()
                except Exception:
                    body = file_data.decode(
                        "utf-8",
                        errors="ignore",
                    )

        except Exception as error:

            raise HTTPException(
                status_code=400,
                detail=f"Could not parse EML file: {error}",
            )

    # --------------------------------------------------
    # TXT
    # --------------------------------------------------

    else:

        body = file_data.decode(
            "utf-8",
            errors="ignore",
        )

        lines = body.splitlines()
        remaining_lines = []

        for line in lines:

            lower_line = line.lower()

            if lower_line.startswith("from:"):
                sender = line[5:].strip()

            elif lower_line.startswith("subject:"):
                subject = line[8:].strip()

            else:
                remaining_lines.append(line)

        body = "\n".join(
            remaining_lines
        ).strip()

    # --------------------------------------------------
    # Normalize sender
    # --------------------------------------------------

    sender = normalize_sender(sender)

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    if not subject and not body:

        raise HTTPException(
            status_code=400,
            detail="The uploaded file does not contain readable email content.",
        )

    # --------------------------------------------------
    # Detection
    # --------------------------------------------------

    result = analyze_hybrid(
        sender=sender,
        subject=subject,
        body=body,
        attachment="",
    )

    # --------------------------------------------------
    # Save
    # --------------------------------------------------

    request = EmailRequest(
        sender=sender,
        subject=subject,
        body=body,
        attachment="",
    )

    save_analysis(request, result)

    return {
        "filename": filename,
        "sender": sender,
        "subject": subject,
        "result": result,
    }


# --------------------------------------------------
# History
# --------------------------------------------------

@app.get("/history")
def get_history():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            sender,
            subject,
            risk_score,
            classification,
            ml_classification,
            phishing_probability,
            recommendation
        FROM email_analysis
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    history = []

    for row in rows:

        record = dict(row)

        record["sender"] = normalize_sender(
            record.get("sender", "")
        )

        history.append(record)

    return {
        "total_records": len(history),
        "history": history,
    }


# --------------------------------------------------
# Dashboard Statistics
# --------------------------------------------------

@app.get("/stats")
def get_statistics():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM email_analysis
        """
    )

    total = cursor.fetchone()["total"]

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM email_analysis
        WHERE classification = 'HIGH RISK'
        """
    )

    high_risk = cursor.fetchone()["count"]

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM email_analysis
        WHERE classification = 'MEDIUM RISK'
        """
    )

    medium_risk = cursor.fetchone()["count"]

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM email_analysis
        WHERE classification = 'LOW RISK'
        """
    )

    low_risk = cursor.fetchone()["count"]

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM email_analysis
        WHERE ml_classification = 'PHISHING'
        """
    )

    phishing = cursor.fetchone()["count"]

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM email_analysis
        WHERE ml_classification = 'LEGITIMATE'
        """
    )

    legitimate = cursor.fetchone()["count"]

    connection.close()

    return {
        "total_analyses": total,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk,
        "phishing": phishing,
        "legitimate": legitimate,
    }