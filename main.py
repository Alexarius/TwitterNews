import os
import tweepy
from transformers import pipeline
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter API credentials from environment variables
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# Gmail details
GMAIL_SENDER = os.getenv('GMAIL_SENDER')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Function to authenticate and send email using Gmail API
def send_email(subject, body, to_email):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    message = MIMEText(body)
    message['to'] = to_email
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message = {'raw': raw}
    
    try:
        message = service.users().messages().send(userId='me', body=message).execute()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to get recent tweets
def get_tweets(screen_name):
    tweets = api.user_timeline(screen_name=screen_name, count=20, tweet_mode="extended")
    return [tweet.full_text for tweet in tweets]

# Function to summarize tweets
def summarize_tweets(tweets):
    combined_tweets = " ".join(tweets)
    summary = summarizer(combined_tweets, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

# Main execution
if __name__ == "__main__":
    # Twitter API authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Summarization pipeline
    summarizer = pipeline("summarization")

    # Get and summarize tweets
    tech_news_account = 'your_tech_news_account'
    tweets = get_tweets(tech_news_account)
    summary = summarize_tweets(tweets)

    # Send the summary via Gmail API
    send_email("Your Daily Tech Newsletter", summary, RECIPIENT_EMAIL)