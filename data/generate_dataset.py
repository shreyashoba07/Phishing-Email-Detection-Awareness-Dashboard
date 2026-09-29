import csv
import random
from pathlib import Path

OUTPUT_FILE = Path(__file__).parent / "phishing_email_dataset.csv"

PHISHING_TEMPLATES = [
    {
        "subject": "URGENT: Verify Your Account",
        "sender": "security-alert@example.net",
        "body": "Your account requires immediate verification. Please confirm your information.",
        "url": "http://verify-account.invalid.test/login",
    },
    {
        "subject": "Your Account Will Be Suspended",
        "sender": "support-alert@example.com",
        "body": "We detected unusual activity. Verify your account immediately to avoid suspension.",
        "url": "http://account-check.invalid.test/verify",
    },
    {
        "subject": "Payment Verification Required",
        "sender": "billing@example.org",
        "body": "Your recent payment requires verification. Please review your account urgently.",
        "url": "http://payment-check.invalid.test/confirm",
    },
    {
        "subject": "Security Alert - Action Required",
        "sender": "security@example.net",
        "body": "Your account has triggered a security alert. Confirm your details now.",
        "url": "http://198.51.100.10/security-check",
    },
]

LEGITIMATE_TEMPLATES = [
    {
        "subject": "Cybersecurity Workshop Reminder",
        "sender": "training@example.org",
        "body": "This is a reminder about the upcoming cybersecurity workshop. Please attend at the scheduled time.",
        "url": "https://example.org/workshop",
    },
    {
        "subject": "Team Meeting Schedule",
        "sender": "team@example.com",
        "body": "The weekly team meeting will take place tomorrow. Please review the agenda before attending.",
        "url": "https://example.com/meetings",
    },
    {
        "subject": "Project Update",
        "sender": "project@example.net",
        "body": "The project documentation has been updated. Please review the latest information when convenient.",
        "url": "https://example.net/project",
    },
    {
        "subject": "Training Material Available",
        "sender": "learning@example.org",
        "body": "The training material is now available. You can review it using the normal learning portal.",
        "url": "https://example.org/training",
    },
]


def create_record(template, label):
    return {
        "subject": template["subject"],
        "from": template["sender"],
        "to": "student@example.org",
        "date": "2026-09-29",
        "body_text": template["body"],
        "urls": template["url"],
        "label": label,
    }


def generate_dataset(total_records=500):
    records = []

    phishing_count = total_records // 2
    legitimate_count = total_records - phishing_count

    for _ in range(phishing_count):
        template = random.choice(PHISHING_TEMPLATES)
        records.append(create_record(template, 1))

    for _ in range(legitimate_count):
        template = random.choice(LEGITIMATE_TEMPLATES)
        records.append(create_record(template, 0))

    random.shuffle(records)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "subject",
            "from",
            "to",
            "date",
            "body_text",
            "urls",
            "label",
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Dataset created successfully!")
    print(f"Total records: {len(records)}")
    print(f"Phishing records: {phishing_count}")
    print(f"Legitimate records: {legitimate_count}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_dataset(500)