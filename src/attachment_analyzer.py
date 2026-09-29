DANGEROUS_EXTENSIONS = {
    ".exe",
    ".scr",
    ".bat",
    ".cmd",
    ".ps1",
    ".vbs",
    ".js",
    ".msi",
}


def analyze_attachment(filename):
    """
    Safely analyze an attachment filename.
    The file is not opened or executed.
    """

    filename = (filename or "").strip().lower()

    if not filename:
        return {
            "filename": "",
            "score": 0,
            "risk_level": "LOW",
            "indicators": ["No attachment provided"],
        }

    indicators = []
    score = 0

    # Find the final file extension
    extension = ""

    if "." in filename:
        extension = "." + filename.rsplit(".", 1)[1]

    # Check for potentially dangerous executable/script extensions
    if extension in DANGEROUS_EXTENSIONS:
        indicators.append(
            f"Potentially dangerous attachment type: {extension}"
        )
        score += 60

    # Check for double extensions such as document.pdf.exe
    if filename.count(".") >= 2:
        indicators.append("Multiple file extensions detected")
        score += 20

    score = min(score, 100)

    if score >= 50:
        risk_level = "HIGH"
    elif score >= 25:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "filename": filename,
        "score": score,
        "risk_level": risk_level,
        "indicators": indicators,
    }