import streamlit as st
from streamlitDB import db 
import pandas as pd
import numpy as np 
import time


db = db({
    'dbname': 'usuarios',
    'user': 'postgres',
    'password': 'admin',
    'host': 'd1a6c80cae46',
    'port': '5432'
})

def view():
    st.title("Clientes cadastrados!")

    data = db.ler_dados()
    df = pd.DataFrame(data=data, columns=["ID", "NOME", "EMAIL"])

    try:
        if data:
            st.dataframe(df.style.hide(axis="index"))
    except Exception as e:
        st.warning(e)
        
def insert():
    st.title("Inserir registro")
    st.write("Preencha o formulário abaixo:")
    nome = st.text_input("Nome:")
    email = st.text_input("Email:")
    enviado = st.button("Enviar")
    if enviado:
        db.inserir_dados(nome, email)
        st.success((nome, " inserido!"))    

def show_modify_form(idA):
    
    st.title("Modificar registro")
    st.write("Preencha o formulário abaixo:")
    data = db.buscar_por_id(idA)
    if data:
        nomeA = st.text_input("Nome:", value=data[1], key="nomeA_input")
        emailA = st.text_input("Email:", value=data[2], key="emailA_input")
    else:
        st.warning("Nenhum dado encontrado.")

    
    col1, col2 = st.columns((7, 1))
    
    with col1:
        update = st.button("Atualizar")
        if update:
            db.atualizar_dados(idA, nomeA, emailA)
            st.success(f"{data[1]} atualizado! \n Resultado: {nomeA}, {emailA}")


    with col2:
        delete = st.button("Deletar")
        if delete:
            try:
                db.deletar_dados(idA)
                st.success(f"{nomeA} excluído com sucesso.")
            except Exception as e:
                st.error(f'Erro ao deletar: {e}')
def buscarNome():
    st.title("Buscar por nome e email")

    with st.form(key='search_form'):
        nome = st.text_input("Nome:", key="nome_input")
        search = st.form_submit_button("Pesquisar")
    
    if search:
        try:
            data = db.buscar_por_nome(nome)
            df = pd.DataFrame(data=data, columns=["ID", "NOME", "EMAIL"])
            if data:
                st.dataframe(df.style.hide(axis="index"))         
            else:
                st.warning("Registros não encontrados.")
        except Exception as e:
            st.warning("Erro durante a pesquisa.")
def buscar(session_state):
    st.title("Buscar por nome e email")

    with st.form(key='search_form'):
        nome = st.text_input("Nome:", key="nome_input")
        email = st.text_input("Email:", key="email_input")
        search = st.form_submit_button("Pesquisar")
    
    if search:
        try:
            ids = db.encontrar_id(nome, email)
            if ids:
                session_state.idA = ids[0]
                session_state.from_search = True
                session_state.page = "Modificar"
            else:
                session_state.from_search = False
                st.warning("Registro não encontrado.")
        except Exception as e:
            st.warning("Erro durante a pesquisa.")

class AppState:
    def __init__(self):
        self.page = "View all"
        self.idA = None
        self.from_search = False
    
def main():
    st.set_page_config(page_title="Client Products", page_icon="📝")
    
    # Verifica se a instância do AppState já foi criada
    if 'app_state' not in st.session_state:
        st.session_state.app_state = AppState()

    session_state = st.session_state.app_state
    
    page_options = ["View all", "Inserir", "Buscar", "Buscar por nome", "Modificar"]
    selected_page = st.sidebar.selectbox("Navegação", page_options)

    if selected_page == "Modificar" and session_state.from_search == False:
        session_state.page = "Buscar"
        session_state.from_search = True
    elif selected_page == "Modificar" and session_state.from_search:
        session_state.page = "Modificar"
        session_state.from_search = True
    elif selected_page == "Buscar" and session_state.from_search:
        session_state.page = "Modificar"
        session_state.from_search = True
    else:
        session_state.page = selected_page      
        session_state.from_search = False
        
    if session_state.page == "View all":
        view()
    elif session_state.page == "Inserir":
        insert()
    elif session_state.page == "Buscar por nome":
        buscarNome()
    elif session_state.page == "Buscar":
        buscar(session_state)
    elif session_state.page == "Modificar" and session_state.from_search:
        show_modify_form(session_state.idA)
        
if __name__ == "__main__":
    main()

