import { useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/scan";

export default function ShelfScanner() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewImage, setPreviewImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [books, setBooks] = useState([]);
  const [error, setError] = useState("");

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setSelectedImage(file);
    setPreviewImage(URL.createObjectURL(file));
  };

  const scanBooks = async () => {
    if (!selectedImage) {
      setError("Please upload an image first");
      return;
    }
    setLoading(true);
    setError("");
    setBooks([]);

    const formData = new FormData();
    formData.append("image", selectedImage);

    try {
      const response = await axios.post(API_URL, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      console.log("📘 API Response:", response.data);

      if (response.data.books?.length > 0) {
        setBooks(response.data.books);
      } else {
        setError("No books detected 😢 Try another image");
      }
    } catch (err) {
      console.error("API Error:", err.response ? err.response.data : err);
      setError("Failed to scan books. Check console for details.");
    }

    setLoading(false);
  };

  return (
    <div className="max-w-3xl mx-auto bg-white p-6 rounded-xl shadow-md">
      <h1 className="text-2xl font-bold mb-4">📚 AI Shelf Scanner</h1>

      {/* Upload UI */}
      <input
        type="file"
        accept="image/*"
        onChange={handleImageChange}
        className="mb-4"
      />

      {previewImage && (
        <img
          src={previewImage}
          alt="preview"
          className="w-full rounded-md mb-4 shadow"
        />
      )}

      <button
        onClick={scanBooks}
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        {loading ? "Scanning..." : "Scan Books"}
      </button>

      {error && <p className="text-red-500 mt-3">{error}</p>}

      {/* Display Results */}
      {books.length > 0 && (
        <div className="mt-6 space-y-4">
          <h2 className="text-xl font-bold">📕 Books Found:</h2>

          {books.map((book, index) => (
            <div key={index} className="flex bg-gray-100 p-3 rounded-lg shadow">
              {book.thumbnail && (
                <img
                  src={book.thumbnail}
                  alt="thumbnail"
                  className="w-20 h-28 object-cover rounded"
                />
              )}
              <div className="ml-4">
                <h3 className="font-semibold text-lg">{book.title}</h3>
                <p className="text-sm text-gray-600">
                  {book.authors?.join(", ") || "Unknown Author"}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
