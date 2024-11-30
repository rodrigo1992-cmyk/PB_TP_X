import streamlit as st
import pandas as pd
from utils import *



def exibir():
    st.title("Visualização das Vagas Anunciadas")

    # -----------------INICIALIZAÇÃO--------------------
    # Inicializar variável de ambiente
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Olá! Sou seu assistente de carreira. Me diga o que busca em uma vaga de emprego, que irei ajudar a encontrar a melhor oportunidade para você!"}]

    # Exibe as mensagens armazenadas no histórico  (Se não tiver essa parte toda vez que é digitada uma nova mensagem o chat é limpo)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    # -----------------USUÁRIO--------------------
    # Cria a caixa de input e exibe um placeholder. Se foi digitado algo na caixa, atribui o valor a variável input_user
    if input_user := st.chat_input("Digite aqui"):

        # Exibe no chat a mensagem que o usuário havia inputado
        with st.chat_message("user"): 
            st.markdown(input_user)

        # Adiciona a mensagem do usuário na variável de ambiente (histórico de mensagens)
        st.session_state.messages.append({"role": "user", "content": input_user})

        # -----------------ASSISTENTE--------------------
        # Exibe a resposta do assistente
        with st.chat_message("assistant"): 
            response = st.write_stream(typing_effect(msg_wait_a_sec()))

        # Adiciona a mensagem do assistente na variável de ambiente (histórico de mensagens)
        st.session_state.messages.append({"role": "assistant", "content": response})

        #-----------------CHAMADA À API-------------------
        with st.chat_message("assistant"): 
            response = st.write_stream(typing_effect(api_post_llm_search(input_user)))

        # Adiciona a mensagem do assistente na variável de ambiente (histórico de mensagens)
        st.session_state.messages.append({"role": "assistant", "content": response})


