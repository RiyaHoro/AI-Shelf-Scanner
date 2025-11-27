# 📚 Shelf Scanner

> AI-powered bookshelf scanner — Detect. Extract. Recommend. 📖✨

Shelf Scanner scans a bookshelf image, detects books, extracts their titles/authors using OCR, fetches ratings & summaries, and gives smart reading recommendations.

---

## 🚀 Features

- 📘 **AI Book Detection** — Identifies book spines in an image
- 🔍 **OCR Text Extraction** using Tesseract
- ⭐ **Book Details Fetch** — Summary, rating, reviews
- 🎯 **Recommendations** — Based on scanned books & genre patterns
- 📄 **PDF Export** of results
- 💻 **Responsive UI** — Clean book cards layout

---


## 🎨 Demo

![Shelf Scanner Demo](path_to_gif_or_screenshot)  
*Upload your bookshelf image → Detect books → Get results in neat cards.*

---

## 🛠 Tech Stack

- **Frontend:** React + Vite + Tailwind CSS  
- **Backend:** FastAPI (Python)  
- **AI/ML:** OpenCV, Tesseract OCR  
- **Database:** PostgreSQL  
- **Deployment:** AWS / Render / Local

---


---

## ⚙️ Installation & Setup

## Backend

```bash
cd backend
python -m venv venv
# Activate venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

## Frontend
cd ../frontend
npm install
npm run dev
# Open http://localhost:5173
---
```
## Project structure
```bash
Shelf-Scanner/
├── backend/ # FastAPI Backend
│ ├── main.py
│ ├── detect.py
│ └── requirements.txt
├── frontend/ # React Frontend
│ ├── src/
│ ├── package.json
│ └── vite.config.js
├── README.md
└── .gitignore
```
## 🧩 How to Use

Take a clear picture of your bookshelf.

Upload it via the frontend.

Detect books and extract info.

View neat cards with title, author, rating, and summary.

Download results as a PDF if needed.

## 🌟 Future Improvements

Multi-language OCR support

AI-based recommendation engine

Real-time mobile scanning

Reading history & personal library stats

## 🤝 Contributing

Fork the repo

Create a branch: git checkout -b feature-name

Commit changes: git commit -m "Add feature"

Push branch: git push origin feature-name

Open a Pull Request

## 📜 License

MIT License. See LICENSE
 for details.
