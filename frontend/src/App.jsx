import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [sender, setSender] = useState("");
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [attachment, setAttachment] = useState("");

  const [selectedFile, setSelectedFile] = useState(null);

  const [result, setResult] = useState(null);
  const [stats, setStats] = useState(null);
  const [history, setHistory] = useState([]);
  const [mlMetrics, setMlMetrics] = useState(null);

  const [loading, setLoading] = useState(false);
  const [uploadLoading, setUploadLoading] = useState(false);
  const [metricsLoading, setMetricsLoading] = useState(true);

  // --------------------------------------------------
  // Load Dashboard Data
  // --------------------------------------------------

  const loadDashboard = async () => {
    try {
      const statsResponse = await fetch(`${API_URL}/stats`);
      const statsData = await statsResponse.json();

      const historyResponse = await fetch(`${API_URL}/history`);
      const historyData = await historyResponse.json();

      setStats(statsData);
      setHistory(historyData.history || []);
    } catch (error) {
      console.error("Dashboard loading error:", error);
    }
  };

  // --------------------------------------------------
  // Load ML Metrics
  // --------------------------------------------------

  const loadMlMetrics = async () => {
    setMetricsLoading(true);

    try {
      const response = await fetch(`${API_URL}/ml-metrics`);

      if (!response.ok) {
        throw new Error("Could not load ML metrics");
      }

      const data = await response.json();

      setMlMetrics(data);
    } catch (error) {
      console.error("ML metrics loading error:", error);
      setMlMetrics(null);
    } finally {
      setMetricsLoading(false);
    }
  };

  // --------------------------------------------------
  // Initial Dashboard Load
  // --------------------------------------------------

  useEffect(() => {
    loadDashboard();
    loadMlMetrics();
  }, []);

  // --------------------------------------------------
  // Analyze Manual Email
  // --------------------------------------------------

  const analyzeEmail = async () => {
    if (!sender.trim() || !subject.trim() || !body.trim()) {
      alert("Please enter sender, subject and email body.");
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          sender: sender.trim(),
          subject: subject.trim(),
          body: body.trim(),
          attachment: attachment.trim(),
        }),
      });

      if (!response.ok) {
        throw new Error("Analysis failed");
      }

      const data = await response.json();

      setResult({
        type: "manual",
        result: data,
      });

      await loadDashboard();
    } catch (error) {
      console.error(error);

      alert(
        "Could not connect to the backend. Make sure FastAPI is running on port 8000."
      );
    } finally {
      setLoading(false);
    }
  };

  // --------------------------------------------------
  // File Selection
  // --------------------------------------------------

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (!file) {
      setSelectedFile(null);
      return;
    }

    const fileName = file.name.toLowerCase();

    if (!fileName.endsWith(".txt") && !fileName.endsWith(".eml")) {
      alert("Only .txt and .eml files are supported.");
      event.target.value = "";
      setSelectedFile(null);
      return;
    }

    if (file.size > 1000000) {
      alert("File is too large. Maximum size is 1 MB.");
      event.target.value = "";
      setSelectedFile(null);
      return;
    }

    setSelectedFile(file);
  };

  // --------------------------------------------------
  // Analyze Uploaded File
  // --------------------------------------------------

  const analyzeUploadedFile = async () => {
    if (!selectedFile) {
      alert("Please select a .txt or .eml file first.");
      return;
    }

    setUploadLoading(true);
    setResult(null);

    try {
      const formData = new FormData();

      formData.append("file", selectedFile);

      const response = await fetch(`${API_URL}/analyze-file`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "File analysis failed");
      }

      setResult({
        type: "file",
        filename: data.filename,
        sender: data.sender,
        subject: data.subject,
        result: data.result,
      });

      await loadDashboard();
    } catch (error) {
      console.error(error);

      alert(
        error.message || "Could not analyze the uploaded file."
      );
    } finally {
      setUploadLoading(false);
    }
  };

  // --------------------------------------------------
  // Clear Form
  // --------------------------------------------------

  const clearForm = () => {
    setSender("");
    setSubject("");
    setBody("");
    setAttachment("");
    setResult(null);
    setSelectedFile(null);

    const fileInput = document.getElementById("email-file");

    if (fileInput) {
      fileInput.value = "";
    }
  };

  // --------------------------------------------------
  // Dashboard Calculations
  // --------------------------------------------------

  const totalAnalyses = stats?.total_analyses || 0;

  const highRiskPercentage =
    totalAnalyses > 0
      ? (stats.high_risk / totalAnalyses) * 100
      : 0;

  const mediumRiskPercentage =
    totalAnalyses > 0
      ? (stats.medium_risk / totalAnalyses) * 100
      : 0;

  const lowRiskPercentage =
    totalAnalyses > 0
      ? (stats.low_risk / totalAnalyses) * 100
      : 0;

  const analyzedResult = result?.result;

  return (
    <div className="app">

      {/* ==================================================
          HEADER
      ================================================== */}

      <header className="header">

        <div className="header-content">

          <div>

            <h1>
              Phishing Email Detection
            </h1>

            <p>
              AI-Powered Email Security & Awareness Dashboard
            </p>

          </div>

          <div className="status-badge">
            ● API Connected
          </div>

        </div>

      </header>


      <main className="container">

        {/* ==================================================
            STATISTICS
        ================================================== */}

        <section className="stats-grid">

          <div className="stat-card">

            <h3>
              Total Analyses
            </h3>

            <div className="stat-number">
              {stats?.total_analyses ?? 0}
            </div>

          </div>


          <div className="stat-card">

            <h3>
              High Risk
            </h3>

            <div className="stat-number">
              {stats?.high_risk ?? 0}
            </div>

          </div>


          <div className="stat-card">

            <h3>
              Medium Risk
            </h3>

            <div className="stat-number">
              {stats?.medium_risk ?? 0}
            </div>

          </div>


          <div className="stat-card">

            <h3>
              Low Risk
            </h3>

            <div className="stat-number">
              {stats?.low_risk ?? 0}
            </div>

          </div>


          <div className="stat-card">

            <h3>
              Phishing
            </h3>

            <div className="stat-number">
              {stats?.phishing ?? 0}
            </div>

          </div>


          <div className="stat-card">

            <h3>
              Legitimate
            </h3>

            <div className="stat-number">
              {stats?.legitimate ?? 0}
            </div>

          </div>

        </section>


        {/* ==================================================
            SECURITY ANALYTICS
        ================================================== */}

        <section className="card analytics-section">

          <div className="section-title">

            <h2>
              Security Analytics
            </h2>

            <p>
              Overview of detected email risks and phishing activity.
            </p>

          </div>


          <div className="analytics-grid">

            {/* Risk Distribution */}

            <div className="analytics-card">

              <h3>
                Risk Distribution
              </h3>


              <div className="analytics-row">

                <div className="analytics-label">

                  <span>
                    High Risk
                  </span>

                  <strong>
                    {stats?.high_risk || 0}
                  </strong>

                </div>


                <div className="analytics-track">

                  <div
                    className="analytics-fill high-fill"
                    style={{
                      width: `${highRiskPercentage}%`,
                    }}
                  />

                </div>

              </div>


              <div className="analytics-row">

                <div className="analytics-label">

                  <span>
                    Medium Risk
                  </span>

                  <strong>
                    {stats?.medium_risk || 0}
                  </strong>

                </div>


                <div className="analytics-track">

                  <div
                    className="analytics-fill medium-fill"
                    style={{
                      width: `${mediumRiskPercentage}%`,
                    }}
                  />

                </div>

              </div>


              <div className="analytics-row">

                <div className="analytics-label">

                  <span>
                    Low Risk
                  </span>

                  <strong>
                    {stats?.low_risk || 0}
                  </strong>

                </div>


                <div className="analytics-track">

                  <div
                    className="analytics-fill low-fill"
                    style={{
                      width: `${lowRiskPercentage}%`,
                    }}
                  />

                </div>

              </div>

            </div>


            {/* Detection Summary */}

            <div className="analytics-card">

              <h3>
                Detection Summary
              </h3>


              <div className="summary-item">

                <span>
                  Phishing Detected
                </span>

                <strong>
                  {stats?.phishing || 0}
                </strong>

              </div>


              <div className="summary-item">

                <span>
                  Legitimate Emails
                </span>

                <strong>
                  {stats?.legitimate || 0}
                </strong>

              </div>


              <div className="summary-item">

                <span>
                  Total Analyses
                </span>

                <strong>
                  {stats?.total_analyses || 0}
                </strong>

              </div>

            </div>


            {/* Security Overview */}

            <div className="analytics-card">

              <h3>
                Security Overview
              </h3>


              <div className="security-overview">

                <div className="security-number">
                  {stats?.phishing || 0}
                </div>

                <p>
                  Phishing emails detected
                </p>

              </div>


              <p className="analytics-note">

                The system combines rule-based analysis,
                machine learning and hybrid scoring to
                identify suspicious email characteristics.

              </p>

            </div>

          </div>

        </section>


        {/* ==================================================
            ML MODEL PERFORMANCE
        ================================================== */}

        <section className="card ml-performance-section">

          <div className="section-title">

            <h2>
              ML Model Performance
            </h2>

            <p>
              Performance metrics of the phishing email
              classification model on the synthetic test dataset.
            </p>

          </div>


          {metricsLoading ? (

            <div className="ml-loading">

              <p>
                Loading model performance...
              </p>

            </div>

          ) : mlMetrics ? (

            <>

              {/* Dataset Information */}

              <div className="ml-dataset-info">

                <div className="ml-info-card">

                  <span>
                    Dataset Records
                  </span>

                  <strong>
                    {mlMetrics.dataset_records}
                  </strong>

                </div>


                <div className="ml-info-card">

                  <span>
                    Training Samples
                  </span>

                  <strong>
                    {mlMetrics.training_samples}
                  </strong>

                </div>


                <div className="ml-info-card">

                  <span>
                    Testing Samples
                  </span>

                  <strong>
                    {mlMetrics.testing_samples}
                  </strong>

                </div>

              </div>


              {/* Performance Metrics */}

              <div className="ml-metrics-grid">

                <div className="ml-metric-card">

                  <h3>
                    Accuracy
                  </h3>

                  <div className="ml-metric-value">
                    {mlMetrics.accuracy}%
                  </div>

                  <p>
                    Overall correct predictions
                  </p>

                </div>


                <div className="ml-metric-card">

                  <h3>
                    Precision
                  </h3>

                  <div className="ml-metric-value">
                    {mlMetrics.precision}%
                  </div>

                  <p>
                    Correct phishing predictions
                  </p>

                </div>


                <div className="ml-metric-card">

                  <h3>
                    Recall
                  </h3>

                  <div className="ml-metric-value">
                    {mlMetrics.recall}%
                  </div>

                  <p>
                    Phishing emails correctly detected
                  </p>

                </div>


                <div className="ml-metric-card">

                  <h3>
                    F1-Score
                  </h3>

                  <div className="ml-metric-value">
                    {mlMetrics.f1_score}%
                  </div>

                  <p>
                    Balance of precision and recall
                  </p>

                </div>

              </div>


              {/* Confusion Matrix */}

              <div className="confusion-section">

                <h3>
                  Confusion Matrix
                </h3>

                <p className="matrix-description">
                  The matrix shows the model's predictions
                  compared with the actual labels.
                </p>


                <div className="confusion-matrix">

                  <div className="matrix-corner">
                    Actual / Predicted
                  </div>

                  <div className="matrix-header">
                    Legitimate
                  </div>

                  <div className="matrix-header">
                    Phishing
                  </div>


                  <div className="matrix-row-label">
                    Legitimate
                  </div>

                  <div className="matrix-cell">
                    {mlMetrics.confusion_matrix[0][0]}
                  </div>

                  <div className="matrix-cell">
                    {mlMetrics.confusion_matrix[0][1]}
                  </div>


                  <div className="matrix-row-label">
                    Phishing
                  </div>

                  <div className="matrix-cell">
                    {mlMetrics.confusion_matrix[1][0]}
                  </div>

                  <div className="matrix-cell">
                    {mlMetrics.confusion_matrix[1][1]}
                  </div>

                </div>


                <div className="matrix-legend">

                  <span>
                    <strong>True Negative:</strong>{" "}
                    {mlMetrics.confusion_matrix[0][0]}
                  </span>

                  <span>
                    <strong>False Positive:</strong>{" "}
                    {mlMetrics.confusion_matrix[0][1]}
                  </span>

                  <span>
                    <strong>False Negative:</strong>{" "}
                    {mlMetrics.confusion_matrix[1][0]}
                  </span>

                  <span>
                    <strong>True Positive:</strong>{" "}
                    {mlMetrics.confusion_matrix[1][1]}
                  </span>

                </div>

              </div>


              <div className="ml-note">

                <strong>
                  Note:
                </strong>{" "}

                These metrics are based on the project's
                synthetic 500-record dataset and its current
                test split. They should not be interpreted as
                real-world phishing detection performance.

              </div>

            </>

          ) : (

            <div className="ml-error">

              <h3>
                ML metrics unavailable
              </h3>

              <p>
                Make sure the FastAPI backend is running and
                the trained model files are available.
              </p>

            </div>

          )}

        </section>


        {/* ==================================================
            EMAIL ANALYZER
        ================================================== */}

        <section className="card">

          <div className="section-title">

            <h2>
              Analyze an Email
            </h2>

            <p>
              Enter a safe sample email to analyze phishing indicators.
            </p>

          </div>


          <div className="form-group">

            <label>
              Sender Email
            </label>

            <input
              type="email"
              placeholder="security-alert@example.net"
              value={sender}
              onChange={(e) => setSender(e.target.value)}
            />

          </div>


          <div className="form-group">

            <label>
              Subject
            </label>

            <input
              type="text"
              placeholder="URGENT: Verify Your Account"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
            />

          </div>


          <div className="form-group">

            <label>
              Email Body
            </label>

            <textarea
              rows="7"
              placeholder="Enter the email body here..."
              value={body}
              onChange={(e) => setBody(e.target.value)}
            />

          </div>


          <div className="form-group">

            <label>

              Attachment Name

              <span className="optional">
                {" "} (Optional)
              </span>

            </label>

            <input
              type="text"
              placeholder="invoice.pdf.exe"
              value={attachment}
              onChange={(e) => setAttachment(e.target.value)}
            />

          </div>


          <div className="button-row">

            <button
              className="primary-button"
              onClick={analyzeEmail}
              disabled={loading}
            >

              {loading
                ? "Analyzing..."
                : "Analyze Email"}

            </button>


            <button
              className="secondary-button"
              onClick={clearForm}
            >
              Clear
            </button>

          </div>

        </section>


        {/* ==================================================
            FILE UPLOAD
        ================================================== */}

        <section className="card upload-card">

          <div className="section-title">

            <h2>
              Upload Email File
            </h2>

            <p>

              Upload a safe local{" "}
              <strong>.txt</strong> or{" "}
              <strong>.eml</strong> email file for analysis.

            </p>

          </div>


          <div className="upload-box">

            <input
              id="email-file"
              type="file"
              accept=".txt,.eml"
              onChange={handleFileChange}
            />


            {selectedFile && (

              <div className="selected-file">

                <strong>
                  Selected file:
                </strong>{" "}

                {selectedFile.name}

                <br />

                <span>
                  Size:{" "}
                  {(selectedFile.size / 1024).toFixed(2)}
                  {" "}KB
                </span>

              </div>

            )}


            <button
              className="primary-button"
              onClick={analyzeUploadedFile}
              disabled={!selectedFile || uploadLoading}
            >

              {uploadLoading
                ? "Analyzing File..."
                : "Upload & Analyze"}

            </button>

          </div>


          <div className="upload-note">

            <strong>
              Safety:
            </strong>{" "}

            Files are parsed by the local application.
            URLs inside emails are analyzed as text
            and are not opened or executed.

          </div>

        </section>


        {/* ==================================================
            ANALYSIS RESULT
        ================================================== */}

        {analyzedResult && (

          <section className="card result-section">

            <div className="section-title">

              <h2>
                Analysis Result
              </h2>


              {result.type === "file" && (

                <div className="file-result-info">

                  <p>
                    <strong>
                      File:
                    </strong>{" "}
                    {result.filename}
                  </p>

                  <p>
                    <strong>
                      Sender:
                    </strong>{" "}
                    {result.sender || "Not detected"}
                  </p>

                  <p>
                    <strong>
                      Subject:
                    </strong>{" "}
                    {result.subject || "Not detected"}
                  </p>

                </div>

              )}

            </div>


            <div className="result-grid">

              <div className="result-card">

                <h3>
                  Rule-Based Score
                </h3>

                <div className="result-value">
                  {analyzedResult.rule_based.risk_score}
                </div>

                <p>
                  {analyzedResult.rule_based.classification}
                </p>

              </div>


              <div className="result-card">

                <h3>
                  ML Prediction
                </h3>

                <div className="result-value">
                  {analyzedResult.ml_based.phishing_probability}%
                </div>

                <p>
                  {analyzedResult.ml_based.classification}
                </p>

              </div>


              <div className="result-card">

                <h3>
                  Hybrid Risk Score
                </h3>

                <div className="result-value">
                  {analyzedResult.hybrid.risk_score}
                </div>

                <p>
                  {analyzedResult.hybrid.classification}
                </p>

              </div>

            </div>


            <div className="recommendation">

              <h3>
                Recommendation
              </h3>

              <p>
                {analyzedResult.hybrid.recommendation}
              </p>

            </div>


            <div className="indicators">

              <h3>
                Detected Indicators
              </h3>


              {analyzedResult.indicators &&
              analyzedResult.indicators.length > 0 ? (

                <ul>

                  {analyzedResult.indicators.map(
                    (indicator, index) => (

                      <li key={index}>
                        {indicator}
                      </li>

                    )
                  )}

                </ul>

              ) : (

                <p>
                  No major phishing indicators detected.
                </p>

              )}

            </div>

          </section>

        )}


        {/* ==================================================
            HISTORY
        ================================================== */}

        <section className="card">

          <div className="section-title">

            <h2>
              Analysis History
            </h2>

            <p>
              Previous email analysis records.
            </p>

          </div>


          {history.length === 0 ? (

            <p className="empty-message">
              No analysis records yet.
            </p>

          ) : (

            <div className="table-container">

              <table>

                <thead>

                  <tr>

                    <th>
                      ID
                    </th>

                    <th>
                      Sender
                    </th>

                    <th>
                      Subject
                    </th>

                    <th>
                      Risk Score
                    </th>

                    <th>
                      Classification
                    </th>

                    <th>
                      ML Result
                    </th>

                    <th>
                      Probability
                    </th>

                  </tr>

                </thead>


                <tbody>

                  {history.map((item) => (

                    <tr key={item.id}>

                      <td>
                        {item.id}
                      </td>

                      <td>
                        {item.sender}
                      </td>

                      <td>
                        {item.subject}
                      </td>

                      <td>
                        {item.risk_score}
                      </td>

                      <td>
                        {item.classification}
                      </td>

                      <td>
                        {item.ml_classification}
                      </td>

                      <td>
                        {item.phishing_probability}%
                      </td>

                    </tr>

                  ))}

                </tbody>

              </table>

            </div>

          )}

        </section>


        {/* ==================================================
            PHISHING AWARENESS
        ================================================== */}

        <section className="card awareness-section">

          <div className="section-title">

            <h2>
              Phishing Awareness
            </h2>

            <p>
              Simple security practices to identify suspicious emails.
            </p>

          </div>


          <div className="awareness-grid">

            <div className="awareness-item">

              <h3>
                Check Links
              </h3>

              <p>
                Be careful with unexpected links.
                Check where a link leads before taking action.
              </p>

            </div>


            <div className="awareness-item">

              <h3>
                Verify the Sender
              </h3>

              <p>
                Check the sender address carefully.
                Do not trust a message only because the display
                name looks familiar.
              </p>

            </div>


            <div className="awareness-item">

              <h3>
                Watch for Urgency
              </h3>

              <p>
                Messages demanding immediate action
                should be checked carefully.
              </p>

            </div>


            <div className="awareness-item">

              <h3>
                Be Careful with Attachments
              </h3>

              <p>
                Avoid opening unexpected or suspicious attachments.
              </p>

            </div>

          </div>

        </section>

      </main>


      {/* ==================================================
          FOOTER
      ================================================== */}

      <footer className="footer">

        <p>
          Phishing Email Detection & Awareness Dashboard
        </p>

        <p>
          Built for educational and defensive cybersecurity purposes.
        </p>

      </footer>

    </div>
  );
}

export default App;