# 🌾 Agro Monitor Pro

Sistema Profissional de Monitoramento do Agronegócio com Análise Técnica e Fundamentalista.

## 📊 Funcionalidades

- ✅ Análise de 27+ ativos do agronegócio (Ações, BDRs, FIAGROs, ETFs)
- ✅ 15+ indicadores técnicos (RSI, MACD, Bandas de Bollinger, etc.)
- ✅ Análise fundamentalista completa (P/L, ROE, Margens, Crescimento)
- ✅ Score inteligente de 0 a 100
- ✅ Recomendações personalizadas por perfil de investidor
- ✅ Comparação com Índice IAGRO (B3)
- ✅ Dashboards interativos e gráficos profissionais
- ✅ Exportação de relatórios (CSV, Excel, JSON)

## 🚀 Como Usar

### Instalação Local

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/agro-monitor-pro.git
cd agro-monitor-pro

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt

# Configure as chaves de API
# Crie o arquivo .streamlit/secrets.toml com suas chaves

# Execute o aplicativo
streamlit run app.py
```

### Deploy no Streamlit Cloud

1. Faça fork deste repositório
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte seu repositório GitHub
4. Configure os secrets no painel do Streamlit
5. Deploy automático!

## 🔑 Configuração de APIs

O sistema utiliza 3 APIs gratuitas:

1. **Finnhub** (notícias financeiras)
   - Cadastre-se em: https://finnhub.io
   - Plano gratuito: 60 chamadas/minuto

2. **News API** (notícias gerais)
   - Cadastre-se em: https://newsapi.org
   - Plano gratuito: 100 requests/dia

3. **Brapi** (dados da B3)
   - Cadastre-se em: https://brapi.dev
   - Plano gratuito: 150 requests/dia

Configure as chaves em `.streamlit/secrets.toml`:

```toml
FINNHUB_API_KEY = "sua_chave_aqui"
NEWS_API_KEY = "sua_chave_aqui"
BRAPI_API_TOKEN = "sua_chave_aqui"
```

## 📁 Estrutura do Projeto

```
agro-monitor-pro/
├── app.py                      # Aplicação Streamlit principal
├── modules/
│   ├── __init__.py
│   ├── database.py             # Base de dados dos ativos
│   ├── technical_analysis.py  # Motor de análise técnica
│   ├── fundamental_analysis.py # Motor de análise fundamentalista
│   ├── news_analysis.py        # Análise de notícias
│   └── monitoring_system.py    # Sistema integrado
├── requirements.txt            # Dependências Python
├── .streamlit/
│   └── secrets.toml           # Chaves de API (NÃO commitar!)
├── .gitignore
└── README.md
```

## 💼 Ativos Monitorados

### Ações Brasileiras (14)
- BEEF3, MRFG3, JBSS3, BRFS3 (Frigoríficos)
- ABEV3, MDIA3 (Bebidas e Alimentos)
- SMTO3, RAIZ4, CSAN3 (Bioenergia)
- SUZB3, KLBN11 (Papel e Celulose)
- SLCE3, AGRO3 (Terras Agrícolas)
- SOJA3 (Sementes)

### BDRs Internacionais (8)
- DE, AGCO (Equipamentos)
- ADM, BG (Trading)
- MOS, NTR, CF (Fertilizantes)
- CTVA (Biotecnologia)

### FIAGROs (3)
- RZTR11, LFTS11, GARE11

### ETFs (2)
- FOOD11, CMBB11

## 📊 Indicadores Técnicos

- Médias Móveis (SMA 20, 50, 200 / EMA 12, 26)
- MACD (Moving Average Convergence Divergence)
- RSI (Relative Strength Index)
- Estocástico
- Bandas de Bollinger
- ATR (Average True Range)
- ADX (Average Directional Index)
- Suporte e Resistência

## 💡 Perfis de Investidor

### 🛡️ Conservador
- Foco em empresas consolidadas
- Score Fundamentalista > 70
- Menor volatilidade

### ⚖️ Moderado
- Equilíbrio técnico/fundamentalista
- Score Final > 65
- Balanço risco/retorno

### 🚀 Arrojado
- Foco em momentum
- Score Técnico > 60
- Oportunidades de curto prazo

## 🌾 Sobre o Agronegócio Brasileiro

- 📊 **24% do PIB** brasileiro
- 🌎 **Líder mundial** em soja, cana-de-açúcar e café
- 🥇 **3º maior produtor** de milho
- 🥩 **Grande exportador** de carne bovina e frango

## 📞 Contato

- 📱 WhatsApp: (62) 99975-5774
- 📧 Email: contato@seu-email.com

## 📝 Licença

Este projeto é fornecido "como está", sem garantias de qualquer tipo.

## ⚠️ Aviso Legal

Este sistema é uma ferramenta de análise e não constitui recomendação de investimento. Sempre consulte um profissional certificado antes de tomar decisões financeiras.

---

Desenvolvido com 💚 para o Agronegócio Brasileiro
