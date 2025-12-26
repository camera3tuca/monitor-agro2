from .database import AgroDatabase
from .technical_analysis import TechnicalAnalysisEngine
from .fundamental_analysis import FundamentalAnalysisEngine
from .news_analysis import NewsAnalysisEngine
from datetime import datetime
import time

class AgroMonitoringSystem:
    def __init__(self, finnhub_key, news_api_key, brapi_token):
        self.database = AgroDatabase()
        self.technical = TechnicalAnalysisEngine()
        self.fundamental = FundamentalAnalysisEngine()
        self.news = NewsAnalysisEngine(finnhub_key, news_api_key)
    
    def analyze_asset(self, ticker):
        ticker_info = self.database.get_ticker_info(ticker)
        if not ticker_info:
            return None
        
        ticker_display = ticker_info.get('ticker_display', ticker)
        
        # Análise Técnica
        df = self.technical.get_price_data(ticker, period='6mo')
        if df is None or len(df) < 50:
            return None
        
        indicators = self.technical.calculate_indicators(df)
        trend = self.technical.analyze_trend(df, indicators)
        momentum = self.technical.analyze_momentum(indicators)
        macd = self.technical.analyze_macd(indicators)
        support_resistance = self.technical.calculate_support_resistance(df)
        technical_score = self.technical.generate_technical_score(trend, momentum, macd)
        
        # Análise Fundamentalista
        fundamentals = self.fundamental.get_fundamental_data(ticker)
        valuation = self.fundamental.analyze_valuation(fundamentals)
        profitability = self.fundamental.analyze_profitability(fundamentals)
        growth = self.fundamental.analyze_growth(fundamentals)
        health = self.fundamental.analyze_financial_health(fundamentals)
        fundamental_score = self.fundamental.generate_fundamental_score(
            valuation, profitability, growth, health
        )
        
        # Análise de Notícias
        news_list = self.news.get_news(ticker)
        sentiment = self.news.analyze_sentiment(news_list)
        catalysts = self.news.detect_catalysts(news_list)
        
        # Score Final
        final_score = (
            technical_score['score'] * 0.40 +
            fundamental_score['score'] * 0.40 +
            ((sentiment['score'] + 100) / 2) * 0.20
        )
        
        # Recomendação
        if final_score >= 70:
            recommendation = "🟢 COMPRA FORTE"
            priority = "ALTA"
        elif final_score >= 55:
            recommendation = "🟢 COMPRA"
            priority = "MÉDIA"
        else:
            recommendation = "⚪ NEUTRO"
            priority = "BAIXA"
        
        return {
            'ticker': ticker,
            'ticker_display': ticker_display,
            'info': ticker_info,
            'price_data': {
                'current': df['Close'].iloc[-1],
                'change_1d': ((df['Close'].iloc[-1] / df['Close'].iloc[-2]) - 1) * 100,
                'change_1m': ((df['Close'].iloc[-1] / df['Close'].iloc[-21]) - 1) * 100,
            },
            'technical': {
                'score': technical_score,
                'trend': trend,
                'momentum': momentum,
                'macd': macd,
                'support_resistance': support_resistance
            },
            'fundamental': {
                'score': fundamental_score,
                'valuation': valuation,
                'profitability': profitability,
                'growth': growth,
                'health': health,
                'raw_data': fundamentals
            },
            'news': {
                'sentiment': sentiment,
                'catalysts': catalysts,
                'recent_news': news_list[:3]
            },
            'recommendation': {
                'final_score': round(final_score, 1),
                'action': recommendation,
                'priority': priority,
                'strategy': f'Stop: -3% | Alvo: +15%',
                'timeframe': '5 dias'
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def scan_all_assets(self, min_score=50):
        all_tickers = self.database.get_all_tickers()
        results = []
        
        for ticker in all_tickers:
            try:
                analysis = self.analyze_asset(ticker)
                if analysis and analysis['recommendation']['final_score'] >= min_score:
                    results.append(analysis)
                time.sleep(0.5)
            except:
                continue
        
        results.sort(key=lambda x: x['recommendation']['final_score'], reverse=True)
        return results
