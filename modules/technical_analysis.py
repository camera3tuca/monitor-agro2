import yfinance as yf
from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator

class TechnicalAnalysisEngine:
    def get_price_data(self, ticker, period='6mo'):
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period)
            return df if not df.empty else None
        except:
            return None
    
    def calculate_indicators(self, df):
        if df is None or len(df) < 50:
            return None
        try:
            indicators = {
                'SMA_20': SMAIndicator(df['Close'], window=20).sma_indicator(),
                'RSI': RSIIndicator(df['Close'], window=14).rsi(),
                'MACD': MACD(df['Close']).macd(),
            }
            return indicators
        except:
            return None
    
    def analyze_trend(self, df, indicators):
        if indicators is None:
            return {'trend': 'NEUTRO', 'score': 0}
        
        try:
            current_price = df['Close'].iloc[-1]
            sma_20 = indicators['SMA_20'].iloc[-1]
            score = 1 if current_price > sma_20 else -1
            trend = 'ALTA' if score > 0 else 'BAIXA'
            return {'trend': trend, 'score': score}
        except:
            return {'trend': 'NEUTRO', 'score': 0}
    
    def analyze_momentum(self, indicators):
        if indicators is None:
            return {'status': 'NEUTRO', 'score': 0, 'rsi': 50}
        try:
            rsi = indicators['RSI'].iloc[-1]
            if rsi < 30:
                return {'status': 'SOBREVENDIDO', 'score': 3, 'rsi': rsi}
            elif rsi > 70:
                return {'status': 'SOBRECOMPRADO', 'score': -3, 'rsi': rsi}
            else:
                return {'status': 'NEUTRO', 'score': 0, 'rsi': rsi}
        except:
            return {'status': 'NEUTRO', 'score': 0, 'rsi': 50}
    
    def analyze_macd(self, indicators):
        return {'signal': 'NEUTRO', 'strength': 0}
    
    def calculate_support_resistance(self, df, window=20):
        try:
            resistance = df['High'].rolling(window=window).max().iloc[-1]
            support = df['Low'].rolling(window=window).min().iloc[-1]
            current = df['Close'].iloc[-1]
            return {
                'resistance': resistance,
                'support': support,
                'current': current,
                'dist_resistance_pct': ((resistance - current) / current) * 100,
                'dist_support_pct': ((current - support) / current) * 100
            }
        except:
            return None
    
    def generate_technical_score(self, trend, momentum, macd):
        trend_score = trend.get('score', 0)
        momentum_score = momentum.get('score', 0)
        total_score = trend_score + momentum_score
        normalized_score = ((total_score + 6) / 12) * 100
        
        if normalized_score >= 70:
            classification = "🟢 COMPRA FORTE"
        elif normalized_score >= 55:
            classification = "🟢 COMPRA"
        elif normalized_score >= 45:
            classification = "⚪ NEUTRO"
        else:
            classification = "🔴 VENDA"
        
        return {
            'score': round(normalized_score, 1),
            'classification': classification
        }
