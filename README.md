# Twitter News Summarizer

This project fetches the latest tweets from a specified Twitter account, summarizes the content using a text summarization model, and sends the summary to your email via the Gmail API. The goal is to create a personalized tech newsletter that you can receive daily in your inbox.

## Features

- **Twitter Feed Crawling:** Fetches the latest tweets from a specified account.
- **Text Summarization:** Uses Hugging Face's `transformers` library to summarize the tweets.
- **Email Delivery:** Sends the summarized content to your Gmail account using the Gmail API.

## Requirements

- Python 3.7+
- Twitter API credentials
- Gmail API credentials

## Installation

### Clone the Repository

```bash
git clone https://github.com/Alexarius/TwitterNews.git
cd TwitterNews