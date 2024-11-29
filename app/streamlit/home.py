from app.router.paths import *

import streamlit as st
from streamlit_navigation_bar import st_navbar
import pandas as pd
import pages as pg
from utils import *


st.set_page_config(layout="wide", page_title="DataJobs Finder", page_icon="🔎",initial_sidebar_state="collapsed")

#-------------Cria a Barra de Navegação----------------
styles = {"div": {"max-width": "350px"}}  # Reduce the page names spacing.
lista_pages = ["Home", "About", "Job Finder", "Profile Analysis"]
page = st_navbar(lista_pages, styles=styles, options={"hide_nav":True})


#-------------Inicializa a página selecionada----------------
if page == "About":
    pg.About()
if page == "Job Finder":
    pg.JobFinder()
if page == "Profile Analysis":
    pg.ProfileAnalysis()
