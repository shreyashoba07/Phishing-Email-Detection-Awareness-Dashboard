# 🛡️ Phishing Email Detection & Awareness Dashboard

A hybrid cybersecurity application that analyzes emails for potential phishing indicators using **rule-based security analysis + machine learning** and presents the results through an interactive web dashboard.

> **Academic Project:** This project uses synthetic email data and safe test examples for educational and demonstration purposes. It is not intended for detecting or handling real-world phishing campaigns.

---

## 📌 Project Overview

Phishing emails are designed to trick users into revealing sensitive information, opening malicious attachments, or following unsafe links.

This project provides an educational dashboard that analyzes an email using multiple security signals:

* 📧 Sender analysis
* 📝 Email content analysis
* 🔗 URL analysis
* 📎 Attachment analysis
* 🤖 Machine learning prediction
* ⚠️ Risk scoring
* 📊 Security analytics
* 📜 Analysis history
* 🛡️ Phishing awareness guidance

The system combines traditional rule-based detection with a machine learning model to provide a more informative analysis.

---

## ✨ Features

### 🔍 Email Analysis

The application analyzes:

* Sender address
* Email subject
* Email body
* URLs
* File attachments

### 🛡️ Rule-Based Detection

The rule engine checks for common phishing indicators such as:

* Urgent language
* Account verification requests
* Credential-related wording
* Suspicious sender patterns
* Unsafe HTTP links
* Raw IP addresses in URLs
* Suspicious URL patterns
* Dangerous attachment extensions
* Double file extensions

### 🤖 Machine Learning Detection

The project uses:

* TF-IDF text vectorization
* Logistic Regression
* Synthetic phishing email dataset

The ML model predicts whether an email is likely to be phishing or legitimate.

### 🔀 Hybrid Detection

The final analysis combines:

```text
Rule-Based Risk Score → 60%
Machine Learning Score → 40%
```

The combined score is used to classify an email as:

* 🟢 LOW RISK
* 🟡 MEDIUM RISK
* 🔴 HIGH RISK

### 📊 Security Dashboard

The dashboard displays:

* Total analyzed emails
* High-risk emails
* Medium-risk emails
* Low-risk emails
* Phishing detections
* Legitimate detections
* ML model performance
* Confusion matrix
* Analysis history

### 📎 Email File Analysis

The backend supports safe analysis of:

* `.txt`
* `.eml`

files within the project's controlled testing environment.

---

## 🧠 Machine Learning Model

The ML pipeline uses:

```text
Email Subject + Email Body
            ↓
       Text Cleaning
            ↓
      TF-IDF Vectorizer
            ↓
    Logistic Regression
            ↓
 Phishing / Legitimate
```

### Dataset

The project includes a synthetic dataset containing:

* **500 total records**
* **250 phishing examples**
* **250 legitimate examples**

The dataset is intended for educational experimentation and does not represent real-world phishing traffic.

### Current Test Results

Using the project's deterministic 80/20 train-test split:

| Metric           | Result |
| ---------------- | -----: |
| Dataset Records  |    500 |
| Training Samples |    400 |
| Testing Samples  |    100 |
| Accuracy         |   100% |
| Precision        |   100% |
| Recall           |   100% |
| F1 Score         |   100% |

### Confusion Matrix

```text
                 Predicted
              Legitimate  Phishing

Actual
Legitimate       50          0

Phishing          0         50
```

> **Important:** These results are from a synthetic dataset and a single project test split. They should not be interpreted as real-world model performance.

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │      User Email      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   FastAPI Backend    │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       Sender Analysis   Content Analysis   URL Analysis
              │                │                │
              └────────────────┼────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Attachment Analysis  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Rule-Based Risk    │
                    │       Engine         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   ML Prediction      │
                    │ TF-IDF + Logistic     │
                    │     Regression       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Hybrid Detection   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   React Dashboard    │
                    └──────────────────────┘
```

---

## 🛠️ Technologies Used

### Frontend

* React
* Vite
* JavaScript
* CSS

### Backend

* Python
* FastAPI
* Uvicorn

### Machine Learning

* Scikit-learn
* Pandas
* NumPy
* TF-IDF
* Logistic Regression

### Database

* SQLite

### Other Libraries

* Joblib
* tldextract
* python-multipart

### Development Tools

* Visual Studio Code
* Git
* GitHub

---

## 📂 Project Structure

```text
Phishing-Email-Detection-Awareness-Dashboard/
│
├── backend/
│   ├── database.py
│   └── main.py
│
├── data/
│   ├── generate_dataset.py
│   └── phishing_email_dataset.csv
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── ml/
│   └── train_model.py
│
├── models/
│   ├── phishing_email_model.pkl
│   └── tfidf_vectorizer.pkl
│
├── src/
│   ├── attachment_analyzer.py
│   ├── content_analyzer.py
│   ├── email_analyzer.py
│   ├── hybrid_detector.py
│   ├── ml_predictor.py
│   ├── preprocessing.py
│   ├── risk_engine.py
│   ├── sender_analyzer.py
│   └── url_analyzer.py
│
├── tests/
├── docs/
├── reports/
├── screenshots/
├── .gitignore
└── README.md
```

---

## 🚀 How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/shreyashoba07/Phishing-Email-Detection-Awareness-Dashboard.git
```

```bash
cd Phishing-Email-Detection-Awareness-Dashboard
```

### 2. Create a Python Virtual Environment

```bash
py -m venv venv
```

### 3. Activate the Virtual Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Python Dependencies

```bash
pip install pandas numpy scikit-learn fastapi uvicorn joblib tldextract python-multipart
```

### 5. Train the ML Model

```bash
python ml/train_model.py
```

The trained model files will be saved inside:

```text
models/
```

### 6. Start the Backend

```bash
uvicorn backend.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

### 7. Start the Frontend

Open another terminal:

```powershell
cd frontend
```

Install frontend dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

Open the displayed local URL in your browser.

---

## 🔐 Security & Safety

This project is intentionally designed for safe academic experimentation.

It uses:

* Synthetic email data
* Safe test domains
* Controlled local analysis
* No real credential collection
* No real phishing campaigns
* No interaction with real targets

The system should not be used to send phishing emails, collect credentials, or test unauthorized systems.

---

## 🎯 Educational Objectives

This project demonstrates practical concepts in:

* Cybersecurity
* Phishing detection
* Natural language processing
* Machine learning
* Risk scoring
* REST APIs
* Full-stack development
* Database management
* Security awareness

---

## 🔮 Future Improvements

Possible future enhancements include:

* Larger and more diverse datasets
* More advanced NLP models
* Explainable AI
* Improved URL reputation analysis
* Domain age and reputation checks
* More attachment metadata analysis
* User authentication
* Role-based access control
* Advanced security analytics
* Deployment to a cloud platform
* Automated model evaluation on external benchmark datasets

---

## 👩‍💻 Project

**Phishing Email Detection & Awareness Dashboard**

Developed as an academic cybersecurity and machine learning project.

---

## ⚠️ Disclaimer

This project is intended for **educational and research purposes only**.

The dataset and test cases are synthetic. The reported machine learning metrics are specific to the included dataset and test split and do not establish real-world phishing detection accuracy.

Users are responsible for ensuring that any future testing or deployment is performed only on systems and data they are authorized to use.
