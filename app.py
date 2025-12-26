"""
🌾 Sistema Profissional de Monitoramento do Agronegócio
Versão Streamlit - Deploy Ready
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import json

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

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2d5016;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #2d5016 0%, #4a7c2c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stButton>button {
        background-color: #2d5016;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 2rem;
    }
    .stButton>button:hover {
        background-color: #4a7c2c;
    }
</style>
""", unsafe_allow_html=True)

# Inicialização
@st.cache_resource
def init_system():
    """Inicializa o sistema (cache para performance)"""
    return AgroMonitoringSystem(
        finnhub_key=st.secrets["FINNHUB_API_KEY"],
        news_api_key=st.secrets["NEWS_API_KEY"],
        brapi_token=st.secrets["BRAPI_API_TOKEN"]
    )

# Header
st.markdown('<h1 class="main-header">🌾 Agro Monitor Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; font-size: 1.2rem;">Sistema Profissional de Monitoramento do Agronegócio</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/2d5016/ffffff?text=Agro+Monitor", use_container_width=True)
    
    st.markdown("### ⚙️ Configurações")
    
    # Perfil do investidor
    investor_profile = st.selectbox(
        "Perfil de Investidor",
        ["Conservador", "Moderado", "Arrojado"],
        index=1
    )
    
    # Score mínimo
    min_score = st.slider(
        "Score Mínimo",
        min_value=0,
        max_value=100,
        value=50,
        step=5
    )
    
    # Seleção de ativos
    st.markdown("### 📊 Categorias")
    show_acoes = st.checkbox("Ações BR", value=True)
    show_bdrs = st.checkbox("BDRs", value=True)
    show_fiagros = st.checkbox("FIAGROs", value=True)
    show_etfs = st.checkbox("ETFs", value=True)
    
    st.markdown("---")
    st.markdown("### 📞 Contato")
    st.markdown("📱 62 99975-5774")
    st.markdown("[WhatsApp](https://wa.me/5562999755774)")

# Tabs principais
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Dashboard",
    "📊 Análise Individual", 
    "📈 Rankings",
    "💼 Portfólio",
    "📚 Educacional"
])

# TAB 1: DASHBOARD
with tab1:
    st.header("📊 Visão Geral do Mercado")
    
    # Botão de análise
    if st.button("🔄 Executar Análise Completa", type="primary"):
        with st.spinner("Analisando ativos do agronegócio..."):
            try:
                system = init_system()
                
                # Executa varredura
                results = system.scan_all_assets(min_score=min_score)
                
                # Salva em session_state
                st.session_state['results'] = results
                st.session_state['last_update'] = datetime.now()
                
                st.success(f"✅ Análise concluída! {len(results)} oportunidades identificadas")
                
            except Exception as e:
                st.error(f"❌ Erro na análise: {e}")
    
    # Mostra resultados se existirem
    if 'results' in st.session_state and st.session_state['results']:
        results = st.session_state['results']
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total de Ativos",
                len(results),
                delta=None
            )
        
        with col2:
            avg_score = sum(r['recommendation']['final_score'] for r in results) / len(results)
            st.metric(
                "Score Médio",
                f"{avg_score:.1f}",
                delta=None
            )
        
        with col3:
            compra_forte = len([r for r in results if 'COMPRA FORTE' in r['recommendation']['action']])
            st.metric(
                "🟢 Compra Forte",
                compra_forte,
                delta=None
            )
        
        with col4:
            best = max(results, key=lambda x: x['recommendation']['final_score'])
            st.metric(
                "🏆 Melhor Score",
                f"{best['ticker_display']} ({best['recommendation']['final_score']:.1f})",
                delta=None
            )
        
        st.markdown("---")
        
        # Top 10 Oportunidades
        st.subheader("🏆 Top 10 Oportunidades")
        
        top_10 = sorted(results, key=lambda x: x['recommendation']['final_score'], reverse=True)[:10]
        
        for i, result in enumerate(top_10, 1):
            with st.expander(f"#{i} - {result['ticker_display']} - {result['info']['name']} (Score: {result['recommendation']['final_score']:.1f})"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**📊 Análise Técnica**")
                    st.write(f"Score: {result['technical']['score']['score']:.1f}")
                    st.write(f"Tendência: {result['technical']['trend']['trend']}")
                    st.write(f"RSI: {result['technical']['momentum'].get('rsi', 0):.1f}")
                
                with col2:
                    st.markdown("**💼 Análise Fundamentalista**")
                    st.write(f"Score: {result['fundamental']['score']['score']:.1f}")
                    if result['fundamental']['valuation']:
                        st.write(f"Valuation: {result['fundamental']['valuation']['status']}")
                    if result['fundamental']['profitability']:
                        st.write(f"Rentabilidade: {result['fundamental']['profitability']['quality']}")
                
                with col3:
                    st.markdown("**🎯 Recomendação**")
                    st.write(f"Ação: {result['recommendation']['action']}")
                    st.write(f"Prioridade: {result['recommendation']['priority']}")
                    st.write(f"Preço: R$ {result['price_data']['current']:.2f}")
        
        # Última atualização
        if 'last_update' in st.session_state:
            st.caption(f"Última atualização: {st.session_state['last_update'].strftime('%d/%m/%Y %H:%M:%S')}")

# TAB 2: ANÁLISE INDIVIDUAL
with tab2:
    st.header("🔍 Análise Detalhada de Ativo")
    
    # Seleção de ticker
    system = init_system()
    all_tickers = system.database.get_all_tickers()
    
    # Cria lista com display names
    ticker_options = []
    for ticker in all_tickers:
        info = system.database.get_ticker_info(ticker)
        if info:
            display = info.get('ticker_display', ticker)
            ticker_options.append(f"{display} - {info['name']}")
    
    selected_option = st.selectbox("Selecione um ativo", ticker_options)
    
    if st.button("📊 Analisar Ativo", type="primary"):
        # Extrai ticker real
        ticker_display = selected_option.split(" - ")[0]
        
        # Busca ticker real no database
        ticker_real = None
        for ticker in all_tickers:
            info = system.database.get_ticker_info(ticker)
            if info and info.get('ticker_display') == ticker_display:
                ticker_real = ticker
                break
        
        if ticker_real:
            with st.spinner(f"Analisando {ticker_display}..."):
                try:
                    analysis = system.analyze_asset(ticker_real)
                    
                    if analysis:
                        # Dashboard do ativo
                        st.success(f"✅ Análise de {analysis['ticker_display']} concluída!")
                        
                        # Métricas
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Score Final", f"{analysis['recommendation']['final_score']:.1f}")
                        with col2:
                            st.metric("Score Técnico", f"{analysis['technical']['score']['score']:.1f}")
                        with col3:
                            st.metric("Score Fundamental", f"{analysis['fundamental']['score']['score']:.1f}")
                        with col4:
                            st.metric("Preço Atual", f"R$ {analysis['price_data']['current']:.2f}")
                        
                        # Recomendação destacada
                        st.markdown("---")
                        st.markdown(f"### {analysis['recommendation']['action']}")
                        st.info(f"**Estratégia:** {analysis['recommendation']['strategy']}")
                        
                        # Gráfico (simplificado para exemplo)
                        st.markdown("---")
                        st.subheader("📈 Gráfico de Preços")
                        st.info("Gráfico interativo será implementado aqui")
                        
                    else:
                        st.error("❌ Não foi possível analisar este ativo")
                        
                except Exception as e:
                    st.error(f"❌ Erro: {e}")

# TAB 3: RANKINGS
with tab3:
    st.header("📊 Rankings e Comparações")
    
    if 'results' in st.session_state and st.session_state['results']:
        results = st.session_state['results']
        
        # Cria DataFrame
        df_data = []
        for r in results:
            df_data.append({
                'Ticker': r['ticker_display'],
                'Empresa': r['info']['name'],
                'Setor': r['info']['subsector'],
                'Score Final': r['recommendation']['final_score'],
                'Score Técnico': r['technical']['score']['score'],
                'Score Fundamental': r['fundamental']['score']['score'],
                'Preço': r['price_data']['current'],
                'Var 1M (%)': r['price_data']['change_1m'],
                'Recomendação': r['recommendation']['action']
            })
        
        df = pd.DataFrame(df_data)
        df = df.sort_values('Score Final', ascending=False)
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            sector_filter = st.multiselect(
                "Filtrar por Setor",
                options=df['Setor'].unique()
            )
        
        with col2:
            action_filter = st.multiselect(
                "Filtrar por Recomendação",
                options=df['Recomendação'].unique()
            )
        
        # Aplica filtros
        if sector_filter:
            df = df[df['Setor'].isin(sector_filter)]
        if action_filter:
            df = df[df['Recomendação'].isin(action_filter)]
        
        # Exibe tabela
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
        
        # Botão de download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Relatório CSV",
            data=csv,
            file_name=f'agro_monitor_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv'
        )
    else:
        st.info("Execute a análise completa na aba Dashboard primeiro")

# TAB 4: PORTFÓLIO
with tab4:
    st.header("💼 Recomendações por Perfil")
    
    if 'results' in st.session_state and st.session_state['results']:
        results = st.session_state['results']
        
        profile = investor_profile.lower()
        
        st.markdown(f"### Portfólio Sugerido: {investor_profile}")
        
        if profile == 'conservador':
            st.info("🛡️ Foco em empresas consolidadas com bons fundamentals")
            recommendations = [r for r in results if r['fundamental']['score']['score'] >= 70]
            recommendations.sort(key=lambda x: x['fundamental']['score']['score'], reverse=True)
        
        elif profile == 'moderado':
            st.info("⚖️ Equilíbrio entre análise técnica e fundamentalista")
            recommendations = [r for r in results if r['recommendation']['final_score'] >= 65]
            recommendations.sort(key=lambda x: x['recommendation']['final_score'], reverse=True)
        
        else:  # arrojado
            st.info("🚀 Foco em oportunidades de momentum e tendência")
            recommendations = [r for r in results if r['technical']['score']['score'] >= 60]
            recommendations.sort(key=lambda x: x['technical']['score']['score'], reverse=True)
        
        # Top 5 recomendações
        for i, rec in enumerate(recommendations[:5], 1):
            with st.container():
                col1, col2, col3 = st.columns([2, 3, 2])
                
                with col1:
                    st.markdown(f"**#{i} - {rec['ticker_display']}**")
                    st.caption(rec['info']['name'])
                
                with col2:
                    st.metric("Score", f"{rec['recommendation']['final_score']:.1f}")
                
                with col3:
                    st.markdown(f"**{rec['recommendation']['action']}**")
                
                st.markdown("---")
    else:
        st.info("Execute a análise completa na aba Dashboard primeiro")

# TAB 5: EDUCACIONAL
with tab5:
    st.header("📚 Sobre o Agronegócio Brasileiro")
    
    context = AgroDatabase().get_market_context()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌾 Participação no PIB")
        st.metric("PIB do Agronegócio", context['pib_contribution'])
        
        st.subheader("🏆 Posição Global do Brasil")
        for product, position in context['brasil_position'].items():
            st.write(f"**{product.replace('_', ' ').title()}:** {position}")
    
    with col2:
        st.subheader("📦 Principais Produtos")
        for product in context['main_products']:
            st.write(f"• {product}")
        
        st.subheader("💼 Formas de Investir")
        for inv_type in context['investment_types']:
            st.write(f"• {inv_type}")
    
    st.markdown("---")
    st.info("💡 **Dica:** O agronegócio é um dos pilares da economia brasileira e oferece diversas oportunidades de investimento!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>🌾 Agro Monitor Pro | Sistema Profissional de Monitoramento do Agronegócio</p>
        <p>📱 Contato: 62 99975-5774 | <a href='https://wa.me/5562999755774'>WhatsApp</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
