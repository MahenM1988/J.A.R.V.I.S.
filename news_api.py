import configparser
import requests

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

NEWS_BASE_URL = config['API']['NEWS_BASE_URL']
NEWS_API_KEY = config['API']['NEWS_API_KEY']

def get_top_headlines():
    params = {
        'apiKey': NEWS_API_KEY,
        'language': 'en',
    }
    try:
        response = requests.get(NEWS_BASE_URL, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        news_headlines = response.json()['articles']
        return news_headlines
    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

def fetch_news_headlines(speak_function):
    news_headlines = get_top_headlines()
    if news_headlines:
        headlines_text = "Here are the top news headlines:\n"
        for article in news_headlines[:10]:  # Limit to 10 headlines
            headlines_text += f"{article['title']}\n"
        print(headlines_text)
        speak_function(headlines_text)  # Pass the speak function as an argument
    else:
        print("Unable to fetch news headlines at the moment.")
