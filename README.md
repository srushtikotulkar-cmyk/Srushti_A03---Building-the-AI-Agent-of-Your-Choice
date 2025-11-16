# 📰 News Digest Agent

> AI-powered autonomous agent that delivers personalized daily news digests

**Course**: CISC691 - AI Agents  
**Assignment**: A03 - Building AI Agent  
**Author**: Srushti Kotulkar  
**Date**: November 2025

---

## 🎯 Overview

The News Digest Agent is an autonomous AI system that:
- Fetches latest news from multiple sources
- Summarizes articles using intelligent algorithms
- Delivers personalized digests via email
- Operates completely autonomously

**Problem Solved**: Information overload - helps users stay informed in minutes instead of hours.

---

## ✨ Features

- ✅ **Multi-topic news fetching** from NewsAPI
- ✅ **Intelligent summarization** using extractive methods
- ✅ **Professional HTML email** delivery
- ✅ **Automatic deduplication** of articles
- ✅ **Error handling** with fallback mechanisms
- ✅ **Local backup** of all digests
- ✅ **Zero ongoing costs** (uses free APIs)

---

## 🏗️ Architecture
```
Data Layer → Processing Layer → Presentation Layer
    ↓              ↓                  ↓
  NewsAPI    Summarization        Email/HTML
```

**Design Pattern**: Retrieval-Augmented Generation (RAG) + Sequential Processing

---

## 🚀 Quick Start

### Prerequisites
- Python 3.x
- Gmail account
- NewsAPI key (free)

### Installation

1. **Clone repository**
```bash
git clone [your-repo-url]
cd news-digest-agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
Create `.env` file:
```env
OPENAI_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECIPIENT=recipient@gmail.com
NEWS_TOPICS=artificial intelligence,technology
MAX_ARTICLES=5
```

4. **Run the agent**
```bash
python news_digest_agent.py
```

---

## 📖 Usage

### Basic Run
```bash
python news_digest_agent.py
```

### Test Components
```bash
python test_connection.py
```

### Customize Topics
Edit `.env` file:
```env
NEWS_TOPICS=ai,robotics,space,climate change
```

---

## 📊 Project Structure
```
news-digest-agent/
├── news_digest_agent.py      # Main agent code
├── test_connection.py         # Connection tester
├── .env                       # Configuration (not in git)
├── requirements.txt           # Dependencies
├── README.md                  # This file
├── technical_report.md        # Full technical documentation
├── workflow_diagram.md        # System diagrams
└── workflow_config.json       # Workflow specification
```

---

## 🧪 Testing

Tested scenarios:
- ✅ Normal execution with 5 articles
- ✅ API failures and rate limits
- ✅ Email delivery failures
- ✅ Empty or missing content
- ✅ Duplicate articles
- ✅ Special characters in text

---

## 📝 Technical Details

**Technologies**:
- Python 3.x
- NewsAPI (news source)
- Gmail SMTP (delivery)
- Custom extractive summarization

**Key Algorithms**:
- Keyword-based sentence scoring
- URL-based deduplication
- Extractive summarization

See `technical_report.md` for complete details.

---

## 🔮 Future Enhancements

- [ ] Sentiment analysis
- [ ] Web dashboard
- [ ] Multi-user support
- [ ] Cloud deployment (AWS Lambda)
- [ ] Advanced NLP summarization
- [ ] Mobile app integration

---

## 📄 License

MIT License - Educational project for CISC691

---

## 👤 Author

**SRUSHTI KOTULKAR**
- Course: CISC691
- Institution: Harrisburg University of Science and Technology 
- Semester: Fall 2025

---

## 🙏 Acknowledgments

- Professor Don O'Hara for guidance
- NewsAPI for free news data
- OpenAI for LLM research

```

---

## ✅ **Item 4: .gitignore**

Create file: `.gitignore`
```
# Environment variables (NEVER commit API keys!)
.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Generated files
digest_*.html
*.log

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
```

---

## ✅ **Item 5: requirements.txt**

```
python-dotenv==1.0.0
requests==2.31.0
newsapi-python==0.2.7
langchain-openai==0.2.0
schedule==1.2.0
python-dateutil==2.8.2