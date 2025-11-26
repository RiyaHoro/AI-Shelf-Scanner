import { useState } from "react";
import "./App.css";

function App() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const API_URL = "http://127.0.0.1:8000/scan"; // FastAPI backend

  const handleUpload = (e) => {
    const file = e.target.files[0];
    setImage(file);
    setPreview(URL.createObjectURL(file));
  };

  const analyzeImage = async () => {
    if (!image) return alert("Upload an image first!");

    setLoading(true);

    const formData = new FormData();
    formData.append("image", image);

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      console.log(data);

      setResults(data.books || []);
    } catch (err) {
      console.error("Error scanning:", err);
      alert("Failed to scan image");
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "20px", textAlign: "center" }}>
      <h1>📚 AI Shelf Scanner</h1>

      {/* Upload Image */}
      <input type="file" accept="image/*" onChange={handleUpload} />
      {preview && (
        <div style={{ marginTop: "10px" }}>
          <img
            src={preview}
            alt="Preview"
            style={{ width: "300px", borderRadius: "12px" }}
          />
        </div>
      )}

      <button
        onClick={analyzeImage}
        disabled={loading}
        style={{
          marginTop: "15px",
          padding: "10px 20px",
          fontSize: "1.1rem",
          cursor: loading ? "not-allowed" : "pointer",
        }}
      >
        {loading ? "Scanning..." : "Scan Books"}
      </button>

      {/* Results */}
      {results.length > 0 && (
        <div style={{ marginTop: "20px" }}>
          <h2>Detected Books ({results.length})</h2>

          <div
            style={{
              display: "flex",
              flexWrap: "wrap",
              gap: "20px",
              justifyContent: "center",
            }}
          >
            {results.map((book, index) => (
              <div
                key={index}
                style={{
                  width: "200px",
                  padding: "15px",
                  border: "1px solid #ddd",
                  borderRadius: "12px",
                  background: "#fff",
                  boxShadow: "0 3px 10px rgba(0,0,0,0.1)",
                }}
              >
                {book.thumbnail && (
                  <img
                    src={book.thumbnail}
                    alt={book.title}
                    style={{
                      width: "100%",
                      height: "260px",
                      objectFit: "cover",
                      borderRadius: "8px",
                    }}
                  />
                )}

                <h3 style={{ fontSize: "1rem", marginTop: "10px" }}>
                  {book.title}
                </h3>

                <p style={{ fontSize: "0.9rem", color: "#444" }}>
                  ✍️ {book.authors || "Unknown Author"}
                </p>

                <p style={{ fontSize: "0.85rem", color: "#666" }}>
                  ⭐ Rating: {book.rating || "N/A"}
                </p>

                <p style={{ fontSize: "0.8rem", color: "#777" }}>
                  {book.category || ""}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {!loading && results.length === 0 && preview && (
        <p style={{ marginTop: "10px", color: "gray" }}>
          📌 Click Scan Books to analyze!
        </p>
      )}
    </div>
  );
}

export default App;
