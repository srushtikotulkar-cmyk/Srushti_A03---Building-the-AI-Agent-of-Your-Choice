"""
News Digest Agent - FREE VERSION (No OpenAI needed!)
CISC691 A03 Assignment - Uses extractive summarization
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from newsapi import NewsApiClient
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

# Load environment variables
load_dotenv()

print("🚀 Starting News Digest Agent (Free Version)...")
print("="*60)

def simple_summarize(text, num_sentences=3):
    """
    Simple extractive summarization - picks most important sentences.
    No OpenAI needed!
    """
    if not text or len(text) < 50:
        return "- Article content too short to summarize"
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    if len(sentences) == 0:
        return "- No content available"
    
    # Score sentences by keyword importance
    keywords = ['new', 'first', 'launch', 'announce', 'develop', 'create', 
                'technology', 'ai', 'system', 'company', 'market', 'data',
                'research', 'study', 'report', 'says', 'according']
    
    scored_sentences = []
    for sentence in sentences:
        score = sum(1 for keyword in keywords if keyword.lower() in sentence.lower())
        scored_sentences.append((score, sentence))
    
    # Sort by score and take top N
    scored_sentences.sort(reverse=True, key=lambda x: x[0])
    top_sentences = [s[1] for s in scored_sentences[:num_sentences]]
    
    # Format as bullet points
    summary = '\n'.join([f"- {sent.strip()}" for sent in top_sentences])
    return summary

# Initialize News API
print("\n1️⃣ Connecting to News API...")
news_api = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))
print("   ✅ News API connected")

print("\n2️⃣ Using FREE extractive summarization (no OpenAI needed)")
print("   ✅ Summarizer ready")

# Get configuration
topics = os.getenv('NEWS_TOPICS', 'technology').split(',')
max_articles = int(os.getenv('MAX_ARTICLES', '5'))

print(f"\n3️⃣ Configuration:")
print(f"   Topics: {', '.join(topics)}")
print(f"   Max articles: {max_articles}")

# Fetch news
print(f"\n4️⃣ Fetching news articles...")
all_articles = []

for topic in topics:
    try:
        response = news_api.get_everything(
            q=topic.strip(),
            language='en',
            sort_by='publishedAt',
            page_size=max_articles
        )
        articles = response.get('articles', [])
        print(f"   ✅ Found {len(articles)} articles for '{topic.strip()}'")
        all_articles.extend(articles)
    except Exception as e:
        print(f"   ❌ Error fetching '{topic}': {str(e)}")

# Remove duplicates
unique_articles = {art['url']: art for art in all_articles}.values()
articles_list = list(unique_articles)[:max_articles]

print(f"\n📰 Total unique articles to process: {len(articles_list)}")

# Summarize articles
print(f"\n5️⃣ Summarizing articles (extractive method)...")
summaries = []

for idx, article in enumerate(articles_list, 1):
    title = article.get('title', 'No title')
    description = article.get('description', '')
    content = article.get('content', '')
    url = article.get('url', '#')
    source = article.get('source', {}).get('name', 'Unknown')
    published = article.get('publishedAt', '')[:10]
    
    print(f"   Processing {idx}/{len(articles_list)}: {title[:50]}...")
    
    try:
        # Combine description and content for better summaries
        full_text = f"{description} {content}" if description or content else ""
        
        # Generate summary using our free method
        summary = simple_summarize(full_text, num_sentences=3)
        
        summaries.append({
            'title': title,
            'summary': summary,
            'url': url,
            'source': source,
            'published': published,
            'description': description[:200] if description else 'No preview available'
        })
        
        print(f"   ✅ Summarized successfully")
        
    except Exception as e:
        print(f"   ⚠️  Error summarizing: {str(e)}")
        summaries.append({
            'title': title,
            'summary': '- Summary unavailable due to processing error',
            'url': url,
            'source': source,
            'published': published,
            'description': description[:200] if description else 'No preview available'
        })

# Create HTML digest
print(f"\n6️⃣ Creating email digest...")
today = datetime.now().strftime("%B %d, %Y")

html_content = f"""
<html>
<head>
    <style>
        body {{ 
            font-family: Arial, sans-serif; 
            line-height: 1.6; 
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{ 
            color: #2c3e50; 
            border-bottom: 3px solid #3498db; 
            padding-bottom: 10px; 
            margin-bottom: 20px;
        }}
        h2 {{ 
            color: #34495e; 
            margin-top: 30px;
            font-size: 1.3em;
        }}
        .article {{ 
            margin: 25px 0; 
            padding: 20px; 
            background: linear-gradient(to right, #f8f9fa 0%, #ffffff 100%); 
            border-left: 5px solid #3498db;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        .source {{ 
            color: #7f8c8d; 
            font-size: 0.9em;
            margin: 10px 0;
            font-style: italic;
        }}
        .preview {{
            color: #555;
            font-style: italic;
            margin: 10px 0;
            padding: 10px;
            background: #f0f0f0;
            border-radius: 3px;
        }}
        .summary {{
            margin: 15px 0;
            line-height: 1.8;
            color: #2c3e50;
        }}
        .summary li {{
            margin: 8px 0;
        }}
        a {{ 
            color: #3498db; 
            text-decoration: none;
            font-weight: bold;
            display: inline-block;
            margin-top: 10px;
            padding: 8px 15px;
            background: #ecf0f1;
            border-radius: 5px;
            transition: all 0.3s;
        }}
        a:hover {{
            background: #3498db;
            color: white;
            transform: translateY(-2px);
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #ddd;
            color: #7f8c8d;
            font-size: 0.9em;
            text-align: center;
        }}
        .badge {{
            display: inline-block;
            padding: 3px 8px;
            background: #3498db;
            color: white;
            border-radius: 3px;
            font-size: 0.8em;
            margin-right: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📰 Your Daily News Digest</h1>
        <p><strong>📅 Date:</strong> {today}</p>
        <p><strong>🏷️ Topics:</strong> {', '.join(topics)}</p>
        <p><strong>📊 Articles:</strong> {len(summaries)}</p>
        <hr>
"""

for idx, article_data in enumerate(summaries, 1):
    html_content += f"""
    <div class="article">
        <h2><span class="badge">#{idx}</span> {article_data['title']}</h2>
        <p class="source">📍 {article_data['source']} | 📅 {article_data['published']}</p>
        
        <div class="preview">
            <strong>Preview:</strong> {article_data['description']}...
        </div>
        
        <div class="summary">
            <strong>Key Points:</strong>
            <div style="margin-top: 10px;">
                {article_data['summary'].replace('- ', '<p style="margin: 5px 0;">• ')}
            </div>
        </div>
        
        <a href="{article_data['url']}" target="_blank">🔗 Read Full Article →</a>
    </div>
    """

html_content += """
    <div class="footer">
        <p><strong>📱 News Digest Agent</strong></p>
        <p>CISC691 A03 Project | Powered by NewsAPI</p>
        <p style="margin-top: 10px; font-size: 0.85em;">
            Using extractive summarization (no API costs!)
        </p>
    </div>
    </div>
</body>
</html>
"""

print("   ✅ Digest created")

# Send email
print(f"\n7️⃣ Sending email...")

try:
    email_sender = os.getenv('EMAIL_SENDER')
    email_password = os.getenv('EMAIL_PASSWORD')
    email_recipient = os.getenv('EMAIL_RECIPIENT')
    
    # Create email message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"📰 Your Daily News Digest - {datetime.now().strftime('%B %d, %Y')}"
    msg['From'] = email_sender
    msg['To'] = email_recipient
    
    # Attach HTML
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)
    
    # Send via Gmail
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(email_sender, email_password)
        server.send_message(msg)
    
    print("   ✅ Email sent successfully!")
    print(f"   📧 Check your inbox: {email_recipient}")
    
    # Also save to file for backup
    filename = f"digest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"   💾 Backup saved to: {filename}")
    
except Exception as e:
    print(f"   ❌ Error sending email: {str(e)}")
    print("\n   Saving digest to file instead...")
    
    # Save to file as backup
    filename = f"digest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"   💾 Digest saved to: {filename}")
    print(f"   🌐 Open this file in your browser to view the digest")

print("\n" + "="*60)
print("✅ News Digest Agent Completed!")
print("="*60)
print("\n💡 Note: Using free extractive summarization")
print("   This picks the most important sentences from articles")
print("   No OpenAI API costs! ✨")