"""
🌾 Sistema Profissional de Monitoramento do Agronegócio
Versão Premium - Análises Avançadas + Gráficos Interativos
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import datetime, timedelta
import json
import numpy as np

# Importa módulos locais
from modules.database import AgroDatabase
from modules.technical_analysis import TechnicalAnalysisEngine
from modules.fundamental_analysis import FundamentalAnalysisEngine
from modules.news_analysis import NewsAnalysisEngine
from modules.monitoring_system import AgroMonitoringSystem

# Configuração da página
st.set_page_config(
    page_title="Agro Monitor Pro",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado PREMIUM
st.markdown("""
<style>
    /* Tema principal */
    .main {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #2d5016 0%, #4a7c2c 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: #f4e4c1;
        font-size: 1.3rem;
        margin-top: 0.5rem;
    }
    
    /* Cards de métricas */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-left: 5px solid #2d5016;
        transition: transform 0.3s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    }
    
    /* Botões */
    .stButton>button {
        background: linear-gradient(135deg, #2d5016 0%, #4a7c2c 100%);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        border: none;
        box-shadow: 0 4px 10px rgba(45, 80, 22, 0.3);
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(45, 80, 22, 0.4);
    }
    
    /* Expander premium */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, #f8f9fa 0%, #ffffff 100%);
        border-radius: 8px;
        font-weight: 600;
        color: #2d5016;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: white;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2d5016 0%, #4a7c2c 100%);
        color: white;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2d5016 0%, #1a3010 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Dataframe */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    /* Badge de score */
    .score-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    .score-high {
        background: #4caf50;
        color: white;
    }
    
    .score-medium {
        background: #ffc107;
        color: #000;
    }
    
    .score-low {
        background: #f44336;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Inicialização
@st.cache_resource
def init_system():
    """Inicializa o sistema (cache para performance)"""
    try:
        finnhub_key = st.secrets.get("FINNHUB_API_KEY", "")
        news_api_key = st.secrets.get("NEWS_API_KEY", "")
        brapi_token = st.secrets.get("BRAPI_API_TOKEN", "")
        
        return AgroMonitoringSystem(
            finnhub_key=finnhub_key,
            news_api_key=news_api_key,
            brapi_token=brapi_token
        )
    except Exception as e:
        st.error(f"Erro ao inicializar sistema: {e}")
        return AgroMonitoringSystem(
            finnhub_key="",
            news_api_key="",
            brapi_token=""
        )

# Funções auxiliares para gráficos
def create_candlestick_chart(ticker, df, indicators):
    """Cria gráfico de candlestick com indicadores"""
    
    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=(
            f'📈 {ticker} - Preço e Indicadores',
            'Volume',
            'RSI (14)',
            'MACD'
        ),
        row_heights=[0.5, 0.15, 0.15, 0.2]
    )
    
    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Preço',
            increasing_line_color='#26a69a',
            decreasing_line_color='#ef5350'
        ),
        row=1, col=1
    )
    
    # Médias Móveis
    if indicators and 'SMA_20' in indicators:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=indicators['SMA_20'],
                name='SMA 20',
                line=dict(color='#ffa726', width=2)
            ),
            row=1, col=1
        )
    
    # Volume
    colors = ['#ef5350' if row['Close'] < row['Open'] else '#26a69a' 
              for _, row in df.iterrows()]
    
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df['Volume'],
            name='Volume',
            marker_color=colors,
            showlegend=False
        ),
        row=2, col=1
    )
    
    # RSI
    if indicators and 'RSI' in indicators:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=indicators['RSI'],
                name='RSI',
                line=dict(color='#ab47bc', width=2)
            ),
            row=3, col=1
        )
        
        # Linhas de sobrecompra/sobrevenda
        fig.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.5, row=3, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.5, row=3, col=1)
    
    # MACD
    if indicators and 'MACD' in indicators:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=indicators['MACD'],
                name='MACD',
                line=dict(color='#42a5f5', width=2)
            ),
            row=4, col=1
        )
    
    # Layout
    fig.update_layout(
        height=1000,
        showlegend=True,
        template='plotly_white',
        hovermode='x unified',
        xaxis_rangeslider_visible=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)')
    
    return fig

def create_score_gauge(score, title):
    """Cria gauge de score"""
    
    color = '#4caf50' if score >= 70 else '#ffc107' if score >= 50 else '#f44336'
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 20, 'color': '#2d5016'}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': '#ffebee'},
                {'range': [40, 70], 'color': '#fff8e1'},
                {'range': [70, 100], 'color': '#e8f5e9'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "#2d5016", 'family': "Arial"}
    )
    
    return fig

def create_sector_comparison(results):
    """Cria gráfico de comparação setorial"""
    
    sector_data = {}
    for result in results:
        sector = result['info']['sector']
        if sector not in sector_data:
            sector_data[sector] = []
        sector_data[sector].append(result['recommendation']['final_score'])
    
    sectors = list(sector_data.keys())
    avg_scores = [np.mean(scores) for scores in sector_data.values()]
    counts = [len(scores) for scores in sector_data.values()]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=sectors,
        y=avg_scores,
        text=[f"{score:.1f}" for score in avg_scores],
        textposition='outside',
        marker=dict(
            color=avg_scores,
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(title="Score Médio")
        ),
        hovertemplate='<b>%{x}</b><br>Score: %{y:.1f}<br>Ativos: %{customdata}<extra></extra>',
        customdata=counts
    ))
    
    fig.update_layout(
        title='📊 Score Médio por Setor',
        xaxis_title='Setor',
        yaxis_title='Score Médio',
        height=400,
        template='plotly_white',
        hovermode='x',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_performance_chart(results):
    """Cria gráfico de performance"""
    
    df_perf = pd.DataFrame([
        {
            'Ticker': r['ticker_display'],
            'Score': r['recommendation']['final_score'],
            'Variação 1M (%)': r['price_data']['change_1m'],
            'Setor': r['info']['sector']
        }
        for r in results
    ])
    
    fig = px.scatter(
        df_perf,
        x='Variação 1M (%)',
        y='Score',
        size='Score',
        color='Setor',
        hover_data=['Ticker'],
        title='🎯 Performance vs Score',
        labels={
            'Variação 1M (%)': 'Variação Mensal (%)',
            'Score': 'Score Final'
        }
    )
    
    fig.add_hline(y=70, line_dash="dash", line_color="green", opacity=0.5,
                  annotation_text="Compra Forte")
    fig.add_hline(y=50, line_dash="dash", line_color="orange", opacity=0.5,
                  annotation_text="Neutro")
    fig.add_vline(x=0, line_dash="dash", line_color="gray", opacity=0.3)
    
    fig.update_layout(
        height=500,
        template='plotly_white',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# Header Premium
st.markdown("""
<div class="main-header">
    <h1>🌾 Agro Monitor Pro</h1>
    <p>Sistema Profissional de Monitoramento do Agronegócio</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Premium
with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    
    # Perfil do investidor
    investor_profile = st.selectbox(
        "👤 Perfil de Investidor",
        ["Conservador", "Moderado", "Arrojado"],
        index=1
    )
    
    # Score mínimo
    min_score = st.slider(
        "📊 Score Mínimo",
        min_value=0,
        max_value=100,
        value=50,
        step=5
    )
    
    # Seleção de ativos
    st.markdown("### 📈 Categorias")
    show_acoes = st.checkbox("Ações BR", value=True)
    show_bdrs = st.checkbox("BDRs", value=True)
    show_fiagros = st.checkbox("FIAGROs", value=True)
    show_etfs = st.checkbox("ETFs", value=True)
    
    st.markdown("---")
    st.markdown("### 📞 Contato")
    st.markdown("📱 **62 99975-5774**")
    st.markdown("[💬 WhatsApp](https://wa.me/5562999755774)")
    
    st.markdown("---")
    st.markdown("### ℹ️ Sobre")
    st.caption("Versão 2.0 Premium")
    st.caption("© 2024 Agro Monitor Pro")

# Tabs principais
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Dashboard",
    "📊 Análise Individual", 
    "📈 Rankings",
    "💼 Portfólio",
    "📚 Educacional",
    "🎯 Comparações"
])

# TAB 1: DASHBOARD PREMIUM
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📊 Visão Geral do Mercado")
    
    with col2:
        if st.button("🔄 Executar Análise Completa", type="primary", use_container_width=True):
            with st.spinner("🔍 Analisando ativos do agronegócio..."):
                try:
                    system = init_system()
                    results = system.scan_all_assets(min_score=min_score)
                    st.session_state['results'] = results
                    st.session_state['last_update'] = datetime.now()
                    st.success(f"✅ {len(results)} oportunidades identificadas!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro: {e}")
    
    # Mostra resultados se existirem
    if 'results' in st.session_state and st.session_state['results']:
        results = st.session_state['results']
        
        # Métricas principais em cards premium
        st.markdown("### 📈 Métricas Principais")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total de Ativos",
                len(results),
                delta=None,
                help="Ativos analisados que atendem o score mínimo"
            )
        
        with col2:
            avg_score = sum(r['recommendation']['final_score'] for r in results) / len(results)
            st.metric(
                "Score Médio",
                f"{avg_score:.1f}",
                delta=f"+{avg_score-50:.1f}" if avg_score > 50 else f"{avg_score-50:.1f}",
                help="Score médio de todos os ativos"
            )
        
        with col3:
            compra_forte = len([r for r in results if 'COMPRA FORTE' in r['recommendation']['action']])
            st.metric(
                "🟢 Compra Forte",
                compra_forte,
                delta=f"{(compra_forte/len(results)*100):.0f}%",
                help="Ativos com recomendação de compra forte"
            )
        
        with col4:
            best = max(results, key=lambda x: x['recommendation']['final_score'])
            st.metric(
                "🏆 Melhor Score",
                f"{best['recommendation']['final_score']:.1f}",
                delta=best['ticker_display'],
                help=f"Melhor ativo: {best['info']['name']}"
            )
        
        st.markdown("---")
        
        # Gráficos de análise
        st.markdown("### 📊 Análises Visuais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                create_sector_comparison(results),
                use_container_width=True
            )
        
        with col2:
            st.plotly_chart(
                create_performance_chart(results),
                use_container_width=True
            )
        
        st.markdown("---")
        
        # Top 10 com design melhorado
        st.markdown("### 🏆 Top 10 Oportunidades")
        
        top_10 = sorted(results, key=lambda x: x['recommendation']['final_score'], reverse=True)[:10]
        
        for i, result in enumerate(top_10, 1):
            score_class = 'score-high' if result['recommendation']['final_score'] >= 70 else 'score-medium' if result['recommendation']['final_score'] >= 50 else 'score-low'
            
            with st.expander(
                f"#{i} - {result['ticker_display']} - {result['info']['name']} • "
                f"Score: {result['recommendation']['final_score']:.1f}",
                expanded=(i <= 3)
            ):
                col1, col2, col3 = st.columns([1, 1, 2])
                
                with col1:
                    st.plotly_chart(
                        create_score_gauge(
                            result['technical']['score']['score'],
                            "Análise Técnica"
                        ),
                        use_container_width=True
                    )
                
                with col2:
                    st.plotly_chart(
                        create_score_gauge(
                            result['fundamental']['score']['score'],
                            "Análise Fundamentalista"
                        ),
                        use_container_width=True
                    )
                
                with col3:
                    st.markdown("#### 📊 Informações Gerais")
                    st.markdown(f"**Setor:** {result['info']['subsector']}")
                    st.markdown(f"**Preço Atual:** R$ {result['price_data']['current']:.2f}")
                    
                    var_color = "green" if result['price_data']['change_1m'] > 0 else "red"
                    st.markdown(f"**Variação 1M:** :{var_color}[{result['price_data']['change_1m']:+.2f}%]")
                    
                    st.markdown(f"**Tendência:** {result['technical']['trend']['trend']}")
                    st.markdown(f"**RSI:** {result['technical']['momentum'].get('rsi', 0):.1f}")
                    
                    if result['fundamental']['valuation']:
                        st.markdown(f"**Valuation:** {result['fundamental']['valuation']['status']}")
                    
                    st.markdown("---")
                    st.markdown(f"### {result['recommendation']['action']}")
                    st.info(f"**Estratégia:** {result['recommendation']['strategy']}")
        
        # Última atualização
        if 'last_update' in st.session_state:
            st.caption(f"🕐 Última atualização: {st.session_state['last_update'].strftime('%d/%m/%Y %H:%M:%S')}")
    else:
        st.info("👆 Clique em 'Executar Análise Completa' para começar")

# TAB 2: ANÁLISE INDIVIDUAL PREMIUM
with tab2:
    st.markdown("### 🔍 Análise Detalhada de Ativo")
    
    system = init_system()
    all_tickers = system.database.get_all_tickers()
    
    # Cria lista com display names
    ticker_options = {}
    for ticker in all_tickers:
        info = system.database.get_ticker_info(ticker)
        if info:
            display = info.get('ticker_display', ticker)
            ticker_options[f"{display} - {info['name']}"] = ticker
    
    selected_option = st.selectbox(
        "Selecione um ativo",
        list(ticker_options.keys())
    )
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        analyze_btn = st.button("📊 Analisar", type="primary", use_container_width=True)
    
    if analyze_btn:
        ticker_real = ticker_options[selected_option]
        
        with st.spinner(f"🔍 Analisando {selected_option.split(' - ')[0]}..."):
            try:
                analysis = system.analyze_asset(ticker_real)
                
                if analysis:
                    st.success(f"✅ Análise concluída!")
                    
                    # Métricas principais
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Score Final", f"{analysis['recommendation']['final_score']:.1f}")
                    with col2:
                        st.metric("Score Técnico", f"{analysis['technical']['score']['score']:.1f}")
                    with col3:
                        st.metric("Score Fundamental", f"{analysis['fundamental']['score']['score']:.1f}")
                    with col4:
                        st.metric("Preço", f"R$ {analysis['price_data']['current']:.2f}")
                    
                    # Recomendação
                    st.markdown("---")
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"### {analysis['recommendation']['action']}")
                        st.info(f"**Estratégia:** {analysis['recommendation']['strategy']}")
                        st.caption(f"**Timeframe:** {analysis['recommendation']['timeframe']}")
                    
                    with col2:
                        st.plotly_chart(
                            create_score_gauge(
                                analysis['recommendation']['final_score'],
                                "Score Final"
                            ),
                            use_container_width=True
                        )
                    
                    # Gráfico de candlestick
                    st.markdown("---")
                    st.markdown("### 📈 Análise Gráfica")
                    
                    tech_engine = TechnicalAnalysisEngine()
                    df = tech_engine.get_price_data(ticker_real, period='6mo')
                    
                    if df is not None and len(df) >= 50:
                        indicators = tech_engine.calculate_indicators(df)
                        
                        fig = create_candlestick_chart(
                            analysis['ticker_display'],
                            df,
                            indicators
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Análise detalhada
                    st.markdown("---")
                    st.markdown("### 📊 Análise Detalhada")
                    
                    tab_tech, tab_fund, tab_news = st.tabs(["📈 Técnica", "💼 Fundamentalista", "📰 Notícias"])
                    
                    with tab_tech:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Tendência**")
                            st.info(analysis['technical']['trend']['trend'])
                            
                            st.markdown("**Momentum**")
                            st.info(f"{analysis['technical']['momentum']['status']} (RSI: {analysis['technical']['momentum'].get('rsi', 0):.1f})")
                        
                        with col2:
                            st.markdown("**MACD**")
                            st.info(analysis['technical']['macd']['signal'])
                            
                            if analysis['technical']['support_resistance']:
                                sr = analysis['technical']['support_resistance']
                                st.markdown("**Suporte/Resistência**")
                                st.success(f"Resistência: R$ {sr['resistance']:.2f} (+{sr['dist_resistance_pct']:.1f}%)")
                                st.error(f"Suporte: R$ {sr['support']:.2f} (-{sr['dist_support_pct']:.1f}%)")
                    
                    with tab_fund:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if analysis['fundamental']['valuation']:
                                st.markdown("**Valuation**")
                                st.info(analysis['fundamental']['valuation']['status'])
                            
                            if analysis['fundamental']['profitability']:
                                st.markdown("**Rentabilidade**")
                                st.info(analysis['fundamental']['profitability']['quality'])
                        
                        with col2:
                            if analysis['fundamental']['growth']:
                                st.markdown("**Crescimento**")
                                st.info(analysis['fundamental']['growth']['status'])
                            
                            if analysis['fundamental']['health']:
                                st.markdown("**Saúde Financeira**")
                                st.info(analysis['fundamental']['health']['health'])
                    
                    with tab_news:
                        sentiment = analysis['news']['sentiment']
                        st.markdown(f"**Sentimento:** {sentiment['sentiment']}")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("🟢 Positivo", sentiment['positive'])
                        with col2:
                            st.metric("🔴 Negativo", sentiment['negative'])
                        with col3:
                            st.metric("⚪ Neutro", sentiment['neutral'])
                else:
                    st.error("❌ Não foi possível analisar este ativo")
            except Exception as e:
                st.error(f"❌ Erro: {e}")

# TAB 3: RANKINGS
with tab3:
    st.markdown("### 📊 Rankings e Comparações")
    
    if 'results' in st.session_state and st.session_state['results']:
        results = st.session_state['results']
        
        # Cria DataFrame
        df_data = []
        for r in results:
            df_data.append({
                'Ticker': r['ticker_display'],
                'Empresa': r['info']['name'],
                'Setor': r['info']['subsector'],
                'Score Final': round(r['recommendation']['final_score'], 1),
                'Técnico': round(r['technical']['score']['score'], 1),
                'Fundamental': round(r['fundamental']['score']['score'], 1),
                'Preço (R$)': round(r['price_data']['current'], 2),
                'Var 1M (%)': round(r['price_data']['change_1m'], 2),
                'Recomendação': r['recommendation']['action']
            })
        
        df = pd.DataFrame(df_data)
        df = df.sort_values('Score Final', ascending=False)
        
        # Filtros
        st.markdown("#### 🔍 Filtros")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sector_filter = st.multiselect(
                "Filtrar por Setor",
                options=df['Setor'].unique(),
                default=[]
            )
        
        with col2:
            score_range = st.slider(
                "Faixa de Score",
                min_value=0,
                max_value=100,
                value=(0, 100)
            )
        
        with col3:
            action_filter = st.multiselect(
                "Filtrar por Recomendação",
                options=df['Recomendação'].unique(),
                default=[]
            )
        
        # Aplica filtros
        df_filtered = df.copy()
        
        if sector_filter:
            df_filtered = df_filtered[df_filtered['Setor'].isin(sector_filter)]
        
        df_filtered = df_filtered[
            (df_filtered['Score Final'] >= score_range[0]) &
            (df_filtered['Score Final'] <= score_range[1])
        ]
        
        if action_filter:
            df_filtered = df_filtered[df_filtered['Recomendação'].isin(action_filter)]
        
        # Exibe tabela estilizada
        st.markdown(f"**{len(df_filtered)} ativos encontrados**")
        
        # Estiliza DataFrame
        def highlight_score(val):
            if val >= 70:
                return 'background-color: #c8e6c9'
            elif val >= 50:
                return 'background-color: #fff9c4'
            else:
                return 'background-color: #ffcdd2'
        
        styled_df = df_filtered.style.applymap(
            highlight_score,
            subset=['Score Final']
        )
        
        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True,
            height=600
        )
        
        # Botões de exportação
        col1, col2, col3 = st.columns([1, 1, 3])
        
        with col1:
            csv = df_filtered.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Baixar CSV",
                data=csv,
                file_name=f'agro_ranking_{datetime.now().strftime("%Y%m%d")}.csv',
                mime='text/csv',
                use_container_width=True
            )
        
        with col2:
            # Botão de exportação Excel (requer openpyxl)
            try:
                from io import BytesIO
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df_filtered.to_excel(writer, index=False, sheet_name='Rankings')
                
                st.download_button(
                    label="📥 Baixar Excel",
                    data=buffer.getvalue(),
                    file_name=f'agro_ranking_{datetime.now().strftime("%Y%m%d")}.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    use_container_width=True
                )
            except:
                pass
        
    else:
        st.info("👆 Execute a análise completa na aba Dashboard primeiro")

# TAB 4: PORTFÓLIO PERSONALIZADO
with tab4:
    st.markdown("### 💼 Recomendações por Perfil de Investidor")
    
    if 'results' in st.session_state and st.session_state['results']:
        results = st.session_state['results']
        
        profile = investor_profile.lower()
        
        # Card de perfil
        if profile == 'conservador':
            st.markdown("""
            <div style='background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%); 
                        padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem;'>
                <h2>🛡️ Perfil Conservador</h2>
                <p style='font-size: 1.2rem; margin-bottom: 0;'>
                    Foco em empresas consolidadas com forte fundamentação financeira e menor volatilidade.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            recommendations = [r for r in results if r['fundamental']['score']['score'] >= 70]
            recommendations.sort(key=lambda x: x['fundamental']['score']['score'], reverse=True)
        
        elif profile == 'moderado':
            st.markdown("""
            <div style='background: linear-gradient(135deg, #ffa726 0%, #fb8c00 100%); 
                        padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem;'>
                <h2>⚖️ Perfil Moderado</h2>
                <p style='font-size: 1.2rem; margin-bottom: 0;'>
                    Equilíbrio entre análise técnica e fundamentalista para risco/retorno balanceado.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            recommendations = [r for r in results if r['recommendation']['final_score'] >= 65]
            recommendations.sort(key=lambda x: x['recommendation']['final_score'], reverse=True)
        
        else:  # arrojado
            st.markdown("""
            <div style='background: linear-gradient(135deg, #e53935 0%, #c62828 100%); 
                        padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem;'>
                <h2>🚀 Perfil Arrojado</h2>
                <p style='font-size: 1.2rem; margin-bottom: 0;'>
                    Foco em momentum e tendências técnicas para oportunidades de maior retorno.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            recommendations = [r for r in results if r['technical']['score']['score'] >= 60]
            recommendations.sort(key=lambda x: x['technical']['score']['score'], reverse=True)
        
        # Top 10 recomendações
        st.markdown("### 🏆 Top 10 Recomendações para seu Perfil")
        
        if len(recommendations) == 0:
            st.warning("Nenhum ativo atende aos critérios do seu perfil. Ajuste o score mínimo nas configurações.")
        else:
            for i, rec in enumerate(recommendations[:10], 1):
                with st.container():
                    col1, col2, col3, col4 = st.columns([1, 2, 1, 2])
                    
                    with col1:
                        st.markdown(f"### #{i}")
                        st.markdown(f"**{rec['ticker_display']}**")
                    
                    with col2:
                        st.markdown(f"**{rec['info']['name']}**")
                        st.caption(f"{rec['info']['subsector']}")
                    
                    with col3:
                        score_color = "🟢" if rec['recommendation']['final_score'] >= 70 else "🟡"
                        st.metric("Score", f"{score_color} {rec['recommendation']['final_score']:.1f}")
                    
                    with col4:
                        st.markdown(f"**{rec['recommendation']['action']}**")
                        st.caption(f"R$ {rec['price_data']['current']:.2f}")
                    
                    st.markdown("---")
            
            # Gráfico de distribuição do portfólio
            st.markdown("### 📊 Distribuição por Setor")
            
            sector_dist = {}
            for rec in recommendations[:10]:
                sector = rec['info']['sector']
                sector_dist[sector] = sector_dist.get(sector, 0) + 1
            
            fig = go.Figure(data=[go.Pie(
                labels=list(sector_dist.keys()),
                values=list(sector_dist.values()),
                hole=.4,
                marker=dict(colors=px.colors.qualitative.Set3)
            )])
            
            fig.update_layout(
                title='Diversificação Setorial do Portfólio Sugerido',
                height=400,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👆 Execute a análise completa na aba Dashboard primeiro")

# TAB 5: EDUCACIONAL
with tab5:
    st.markdown("### 📚 Sobre o Agronegócio Brasileiro")
    
    context = AgroDatabase().get_market_context()
    
    # Cards informativos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #2d5016 0%, #4a7c2c 100%); 
                    padding: 2rem; border-radius: 15px; color: white; margin-bottom: 1rem;'>
            <h3>🌾 Participação no PIB</h3>
            <h1 style='font-size: 4rem; margin: 1rem 0;'>24%</h1>
            <p>O agronegócio representa quase 1/4 do PIB brasileiro</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 🏆 Posição Global do Brasil")
        for product, position in context['brasil_position'].items():
            st.success(f"**{product.replace('_', ' ').title()}:** {position}")
    
    with col2:
        st.markdown("#### 📦 Principais Produtos")
        for product in context['main_products']:
            st.info(f"🌾 {product}")
        
        st.markdown("#### 💼 Formas de Investir")
        for inv_type in context['investment_types']:
            st.write(f"✅ {inv_type}")
    
    st.markdown("---")
    
    # Seção educativa expandida
    with st.expander("📖 Guia Completo de Investimento no Agronegócio", expanded=False):
        st.markdown("""
        ### Por que investir no Agronegócio?
        
        O agronegócio brasileiro é reconhecido mundialmente pela sua competitividade e inovação. 
        Investir neste setor oferece:
        
        - **Diversificação**: Exposição a diferentes segmentos (grãos, proteínas, insumos, etc)
        - **Proteção contra inflação**: Commodities tendem a acompanhar a inflação
        - **Crescimento populacional**: Demanda mundial por alimentos em expansão
        - **Vantagens competitivas**: Brasil possui clima, tecnologia e escala
        
        ### Como Analisar Empresas do Setor
        
        **Análise Fundamentalista:**
        - Margem operacional e EBITDA
        - Endividamento (Dívida/EBITDA)
        - Eficiência operacional
        - Exposição cambial
        
        **Análise Técnica:**
        - Tendências de commodities
        - Sazonalidade das safras
        - Padrões de preços históricos
        
        ### Riscos a Considerar
        
        - **Climáticos**: Secas, geadas, excesso de chuvas
        - **Commodities**: Volatilidade de preços internacionais
        - **Cambiais**: Exposição ao dólar
        - **Regulatórios**: Mudanças em políticas agrícolas
        """)

# TAB 6: COMPARAÇÕES AVANÇADAS
with tab6:
    st.markdown("### 🎯 Análises Comparativas Avançadas")
    
    if 'results' in st.session_state and st.session_state['results']:
        results = st.session_state['results']
        
        # Seletor de ativos para comparar
        st.markdown("#### Selecione ativos para comparar")
        
        ticker_options_compare = {
            r['ticker_display']: r for r in results
        }
        
        selected_tickers = st.multiselect(
            "Escolha de 2 a 5 ativos",
            options=list(ticker_options_compare.keys()),
            max_selections=5
        )
        
        if len(selected_tickers) >= 2:
            selected_results = [ticker_options_compare[t] for t in selected_tickers]
            
            # Comparação de scores
            st.markdown("#### 📊 Comparação de Scores")
            
            categories = ['Score Final', 'Técnico', 'Fundamentalista']
            
            fig = go.Figure()
            
            for result in selected_results:
                fig.add_trace(go.Bar(
                    name=result['ticker_display'],
                    x=categories,
                    y=[
                        result['recommendation']['final_score'],
                        result['technical']['score']['score'],
                        result['fundamental']['score']['score']
                    ],
                    text=[
                        f"{result['recommendation']['final_score']:.1f}",
                        f"{result['technical']['score']['score']:.1f}",
                        f"{result['fundamental']['score']['score']:.1f}"
                    ],
                    textposition='outside'
                ))
            
            fig.update_layout(
                barmode='group',
                title='Comparação de Scores',
                yaxis_title='Score',
                height=400,
                template='plotly_white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabela comparativa
            st.markdown("#### 📋 Tabela Comparativa Detalhada")
            
            comparison_data = []
            for result in selected_results:
                comparison_data.append({
                    'Ativo': result['ticker_display'],
                    'Empresa': result['info']['name'],
                    'Setor': result['info']['subsector'],
                    'Preço': f"R$ {result['price_data']['current']:.2f}",
                    'Var 1M': f"{result['price_data']['change_1m']:+.2f}%",
                    'Score Final': result['recommendation']['final_score'],
                    'Técnico': result['technical']['score']['score'],
                    'Fundamental': result['fundamental']['score']['score'],
                    'Tendência': result['technical']['trend']['trend'],
                    'RSI': f"{result['technical']['momentum'].get('rsi', 0):.1f}",
                    'Recomendação': result['recommendation']['action']
                })
            
            df_comparison = pd.DataFrame(comparison_data)
            st.dataframe(df_comparison, use_container_width=True, hide_index=True)
            
        elif len(selected_tickers) == 1:
            st.info("Selecione pelo menos mais um ativo para comparar")
        else:
            st.info("Selecione 2 ou mais ativos para começar a comparação")
    else:
        st.info("👆 Execute a análise completa na aba Dashboard primeiro")

# Footer Premium
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #2d5016 0%, #4a7c2c 100%); 
                border-radius: 15px; color: white;'>
        <h3>🌾 Agro Monitor Pro</h3>
        <p style='font-size: 1.1rem;'>Sistema Profissional de Monitoramento do Agronegócio</p>
        <p style='margin-top: 1rem;'>
            📱 Contato: <strong>62 99975-5774</strong> | 
            <a href='https://wa.me/5562999755774' style='color: #90ee90;'>WhatsApp</a>
        </p>
        <p style='margin-top: 0.5rem; font-size: 0.9rem; opacity: 0.8;'>
            © 2024 Agro Monitor Pro | Versão 2.0 Premium
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
