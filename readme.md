# 📚 Shelf Scanner

![GitHub stars](https://img.shields.io/github/stars/your-username/shelf-scanner?style=social) 
![GitHub forks](https://img.shields.io/github/forks/your-username/shelf-scanner?style=social) 
![GitHub license](https://img.shields.io/github/license/your-username/shelf-scanner)

**Shelf Scanner** is an AI-powered app that scans books on a shelf, extracts key info like title, author, rating, and reviews, and gives personalized recommendations. Perfect for libraries, bookstores, or personal collections.  

---

## 🚀 Features

- 🔹 **Book Detection:** Detects book spines in images using computer vision.  
- 🔹 **OCR Extraction:** Reads titles and authors with Tesseract OCR.  
- 🔹 **Book Info:** Fetches summaries, ratings, and reviews automatically.  
- 🔹 **Recommendations:** Suggests books based on scanned books and preferences.  
- 🔹 **PDF Reports:** Download full scanned results as a PDF.  
- 🔹 **Responsive UI:** Neat cards for each book with summary and rating.

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

## 💻 Installation

### Backend

```bash
git clone https://github.com/your-username/shelf-scanner.git
cd shelf-scanner/backend
python -m venv venv
# Activate venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
---
## Frontend
cd ../frontend
npm install
npm run dev
# Open http://localhost:5173
---
## Project structure
Shelf-Scanner/
├── backend/       # FastAPI backend
│   ├── main.py
│   ├── detect.py
│   └── requirements.txt
├── frontend/      # React frontend
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── README.md
└── .gitignore

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
