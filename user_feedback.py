"""
User Feedback System - Production Ready
Tracks user interactions and adapts future digests based on preferences
INTEGRATED with news_digest_agent.py
"""

import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import os

class FeedbackTracker:
    """
    Tracks user interactions to enable personalization and adaptation.
    Now with actual functionality to influence article selection!
    """
    
    def __init__(self, feedback_file='user_preferences.json'):
        self.feedback_file = feedback_file
        self.preferences = self._load_preferences()
    
    def _load_preferences(self):
        """Load existing preferences from file"""
        if Path(self.feedback_file).exists():
            with open(self.feedback_file, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    # Handle case where file has line-delimited JSON
                    return self._migrate_old_format()
        
        # Initialize empty preferences structure
        return {
            'interactions': [],
            'source_scores': {},
            'topic_weights': {},
            'article_history': [],
            'metadata': {
                'created': datetime.now().isoformat(),
                'total_interactions': 0,
                'last_updated': None
            }
        }
    
    def _migrate_old_format(self):
        """Migrate from line-delimited JSON to structured format"""
        print("📦 Migrating old feedback format...")
        interactions = []
        
        with open(self.feedback_file, 'r') as f:
            for line in f:
                try:
                    interactions.append(json.loads(line.strip()))
                except:
                    continue
        
        # Create new structure with migrated data
        new_prefs = {
            'interactions': interactions,
            'source_scores': {},
            'topic_weights': {},
            'article_history': [],
            'metadata': {
                'created': datetime.now().isoformat(),
                'total_interactions': len(interactions),
                'last_updated': datetime.now().isoformat()
            }
        }
        
        # Calculate scores from old interactions
        for interaction in interactions:
            source = interaction.get('source')
            topic = interaction.get('topic')
            if source:
                new_prefs['source_scores'][source] = new_prefs['source_scores'].get(source, 0) + 1
            if topic:
                new_prefs['topic_weights'][topic] = new_prefs['topic_weights'].get(topic, 0) + 1
        
        self._save_preferences(new_prefs)
        print("✅ Migration complete!")
        return new_prefs
    
    def _save_preferences(self, prefs=None):
        """Save preferences to file"""
        if prefs is None:
            prefs = self.preferences
        
        prefs['metadata']['last_updated'] = datetime.now().isoformat()
        
        with open(self.feedback_file, 'w') as f:
            json.dump(prefs, f, indent=2)
    
    def log_article_click(self, article_url, topic, source, sentiment='neutral'):
        """
        Log when user clicks on an article (indicates interest)
        
        Args:
            article_url: URL of clicked article
            topic: Article topic category
            source: News source name
            sentiment: Optional sentiment indicator
        """
        interaction = {
            'url': article_url,
            'topic': topic,
            'source': source,
            'sentiment': sentiment,
            'timestamp': datetime.now().isoformat(),
            'action': 'clicked'
        }
        
        # Update preferences
        self.preferences['interactions'].append(interaction)
        self.preferences['metadata']['total_interactions'] += 1
        
        # Update source score (positive feedback)
        self.preferences['source_scores'][source] = \
            self.preferences['source_scores'].get(source, 0) + 1
        
        # Update topic weight (increase interest)
        self.preferences['topic_weights'][topic] = \
            self.preferences['topic_weights'].get(topic, 0) + 1
        
        # Add to history
        self.preferences['article_history'].append({
            'url': article_url,
            'read_date': datetime.now().isoformat()
        })
        
        self._save_preferences()
        
        print(f"✓ Logged interest in {topic} from {source}")
        return interaction
    
    def log_article_feedback(self, article_url, liked=True):
        """
        Record explicit user feedback (thumbs up/down)
        
        Args:
            article_url: Article URL
            liked: True if positive feedback, False if negative
        """
        feedback_type = 'liked' if liked else 'disliked'
        
        interaction = {
            'url': article_url,
            'timestamp': datetime.now().isoformat(),
            'action': feedback_type
        }
        
        self.preferences['interactions'].append(interaction)
        self.preferences['metadata']['total_interactions'] += 1
        
        # Find article in history to get source/topic
        for hist_article in reversed(self.preferences['interactions']):
            if hist_article.get('url') == article_url:
                source = hist_article.get('source')
                topic = hist_article.get('topic')
                
                if source:
                    # Adjust source score
                    delta = 2 if liked else -1
                    self.preferences['source_scores'][source] = \
                        self.preferences['source_scores'].get(source, 0) + delta
                
                if topic:
                    # Adjust topic weight
                    delta = 2 if liked else -1
                    self.preferences['topic_weights'][topic] = \
                        self.preferences['topic_weights'].get(topic, 0) + delta
                
                break
        
        self._save_preferences()
        print(f"{'👍' if liked else '👎'} Feedback recorded for {article_url[:50]}...")
        return interaction
    
    def get_source_score(self, source_name):
        """
        Get preference score for a news source
        Higher = user prefers this source
        """
        return self.preferences['source_scores'].get(source_name, 0)
    
    def get_topic_weight(self, topic):
        """
        Get interest weight for a topic
        Higher = user more interested in this topic
        """
        return self.preferences['topic_weights'].get(topic, 1)  # Default weight = 1
    
    def rank_articles(self, articles):
        """
        Rank articles based on user preferences
        
        Args:
            articles: List of article dicts with 'source', 'title', 'url'
        
        Returns:
            List of (score, article) tuples sorted by score (highest first)
        """
        scored_articles = []
        
        for article in articles:
            score = 0
            source = article.get('source', {})
            if isinstance(source, dict):
                source_name = source.get('name', 'Unknown')
            else:
                source_name = source
            
            # Score based on source preference
            source_score = self.get_source_score(source_name)
            score += source_score * 10  # Weight source heavily
            
            # Score based on topic (would need topic extraction in real implementation)
            # For now, check if article title contains any known topics
            title = article.get('title', '').lower()
            for topic, weight in self.preferences['topic_weights'].items():
                if topic.lower() in title:
                    score += weight * 5
            
            # Penalize already-read articles
            url = article.get('url')
            if any(h['url'] == url for h in self.preferences['article_history']):
                score -= 100  # Strong penalty for duplicates
            
            scored_articles.append((score, article))
        
        # Sort by score (highest first)
        scored_articles.sort(key=lambda x: x[0], reverse=True)
        
        return scored_articles
    
    def get_personalized_articles(self, articles, max_count=5):
        """
        Filter and rank articles based on user preferences
        
        Args:
            articles: List of available articles
            max_count: Maximum number to return
        
        Returns:
            List of top articles based on preferences
        """
        ranked = self.rank_articles(articles)
        return [article for score, article in ranked[:max_count]]
    
    def generate_insights_report(self):
        """Generate human-readable insights about user preferences"""
        prefs = self.preferences
        
        report = f"""
╔══════════════════════════════════════════════════════════╗
║           📊 USER PREFERENCE INSIGHTS                    ║
╚══════════════════════════════════════════════════════════╝

🎯 Activity Summary:
   • Total Interactions: {prefs['metadata']['total_interactions']}
   • Articles Read: {len(prefs['article_history'])}
   • Last Updated: {prefs['metadata'].get('last_updated', 'Never')[:10]}

📰 Top Preferred Sources:
"""
        # Sort sources by score
        top_sources = sorted(
            prefs['source_scores'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        for source, score in top_sources:
            bar = '█' * min(score, 20)
            report += f"   • {source:<20} {bar} ({score})\n"
        
        report += "\n🏷️  Topic Interests:\n"
        top_topics = sorted(
            prefs['topic_weights'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        for topic, weight in top_topics:
            bar = '█' * min(weight, 20)
            report += f"   • {topic:<20} {bar} ({weight})\n"
        
        # Recent activity
        if prefs['interactions']:
            report += f"\n🕒 Recent Activity:\n"
            for interaction in prefs['interactions'][-3:]:
                action = interaction.get('action', 'unknown')
                timestamp = interaction.get('timestamp', '')[:10]
                topic = interaction.get('topic', 'N/A')
                report += f"   • {timestamp} - {action} ({topic})\n"
        
        report += "\n💡 Personalization Status: "
        if prefs['metadata']['total_interactions'] > 10:
            report += "✅ ACTIVE (Agent is learning your preferences)\n"
        elif prefs['metadata']['total_interactions'] > 0:
            report += "🔄 LEARNING (Keep interacting to improve)\n"
        else:
            report += "⭕ NOT STARTED (No interactions yet)\n"
        
        return report
    
    def should_include_article(self, article, threshold=0):
        """
        Decide if article should be included based on preferences
        
        Args:
            article: Article dict
            threshold: Minimum score required
        
        Returns:
            Boolean
        """
        scored = self.rank_articles([article])
        if scored:
            score, _ = scored[0]
            return score >= threshold
        return True  # Include by default if no preference data

# ═══════════════════════════════════════════════════════════
#  DEMO & TESTING
# ═══════════════════════════════════════════════════════════

def demo_feedback_system():
    """Demonstrate the feedback system capabilities"""
    print("🧪 Testing Enhanced Feedback System\n")
    print("="*60)
    
    tracker = FeedbackTracker()
    
    # Simulate user interactions
    print("\n1️⃣  Simulating user reading articles...")
    tracker.log_article_click(
        'https://techcrunch.com/ai-breakthrough',
        'artificial intelligence',
        'TechCrunch'
    )
    
    tracker.log_article_click(
        'https://theverge.com/new-gadget',
        'technology',
        'The Verge'
    )
    
    tracker.log_article_click(
        'https://techcrunch.com/ml-research',
        'machine learning',
        'TechCrunch'
    )
    
    print("\n2️⃣  Simulating explicit feedback...")
    tracker.log_article_feedback('https://techcrunch.com/ai-breakthrough', liked=True)
    tracker.log_article_feedback('https://random-blog.com/clickbait', liked=False)
    
    print("\n3️⃣  Testing article ranking...")
    test_articles = [
        {'title': 'AI News', 'source': {'name': 'TechCrunch'}, 'url': 'url1'},
        {'title': 'Random Topic', 'source': {'name': 'Unknown Blog'}, 'url': 'url2'},
        {'title': 'Tech Update', 'source': {'name': 'The Verge'}, 'url': 'url3'},
    ]
    
    ranked = tracker.rank_articles(test_articles)
    print("\n   Ranked Articles:")
    for score, article in ranked:
        print(f"   • Score: {score:3.0f} - {article['title']} ({article['source']['name']})")
    
    print("\n4️⃣  Generating insights report...")
    print(tracker.generate_insights_report())
    
    print("\n✅ Demo Complete!")
    print(f"📁 Preferences saved to: {tracker.feedback_file}")

if __name__ == "__main__":
    demo_feedback_system()