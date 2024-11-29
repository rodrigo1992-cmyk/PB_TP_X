import streamlit as st
from app.services.functions_graphs import *

def exibir():
    st.title("Análise dos Diferentes Perfis de Profissionais de Dados")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<h4 style='text-align: center; color: black;'>Histórico de Vagas Anunciadas (por Semana)</h4>", unsafe_allow_html=True)
        plot_historico_vagas(st.session_state.df_vagas_filt)

        st.markdown("<h4 style='text-align: center; color: black;'>Distribuição de Vagas por Perfil e Senioridade</h4>", unsafe_allow_html=True)
        plot_dist_senioridade(st.session_state.df_vagas_filt)

        st.markdown("<h4 style='text-align: center; color: black;'>Hard Skills mais Requisitados</h4>", unsafe_allow_html=True)
        top_requisitos(st.session_state.df_vagas_filt, st.session_state.df_requisitos)
        
    with col_b:

        st.markdown("<h4 style='text-align: center; color: black;'>Comparação de Salários por Perfil</h4>", unsafe_allow_html=True)
        plot_box_salarios(st.session_state.df_vagas_filt)

        st.markdown("<h4 style='text-align: center; color: black;'>Distribuição de Vagas por localidade</h4>", unsafe_allow_html=True)
        plot_dist_regiao(st.session_state.df_vagas_filt)

        st.markdown("<h4 style='text-align: center; color: black;'>Wordcloud - Hard Skills mais Requisitados</h4>", unsafe_allow_html=True)
        st.markdown("### ")
        plot_wordcloud(st.session_state.df_requisitos)

    st.markdown("<h4 style='text-align: center; color: black;'>Diagrama Ternário (Hard Skills x Perfil)</h4>", unsafe_allow_html=True)

    plot_ternario_requisitos(st.session_state.df_vagas, st.session_state.df_ternario_filt, st.session_state.df_requisitos)
