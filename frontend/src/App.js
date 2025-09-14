import React, { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a CSV file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (data.error) {
        setError(data.error);
        setResults(null);
        setSummary(null);
      } else {
        setResults(data.predictions);
        setSummary(data.summary);
        setError(null);
      }
    } catch (err) {
      setError("Failed to get predictions.");
      setResults(null);
      setSummary(null);
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Insurance Churn Prediction</h1>

      <input type="file" accept=".csv" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload & Predict</button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {summary && (
        <div>
          <h3>Summary:</h3>
          <pre>{JSON.stringify(summary, null, 2)}</pre>
        </div>
      )}

      {results && (
        <div>
          <h3>Predictions:</h3>
          <table border="1" cellPadding="5">
            <thead>
              <tr>
                {Object.keys(results[0]).map((col) => (
                  <th key={col}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {results.map((row, i) => (
                <tr key={i}>
                  {Object.values(row).map((val, j) => (
                    <td key={j}>{val}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;
