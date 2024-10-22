import streamlit as st
import requests

st.title("Meu App Streamlit")

response = requests.get("http://localhost:8000/data")
data = response.json()

st.write(data)