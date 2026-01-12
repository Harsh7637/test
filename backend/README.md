# AI Platform Backend - Enhanced with Gemini API

A powerful FastAPI backend for AI-driven resume optimization and ATS analysis. Now powered by Google's Gemini API.

## ✨ Key Features

- 🚀 **No Local Models** - Uses Google Gemini API instead of large models  
- 💎 **High Performance** - Fast, accurate, and cost-effective  
- 📄 **ATS Optimization** - Dual-layer analysis with Gemini AI  
- ✍️ **Resume Enhancement** - AI-powered improvements  
- 📝 **Cover Letter Generation** - Automated personalized letters  
- 🎨 **Image Descriptions** - Enhanced metadata generation  

## 🚀 Quick Start

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLP models
python -m spacy download en_core_web_sm

# Setup environment
cp .env.example .env
# Edit .env and add GEMINI_API_KEY
```

## Run the Application

```bash
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/api/docs

## 📚 Documentation

See [UPGRADE_GUIDE.md](../UPGRADE_GUIDE.md) for detailed setup instructions.