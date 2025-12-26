"""
Base de Dados de Ativos do Agronegócio
"""

class AgroDatabase:
    """
    Base de dados completa do setor de agronegócio
    """
    
    def __init__(self):
        self.data = self._initialize_database()
    
    def _initialize_database(self):
        """Inicializa base de ativos do agronegócio"""
        
        database = {
            # AÇÕES BRASILEIRAS - Agronegócio (com sufixo .SA para Yahoo Finance)
            'acoes_br': {
                # Proteína Animal
                'BEEF3.SA': {'name': 'Minerva', 'sector': 'Frigorífico', 'subsector': 'Proteína Bovina', 'ticker_display': 'BEEF3'},
                'MRFG3.SA': {'name': 'Marfrig', 'sector': 'Frigorífico', 'subsector': 'Proteína Bovina', 'ticker_display': 'MRFG3'},
                'JBSS3.SA': {'name': 'JBS', 'sector': 'Frigorífico', 'subsector': 'Proteína Animal', 'ticker_display': 'JBSS3'},
                'BRFS3.SA': {'name': 'BRF', 'sector': 'Frigorífico', 'subsector': 'Aves e Suínos', 'ticker_display': 'BRFS3'},
                
                # Bebidas e Alimentos
                'ABEV3.SA': {'name': 'Ambev', 'sector': 'Bebidas', 'subsector': 'Bebidas', 'ticker_display': 'ABEV3'},
                'MDIA3.SA': {'name': 'M. Dias Branco', 'sector': 'Alimentos', 'subsector': 'Alimentos Processados', 'ticker_display': 'MDIA3'},
                
                # Insumos Agrícolas
                'SMTO3.SA': {'name': 'São Martinho', 'sector': 'Açúcar e Etanol', 'subsector': 'Bioenergia', 'ticker_display': 'SMTO3'},
                'SOJA3.SA': {'name': 'Boa Safra', 'sector': 'Insumos', 'subsector': 'Sementes', 'ticker_display': 'SOJA3'},
                
                # Trading e Logística
                'RAIZ4.SA': {'name': 'Raízen', 'sector': 'Bioenergia', 'subsector': 'Etanol', 'ticker_display': 'RAIZ4'},
                'CSAN3.SA': {'name': 'Cosan', 'sector': 'Bioenergia', 'subsector': 'Açúcar e Etanol', 'ticker_display': 'CSAN3'},
                
                # Papel e Celulose (ligado ao agro)
                'SUZB3.SA': {'name': 'Suzano', 'sector': 'Papel e Celulose', 'subsector': 'Celulose', 'ticker_display': 'SUZB3'},
                'KLBN11.SA': {'name': 'Klabin', 'sector': 'Papel e Celulose', 'subsector': 'Papel', 'ticker_display': 'KLBN11'},
                
                # Terras e Agricultura
                'SLCE3.SA': {'name': 'SLC Agrícola', 'sector': 'Agricultura', 'subsector': 'Grãos', 'ticker_display': 'SLCE3'},
                'AGRO3.SA': {'name': 'BrasilAgro', 'sector': 'Agricultura', 'subsector': 'Terras Agrícolas', 'ticker_display': 'AGRO3'},
            },
            
            # BDRs - Agronegócio Internacional (códigos corretos)
            'bdrs': {
                # Equipamentos Agrícolas
                'DE': {'name': 'Deere & Company', 'sector': 'Equipamentos', 'subsector': 'Maquinário Agrícola', 'ticker_display': 'DE (D1EE34)', 'is_bdr': True},
                'AGCO': {'name': 'AGCO Corp', 'sector': 'Equipamentos', 'subsector': 'Maquinário Agrícola', 'ticker_display': 'AGCO (A1GC34)', 'is_bdr': True},
                
                # Trading e Processamento
                'ADM': {'name': 'Archer Daniels', 'sector': 'Trading', 'subsector': 'Commodities Agrícolas', 'ticker_display': 'ADM (A1DM34)', 'is_bdr': True},
                'BG': {'name': 'Bunge', 'sector': 'Trading', 'subsector': 'Commodities Agrícolas', 'ticker_display': 'BG (B1UN34)', 'is_bdr': True},
                
                # Fertilizantes
                'MOS': {'name': 'Mosaic', 'sector': 'Insumos', 'subsector': 'Fertilizantes', 'ticker_display': 'MOS (M1OS34)', 'is_bdr': True},
                'NTR': {'name': 'Nutrien', 'sector': 'Insumos', 'subsector': 'Fertilizantes', 'ticker_display': 'NTR (N1TR34)', 'is_bdr': True},
                'CF': {'name': 'CF Industries', 'sector': 'Insumos', 'subsector': 'Fertilizantes', 'ticker_display': 'CF (C1F34)', 'is_bdr': True},
                
                # Biotecnologia Agrícola
                'CTVA': {'name': 'Corteva', 'sector': 'Insumos', 'subsector': 'Sementes e Defensivos', 'ticker_display': 'CTVA (C1TX34)', 'is_bdr': True},
            },
            
            # FIAGROs - Fundos de Investimento do Agronegócio
            'fiagros': {
                'RZTR11.SA': {'name': 'Riza Terrax', 'sector': 'FIAGRO', 'subsector': 'Terras Agrícolas', 'ticker_display': 'RZTR11'},
                'LFTS11.SA': {'name': 'Life FII Agro', 'sector': 'FIAGRO', 'subsector': 'Terras Agrícolas', 'ticker_display': 'LFTS11'},
                'GARE11.SA': {'name': 'Guardian Real Estate', 'sector': 'FIAGRO', 'subsector': 'CRA/Imóveis Rurais', 'ticker_display': 'GARE11'},
            },
            
            # ETFs - Agronegócio
            'etfs': {
                'FOOD11.SA': {'name': 'ETF Agronegócio', 'sector': 'ETF', 'subsector': 'Agronegócio BR', 'ticker_display': 'FOOD11'},
            },
            
            # Commodities para Correlação
            'commodities': {
                'ZC=F': {'name': 'Milho Futuro', 'sector': 'Commodity', 'subsector': 'Grãos'},
                'ZS=F': {'name': 'Soja Futuro', 'sector': 'Commodity', 'subsector': 'Grãos'},
                'ZW=F': {'name': 'Trigo Futuro', 'sector': 'Commodity', 'subsector': 'Grãos'},
                'LE=F': {'name': 'Gado Futuro', 'sector': 'Commodity', 'subsector': 'Proteína'},
                'SB=F': {'name': 'Açúcar Futuro', 'sector': 'Commodity', 'subsector': 'Açúcar'},
            }
        }
        
        return database
    
    def get_all_tickers(self):
        """Retorna todos os tickers para monitoramento"""
        tickers = []
        for category in ['acoes_br', 'bdrs', 'fiagros', 'etfs']:
            tickers.extend(list(self.data[category].keys()))
        return tickers
    
    def get_ticker_info(self, ticker):
        """Retorna informações de um ticker específico"""
        for category in self.data.values():
            if ticker in category:
                return category[ticker]
        return None
    
    def get_by_sector(self, sector):
        """Retorna tickers por setor"""
        result = []
        for category in ['acoes_br', 'bdrs', 'fiagros', 'etfs']:
            for ticker, info in self.data[category].items():
                if info['sector'] == sector:
                    result.append((ticker, info))
        return result
    
    def get_market_context(self):
        """Retorna contexto do mercado do agronegócio"""
        return {
            'pib_contribution': '24%',
            'main_products': ['Soja', 'Milho', 'Cana-de-açúcar', 'Café', 'Carne bovina', 'Frango'],
            'brasil_position': {
                'soja': 'Maior produtor mundial',
                'milho': '3º maior produtor (após EUA e China)',
                'cana': 'Maior produtor mundial',
                'cafe': 'Maior produtor e exportador',
                'carne_bovina': 'Um dos maiores exportadores',
            },
            'investment_types': [
                'Ações de empresas do agro',
                'FIAGROs (FIIs do agronegócio)',
                'BDRs de empresas internacionais',
                'LCAs (Letras de Crédito do Agronegócio)',
                'CRAs (Certificados de Recebíveis do Agronegócio)',
                'Mercado Futuro de Commodities',
            ]
        }
