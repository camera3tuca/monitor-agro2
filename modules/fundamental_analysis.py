import yfinance as yf

class FundamentalAnalysisEngine:
    def get_fundamental_data(self, ticker):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            return {
                'pe_ratio': info.get('trailingPE'),
                'price_to_book': info.get('priceToBook'),
                'roe': info.get('returnOnEquity'),
                'profit_margin': info.get('profitMargins'),
            }
        except:
            return None
    
    def analyze_valuation(self, fundamentals):
        if not fundamentals:
            return {'status': 'N/A', 'score': 0}
        
        pe = fundamentals.get('pe_ratio')
        score = 2 if pe and pe < 15 else 0
        status = "BARATO" if score > 0 else "JUSTO"
        
        return {'status': status, 'score': score}
    
    def analyze_profitability(self, fundamentals):
        if not fundamentals:
            return {'quality': 'N/A', 'score': 0}
        
        roe = fundamentals.get('roe')
        score = 2 if roe and roe > 0.15 else 0
        quality = "BOA" if score > 0 else "REGULAR"
        
        return {'quality': quality, 'score': score}
    
    def analyze_growth(self, fundamentals):
        return {'status': 'ESTÁVEL', 'score': 0}
    
    def analyze_financial_health(self, fundamentals):
        return {'health': 'BOA', 'score': 0}
    
    def generate_fundamental_score(self, valuation, profitability, growth, health):
        val_score = (valuation.get('score', 0) + 3) / 6 * 100
        prof_score = (profitability.get('score', 0) + 3) / 6 * 100
        total_score = (val_score + prof_score) / 2
        
        if total_score >= 70:
            classification = "🌟 EXCELENTE"
        elif total_score >= 50:
            classification = "🟢 BOM"
        else:
            classification = "🟡 REGULAR"
        
        return {
            'score': round(total_score, 1),
            'classification': classification
        }
