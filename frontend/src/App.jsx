import { useState } from "react";
import "./App.css";
import useTheme from "./useTheme";

function App() {
  const { theme, setTheme } = useTheme();

  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [recommendations, setRecommendations] = useState([]);

  const API_URL = "http://127.0.0.1:8000/scan";

  const toggleTheme = () => {
    setTheme(theme === "dark" ? "light" : "dark");
  };

  const handleUpload = (e) => {
    const file = e.target.files[0];
    setImage(file);
    setPreview(URL.createObjectURL(file));
  };

  const fetchRecommendations = async (category) => {
    if (!category) return alert("No category for recommendations!");

    const url = `https://www.googleapis.com/books/v1/volumes?q=subject:${category}&maxResults=6`;
    const res = await fetch(url);
    const data = await res.json();

    const books =
      data.items?.map((item) => ({
        title: item.volumeInfo.title,
        authors: item.volumeInfo.authors || ["Unknown"],
        thumbnail: item.volumeInfo.imageLinks?.thumbnail || "",
      })) || [];

    setRecommendations(books);
    setShowModal(true);
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
      setResults(data.books || []);
    } catch (err) {
        alert("Error scanning!");
    }
    setLoading(false);
  };

  return (
    <div className={`app-container ${theme}`}>
      {/* Theme Button */}
      <button className="theme-toggle" onClick={toggleTheme}>
        {theme === "dark" ? "🌞" : "🌙"}
      </button>

      <h1 className="text-6xl md:text-8xl font-extrabold italic tracking-wide text-center my-8">
  AI Shelf Scanner
</h1>


      <input type="file" accept="image/*" onChange={handleUpload} className="upload-input" />

      {preview && (
        <img className="preview-img" src={preview} alt="Preview" />
      )}

      <button className="app-btn scan-btn align-middle" onClick={analyzeImage} disabled={loading}>
        {loading ? "Scanning..." : "Scan Books"}
      </button>
       
      {/* Results */}
      {results.length > 0 && (
        <>
          <h2>Detected Books ({results.length})</h2>


          <div className="results-container">
            {results.map((book, i) => (
              <div className="card" key={i}>
                {book.thumbnail && <img src={book.thumbnail} alt="" className="book-img" />}

                <h3>{book.title}</h3>

                <p>✍️ {book.authors?.join(", ")}</p>

                <p>⭐ {book.rating || "No rating"}</p>

                <p className="category-text">
                  {book.categories?.join(", ") || "No Category"}
                </p>

                <details>
                  <summary>📌 Summary</summary>
                  <p>
                    {book.description
                      ? book.description.slice(0, 200) + "..."
                      : "No summary available"}
                  </p>
                </details>

                <button
                  className="app-btn recommend-btn"
                  onClick={() => fetchRecommendations(book.categories?.[0])}
                >
                  🎯 Recommend Similar
                </button>
              </div>
            ))}
          </div>
        </>
      )}

      {/* Recommendation Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-card" onClick={(e) => e.stopPropagation()}>
            <h3>📌 Similar Books</h3>
            <button className="close-btn" onClick={() => setShowModal(false)}>✖</button>

            <div className="recommendations">
              {recommendations.map((book, i) => (
                <div key={i} className="recommend-card">
                  {book.thumbnail && (
                    <img src={book.thumbnail} alt="" className="rec-book-img" />
                  )}
                  <p className="rec-title">{book.title}</p>
                  <small>{book.authors.join(", ")}</small>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

    </div>
  );
}

export default App;
