class NewsAnalysisEngine:
    def __init__(self, finnhub_key, news_api_key):
        self.finnhub_key = finnhub_key
        self.news_api_key = news_api_key
    
    def get_news(self, ticker):
        return []
    
    def analyze_sentiment(self, news_list):
        return {
            'sentiment': 'NEUTRO',
            'score': 0,
            'positive': 0,
            'negative': 0,
            'neutral': 0
        }
    
    def detect_catalysts(self, news_list):
        return []
