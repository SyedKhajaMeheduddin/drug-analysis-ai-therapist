# 💊 Drug Analysis & AI Therapist System

A full-stack web application that identifies medicines from uploaded images using OCR and provides AI-powered health guidance through a built-in therapist module.

---

## 🎯 Features

| Module | Description |
|--------|-------------|
| **Image Upload** | Drag-and-drop pill/packaging image upload with preview |
| **OCR Engine** | Tesseract-powered text extraction with multi-config preprocessing |
| **Drug Matching** | 3-level matching: exact local → fuzzy → openFDA API |
| **Drug Info** | Enriched info from openFDA: generic name, dosage form, manufacturer, warnings |
| **AI Therapist** | Classifies concerns (safety / side effects / usage / info) and gives structured responses |
| **Admin Dashboard** | Tracks all analyses and therapy sessions with statistics |
| **Database** | MySQL persistence for all analyses and sessions |

---

## 🏗️ Project Structure

```
drug_analysis/
├── app.py                    # Flask entry point
├── requirements.txt
├── modules/
│   ├── database.py           # MySQL connection & init
│   ├── ocr.py                # Tesseract OCR + preprocessing
│   ├── drug_matcher.py       # Exact / fuzzy / API matching
│   ├── drug_info.py          # openFDA drug info fetcher
│   └── therapist.py          # AI concern classifier & response generator
├── routes/
│   ├── upload.py             # Image upload + full pipeline
│   ├── drug.py               # Drug detail view
│   ├── therapist.py          # AI therapist form
│   └── admin.py              # Admin dashboard
├── templates/
│   ├── base.html
│   ├── index.html            # Upload page
│   ├── result.html           # Analysis result
│   ├── therapist.html        # AI Therapist
│   └── admin.html            # Admin dashboard
└── static/
    ├── css/style.css
    ├── js/main.js
    └── uploads/              # Uploaded images (gitignored)
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- MySQL 8.0+
- Tesseract OCR installed on your system

**Install Tesseract:**
- **Ubuntu/Debian:** `sudo apt install tesseract-ocr`
- **macOS:** `brew install tesseract`
- **Windows:** Download from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/drug-analysis-ai-therapist.git
cd drug-analysis-ai-therapist

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables (optional)
# Create a .env file or set directly:
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=yourpassword
export DB_NAME=drug_analysis_db

# 5. Run the app (auto-creates the database and tables)
python app.py
```

Open your browser at `http://localhost:5000`

---

## 🚀 Usage

1. **Upload** — Go to the home page, drag and drop or select a pill/medicine image.
2. **Analyze** — The OCR extracts text → drug matching runs → openFDA enriches the data.
3. **Result** — View the identified drug, its details, warnings, and adverse reactions.
4. **Therapist** — Click "Consult AI Therapist", type your concern, get structured guidance.
5. **Admin** — Visit `/admin` for system statistics and session history.

---

## 🔌 APIs Used

- **[openFDA NDC API](https://open.fda.gov/apis/drug/ndc/)** — Drug product data (no API key required for public use)
- **[openFDA Label API](https://open.fda.gov/apis/drug/label/)** — Warnings, indications, adverse reactions

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| OCR | Tesseract (pytesseract), OpenCV, Pillow |
| Matching | Difflib (fuzzy), requests (API) |
| Database | MySQL, mysql-connector-python |
| Data | Pandas-ready structure (extendable) |
| Frontend | HTML5, CSS3, Vanilla JS |

---

## 📸 Screenshots

*(Add screenshots of the upload page, result page, therapist page, and admin dashboard here)*

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**Syed Khaja Meheduddin**  
[LinkedIn](https://linkedin.com/in/syedkhajameheduddin) • [GitHub](https://github.com/yourusername)
