# News Digest Agent - System Workflow Diagram

## High-Level Flow
```
┌─────────────┐
│   START     │
└──────┬──────┘
       │
       ▼
┌──────────────────────┐
│  Load Configuration  │
│  • API Keys          │
│  • Topics            │
│  • Email Settings    │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Initialize Clients  │
│  • NewsAPI           │
│  • SMTP              │
└──────┬───────────────┘
       │
       ▼
┌─────────────────────────────┐
│  Fetch News                 │
│  ┌───────────────────────┐  │
│  │ FOR EACH topic:       │  │
│  │  • Query NewsAPI      │  │
│  │  • Filter & Sort      │  │
│  └───────────────────────┘  │
└──────┬──────────────────────┘
       │
       ▼
┌──────────────────────┐
│  Deduplicate by URL  │
└──────┬───────────────┘
       │
       ▼
┌─────────────────────────────┐
│  Summarize Articles         │
│  ┌───────────────────────┐  │
│  │ FOR EACH article:     │  │
│  │  • Extract text       │  │
│  │  • Score sentences    │  │
│  │  • Select top 3       │  │
│  └───────────────────────┘  │
└──────┬──────────────────────┘
       │
       ▼
┌──────────────────────┐
│  Format HTML Digest  │
│  • Apply CSS         │
│  • Insert Data       │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Send Email          │
│  via SMTP            │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Save HTML Backup    │
└──────┬───────────────┘
       │
       ▼
┌─────────────┐
│  COMPLETE   │
└─────────────┘
```

## Architecture Diagram
```
╔═══════════════════════════════════════════════╗
║        PRESENTATION LAYER                     ║
║  ┌─────────────────────────────────────────┐  ║
║  │ • HTML Email Formatting                 │  ║
║  │ • SMTP Email Delivery (Gmail)           │  ║
║  │ • Local File Backup System              │  ║
║  └─────────────────────────────────────────┘  ║
╚═══════════════════════════╦═══════════════════╝
                            ↓
╔═══════════════════════════════════════════════╗
║        PROCESSING LAYER                       ║
║  ┌─────────────────────────────────────────┐  ║
║  │ • Extractive Summarization Engine       │  ║
║  │ • Keyword-based Sentence Scoring        │  ║
║  │ • URL-based Content Deduplication       │  ║
║  └─────────────────────────────────────────┘  ║
╚═══════════════════════════╦═══════════════════╝
                            ↓
╔═══════════════════════════════════════════════╗
║        DATA LAYER                             ║
║  ┌─────────────────────────────────────────┐  ║
║  │ • NewsAPI Client Integration            │  ║
║  │ • Multi-topic Article Fetching          │  ║
║  │ • Language & Date Filtering             │  ║
║  └─────────────────────────────────────────┘  ║
╚═══════════════════════════════════════════════╝
```