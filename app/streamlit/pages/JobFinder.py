import streamlit as st
import pandas as pd
from utils import *
import time
import random

def response_generator():

    response = random.choice(
        [
            "Ok, aguarde alguns segundos que irei buscar a vaga ideal.",
            "Ótimo! Vou procurar a vaga perfeita para você, um segundo.",
            "Aguarde um momento que irei olhar nos meus arquivos.",
            "Perfeito! Um segundo que vou achar as vagas ideais para você.",
            "Tenho a vaga perfeita nos meus arquivos! Um segundo que vou pegar ela para você.",
            "Entendido! Tenho exatamente o que você precisa. Aguarde um momento.",
            "Maravilha! Já sei o que você precisa. Vou buscar a vaga ideal para você.",
        ]
    )

    for word in response.split():
        yield word + " "
        time.sleep(0.05)

def JobFinder():
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
        with st.chat_message("user"): st.markdown(input_user)

        # Adiciona a mensagem do usuário na variável de ambiente (histórico de mensagens)
        st.session_state.messages.append({"role": "user", "content": input_user})

        # -----------------ASSISTENTE--------------------
        # Exibe a resposta do assistente
        with st.chat_message("assistant"): response = st.write_stream(response_generator())

        # Adiciona a mensagem do assistente na variável de ambiente (histórico de mensagens)
        st.session_state.messages.append({"role": "assistant", "content": response})



