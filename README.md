# README.md

# 🔍 TraceLens

**OSINT Image Analysis Platform**

TraceLens is a comprehensive open-source OSINT (Open Source Intelligence) platform for analyzing images. It provides metadata extraction, OCR, AI-generated image detection, reverse image search capabilities, and perceptual hashing for duplicate detection.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)

---

## ⚖️ Ethics & Legal Notice

**IMPORTANT**: TraceLens is designed for **lawful, ethical OSINT research only**. Users must:

- Comply with all applicable local, national, and international laws
- Respect privacy rights and obtain necessary permissions
- Use the tool only for legitimate research, investigation, or analysis purposes
- **NOT** use this tool for:
  - Unauthorized surveillance or stalking
  - Harassment or intimidation
  - Violation of privacy rights
  - Any malicious, illegal, or unethical purposes

By using TraceLens, you agree to use it responsibly and ethically. The developers are not responsible for misuse of this software.

---

## ✨ Features

- **📸 Metadata Extraction**: Extract comprehensive EXIF, IPTC, and GPS data from images
- **📝 OCR (Optical Character Recognition)**: Extract text from images using Tesseract
- **🤖 AI Detection**: Detect AI-generated images using multiple heuristics:
  - Noise level analysis
  - Frequency domain analysis
  - Color distribution patterns
  - Perceptual hash entropy
- **🔄 Reverse Image Search**: 
  - External API integration support (Google Vision, Bing, TinEye)
  - Local fallback using perceptual hash matching
- **🔗 Duplicate Detection**: Find similar images using perceptual hashing (pHash)
- **📊 Exportable Reports**: Download analysis results as JSON
- **🐳 Dockerized**: Easy deployment with Docker and docker-compose
- **🔒 Security**: File size limits, input sanitization, ethical content filtering

---

## 🏗️ Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                      TraceLens Frontend                      │
│                    (React + Vite)                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Upload Form  │  │ Results View │  │ Export       │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │ HTTP/REST
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      TraceLens Backend                       │
│                     (FastAPI + Python)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   API Layer  │  │   Services   │  │   Utils      │      │
│  │              │  │              │  │              │      │
│  │ /analyze     │─▶│ • Metadata   │  │ • File       │      │
│  │ /health      │  │ • OCR        │  │   Validation │      │
│  └──────────────┘  │ • AI Detect  │  │ • Security   │      │
│                    │ • pHash      │  └──────────────┘      │
│                    │ • Rev Search │                         │
│                    └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
              ┌──────────────────────────┐
              │   External Services      │
              │                          │
              │ • Tesseract OCR          │
              │ • Reverse Search APIs    │
              │   (optional)             │
              └──────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- (Optional) For local development:
  - Python 3.11+
  - Node.js 18+
  - Tesseract OCR

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/tracelens.git
cd tracelens
```

2. **Set up environment variables** (optional):
```bash
# Create .env file
echo "REVSEARCH_API_KEY=your_api_key_here" > .env
```

3. **Run with Docker Compose**:
```bash
docker-compose up --build
```

4. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

---

## 🛠️ Local Development

### Backend Setup
```bash
cd backend

# Install Tesseract OCR (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-eng

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `REVSEARCH_API_KEY` | API key for reverse image search service | None (uses local fallback) |
| `MAX_FILE_SIZE` | Maximum upload file size in bytes | 10485760 (10MB) |
| `TESSERACT_LANG` | Tesseract OCR language | eng |
| `AI_DETECTION_THRESHOLD` | AI detection threshold (0-1) | 0.7 |
| `CORS_ORIGINS` | Allowed CORS origins | localhost:3000 |

### Reverse Image Search API Integration

To use external reverse image search APIs, set the `REVSEARCH_API_KEY` environment variable:
```bash
export REVSEARCH_API_KEY="your_api_key_here"
```

**Supported APIs** (implement in `backend/app/services/rev_search.py`):
- Google Cloud Vision API
- Bing Image Search API
- TinEye API

Without an API key, TraceLens uses local perceptual hash matching as a fallback.

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

---

## 📊 API Documentation

### Endpoints

#### `POST /api/v1/analyze`

Analyze an uploaded image.

**Request**:
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `file` (image file, max 10MB)

**Response**:
```json
{
  "filename": "example.jpg",
  "metadata": {
    "exif": {...},
    "iptc": {...},
    "basic": {...},
    "gps": {...}
  },
  "ocr": {
    "text": "Extracted text...",
    "confidence": 0.95,
    "language": "eng"
  },
  "ai_detection": {
    "score": 0.72,
    "verdict": "ai",
    "explanation": "High probability of AI generation...",
    "signals": {...}
  },
  "perceptual_hash": "8f373b8e8e8e8e8e",
  "duplicates": [...],
  "reverse_search": [...]
}
```

#### `GET /api/v1/health`

Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

---

## 📁 Project Structure
```
tracelens/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app entry point
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints.py    # API routes
│   │   │       └── models.py       # Pydantic models
│   │   ├── core/
│   │   │   └── config.py           # Configuration
│   │   ├── services/
│   │   │   ├── metadata.py         # Metadata extraction
│   │   │   ├── ocr_service.py      # OCR service
│   │   │   ├── ai_detector.py      # AI detection
│   │   │   ├── rev_search.py       # Reverse search
│   │   │   └── phash.py            # Perceptual hashing
│   │   └── utils/
│   │       └── file_helpers.py     # File utilities
│   ├── tests/
│   │   └── test_metadata.py        # Unit tests
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.jsx                 # Main app component
│   │   ├── index.jsx               # Entry point
│   │   └── components/
│   │       ├── UploadForm.jsx      # Upload component
│   │       └── ResultsView.jsx     # Results display
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
├── docker-compose.yml
├── .github/
│   └── workflows/
│       └── ci.yml                  # GitHub Actions CI
├── LICENSE
└── README.md
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint/Prettier for JavaScript/React code
- Write tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

---

## 🐛 Known Limitations

- AI detection uses heuristics, not deep learning models (for demo/lightweight deployment)
- Reverse image search requires external API keys for full functionality
- In-memory storage means duplicate detection resets on server restart
- Basic explicit content filtering (ML-based moderation recommended for production)

---

## 🗺️ Roadmap

- [ ] Add support for video analysis
- [ ] Implement proper database for persistent storage
- [ ] Integrate pre-trained AI detection models (e.g., CNN-based)
- [ ] Add batch processing capabilities
- [ ] Implement user authentication and multi-tenancy
- [ ] Add support for more OCR languages
- [ ] Create CLI tool for automation
- [ ] Add geolocation visualization for GPS data

---

## 📄 License

This project is licensed under the MIT License - see below for details:
```
MIT License

Copyright (c) 2024 TraceLens Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [React](https://reactjs.org/) - UI library
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - OCR engine
- [ImageHash](https://github.com/JohannesBuchner/imagehash) - Perceptual hashing
- [Pillow](https://python-pillow.org/) - Image processing

---

## 📧 Contact

For questions, suggestions, or security concerns, please open an issue on GitHub.

---

**Remember: Use TraceLens responsibly and ethically. Always respect privacy and comply with applicable laws.**