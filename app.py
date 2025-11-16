"""
News Digest Agent - Web Frontend
Built with Streamlit for CISC691 A03
"""

import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv
from newsapi import NewsApiClient
import re
import glob

# Load environment
load_dotenv()

# Page config
st.set_page_config(
    page_title="News Digest Agent",
    page_icon="📰",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #3498db;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .article-card {
        background: #f8f9fa;
        padding: 20px;
        border-left: 5px solid #3498db;
        border-radius: 5px;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# Summarization function
def simple_summarize(text, num_sentences=3):
    """Extractive summarization"""
    if not text or len(text) < 50:
        return "- Content too short to summarize"
    
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    if len(sentences) == 0:
        return "- No content available"
    
    keywords = ['new', 'first', 'launch', 'announce', 'develop', 'create', 
                'technology', 'ai', 'system', 'company', 'market', 'data',
                'research', 'study', 'report', 'says', 'according']
    
    scored_sentences = []
    for sentence in sentences:
        score = sum(1 for keyword in keywords if keyword.lower() in sentence.lower())
        scored_sentences.append((score, sentence))
    
    scored_sentences.sort(reverse=True, key=lambda x: x[0])
    top_sentences = [s[1] for s in scored_sentences[:num_sentences]]
    
    return '\n'.join([f"• {sent.strip()}" for sent in top_sentences])

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/news.png", width=80)
    st.title("⚙️ Configuration")
    
    # API Status
    news_api_key = os.getenv('NEWS_API_KEY')
    if news_api_key:
        st.success("✅ NewsAPI Connected")
    else:
        st.error("❌ NewsAPI Not Configured")
    
    st.markdown("---")
    
    # Topic configuration
    st.subheader("📌 Topics")
    default_topics = os.getenv('NEWS_TOPICS', 'artificial intelligence,technology').split(',')
    topics_input = st.text_area(
        "Enter topics (one per line):",
        value='\n'.join([t.strip() for t in default_topics]),
        height=150
    )
    topics = [t.strip() for t in topics_input.split('\n') if t.strip()]
    
    # Article count
    max_articles = st.slider("Max Articles", 1, 10, 5)
    
    st.markdown("---")
    
    # Stats
    st.subheader("📊 Stats")
    digest_files = glob.glob("digest_*.html")
    st.metric("Past Digests", len(digest_files))
    st.metric("Topics Tracked", len(topics))

# Main content
st.markdown('<h1 class="main-header">📰 News Digest Agent</h1>', unsafe_allow_html=True)
st.markdown("**AI-Powered Personalized News Curation | CISC691 A03 Project**")

# Tabs
tab1, tab2, tab3 = st.tabs(["🚀 Generate Digest", "📚 Past Digests", "ℹ️ About"])

# TAB 1: Generate Digest
with tab1:
    st.header("Generate Your Personalized Digest")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info(f"📍 Configured for **{len(topics)} topics**: {', '.join(topics[:3])}{'...' if len(topics) > 3 else ''}")
    
    with col2:
        if st.button("🚀 Generate Digest", type="primary", use_container_width=True):
            with st.spinner("🔄 Fetching and processing news..."):
                try:
                    # Initialize NewsAPI
                    news_api = NewsApiClient(api_key=news_api_key)
                    
                    # Progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Fetch news
                    status_text.text("📡 Fetching news articles...")
                    progress_bar.progress(20)
                    
                    all_articles = []
                    for idx, topic in enumerate(topics):
                        try:
                            response = news_api.get_everything(
                                q=topic,
                                language='en',
                                sort_by='publishedAt',
                                page_size=max_articles
                            )
                            articles = response.get('articles', [])
                            all_articles.extend(articles)
                            progress_bar.progress(20 + int(30 * (idx + 1) / len(topics)))
                        except Exception as e:
                            st.warning(f"⚠️ Error fetching '{topic}': {str(e)}")
                    
                    # Deduplicate
                    status_text.text("🔄 Removing duplicates...")
                    progress_bar.progress(60)
                    unique_articles = {art['url']: art for art in all_articles}.values()
                    articles_list = list(unique_articles)[:max_articles]
                    
                    # Summarize
                    status_text.text("✍️ Generating summaries...")
                    progress_bar.progress(70)
                    
                    summaries = []
                    for idx, article in enumerate(articles_list):
                        title = article.get('title', 'No title')
                        content = article.get('description', '') or article.get('content', '')
                        url = article.get('url', '#')
                        source = article.get('source', {}).get('name', 'Unknown')
                        published = article.get('publishedAt', '')[:10]
                        
                        summary = simple_summarize(content, num_sentences=3)
                        
                        summaries.append({
                            'title': title,
                            'summary': summary,
                            'url': url,
                            'source': source,
                            'published': published
                        })
                        
                        progress_bar.progress(70 + int(25 * (idx + 1) / len(articles_list)))
                    
                    status_text.text("✅ Digest ready!")
                    progress_bar.progress(100)
                    
                    # Display results
                    st.success(f"✅ Generated digest with **{len(summaries)} articles**")
                    
                    # Show articles
                    st.markdown("---")
                    st.subheader("📰 Your Digest")
                    
                    for idx, article_data in enumerate(summaries, 1):
                        with st.container():
                            st.markdown(f"""
                            <div class="article-card">
                                <h3>{idx}. {article_data['title']}</h3>
                                <p style="color: #7f8c8d; font-size: 0.9em;">
                                    📍 {article_data['source']} | 📅 {article_data['published']}
                                </p>
                                <div style="margin: 15px 0; line-height: 1.8;">
                                    {article_data['summary'].replace(chr(10), '<br>')}
                                </div>
                                <a href="{article_data['url']}" target="_blank" 
                                   style="color: #3498db; text-decoration: none; font-weight: bold;">
                                    🔗 Read Full Article →
                                </a>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Save option
                    st.markdown("---")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("💾 Save as HTML"):
                            filename = f"digest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                            # Create HTML (simplified)
                            html_content = "<html><body><h1>News Digest</h1>"
                            for art in summaries:
                                html_content += f"<h2>{art['title']}</h2><p>{art['summary']}</p>"
                            html_content += "</body></html>"
                            
                            with open(filename, 'w', encoding='utf-8') as f:
                                f.write(html_content)
                            
                            st.success(f"✅ Saved to {filename}")
                    
                    with col2:
                        if st.button("📧 Send Email (Coming Soon)"):
                            st.info("Email integration coming soon!")
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.exception(e)

# TAB 2: Past Digests
with tab2:
    st.header("📚 Past Digests")
    
    digest_files = sorted(glob.glob("digest_*.html"), reverse=True)
    
    if digest_files:
        st.info(f"Found **{len(digest_files)}** past digests")
        
        for file in digest_files[:10]:  # Show last 10
            file_name = os.path.basename(file)
            file_time = datetime.strptime(file_name.replace('digest_', '').replace('.html', ''), '%Y%m%d_%H%M%S')
            
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"📄 **{file_name}**")
                st.caption(f"Generated: {file_time.strftime('%B %d, %Y at %I:%M %p')}")
            
            with col2:
                with open(file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                st.download_button(
                    "⬇️ Download",
                    html_content,
                    file_name=file_name,
                    mime="text/html"
                )
            
            with col3:
                if st.button("👁️ View", key=f"view_{file}"):
                    st.components.v1.html(html_content, height=600, scrolling=True)
            
            st.markdown("---")
    else:
        st.warning("No past digests found. Generate one using the first tab!")

# TAB 3: About
with tab3:
    st.header("ℹ️ About This Project")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Project Overview")
        st.markdown("""
        **News Digest Agent** is an autonomous AI system built for CISC691 (A03 Assignment).
        
        **Key Features:**
        - 📡 Fetches news from NewsAPI
        - 🤖 AI-powered summarization
        - 📧 Email delivery (command-line version)
        - 🌐 Web interface (this app!)
        
        **Technologies:**
        - Python 3.x
        - Streamlit (Frontend)
        - NewsAPI (Data Source)
        - Custom Extractive Summarization
        """)
    
    with col2:
        st.subheader("🏗️ Architecture")
        st.markdown("""
        **Three-Layer Architecture:**
        
        1. **Data Layer**
           - NewsAPI integration
           - Multi-topic fetching
        
        2. **Processing Layer**
           - Deduplication
           - Extractive summarization
        
        3. **Presentation Layer**
           - Web UI (Streamlit)
           - HTML email (CLI version)
        """)
    
    st.markdown("---")
    
    st.subheader("👨‍💻 Author")
    st.markdown("""
    **Course:** CISC691 - AI Agents  
    **Assignment:** A03 - Building AI Agent  
    **Semester:** Fall 2025
    
    **Source Code:** Available on request  
    **Documentation:** See technical report
    """)
    
    st.markdown("---")
    
    st.subheader("🚀 Future Enhancements")
    st.markdown("""
    - ✅ Web interface (Done!)
    - ⏳ Sentiment analysis
    - ⏳ User authentication
    - ⏳ Preference learning
    - ⏳ Email scheduling from web UI
    - ⏳ Mobile app
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #7f8c8d;'>"
    "📰 News Digest Agent | CISC691 A03 Project | Powered by NewsAPI & Streamlit"
    "</div>",
    unsafe_allow_html=True
)