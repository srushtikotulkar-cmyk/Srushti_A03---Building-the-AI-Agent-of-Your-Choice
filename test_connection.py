from dotenv import load_dotenv
import os

load_dotenv()

print("\n🔍 Testing Configuration...\n")

# Check OpenAI Key
openai_key = os.getenv('OPENAI_API_KEY')
if openai_key:
    print(f"✅ OpenAI Key: {openai_key[:15]}...")
else:
    print("❌ OpenAI Key: MISSING")

# Check News API Key
news_key = os.getenv('NEWS_API_KEY')
if news_key:
    print(f"✅ News API Key: {news_key[:15]}...")
else:
    print("❌ News API Key: MISSING")

# Check Email
email = os.getenv('EMAIL_SENDER')
if email and email != 'your_email@gmail.com':
    print(f"✅ Email: {email}")
else:
    print("❌ Email: Not configured (still shows 'your_email@gmail.com')")

# Check Password
password = os.getenv('EMAIL_PASSWORD')
if password:
    print(f"✅ Email Password: {password[:4]}...")
else:
    print("❌ Email Password: MISSING")

print("\n" + "="*50)