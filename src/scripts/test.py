import streamlit as st
import unidecode
import os
import datetime as dt
import pontoBD as p

add_selectbox = st.sidebar.container()

add_selectbox.markdown("""
    # <center>Marcação de Ponto</center><br>
""", unsafe_allow_html = True)

options = ['Marcar Ponto Diário', 'Inserir Ponto', 'Comprovante',  'Relatórios']
result_bar = add_selectbox.radio('Escolha a opção', options)


if result_bar == options[0]:
    st.title(options[0])
    st.markdown(f'<b>Clique Abaixo para marcar o ponto Diário</b><br>', unsafe_allow_html = True)
    marca = st.button('Marcar Ponto')
    if marca:
        manneger = p.PontoBD()
        retorno = manneger.ponto()
        manneger.horas()
        if retorno == -1:
            st.warning('Ponto já inserido')
        else:
            st.success('Ponto Marcado com sucesso!!!')

elif result_bar == options[1]:
    st.title(options[1])
    data = st.date_input('Digite a data de marcação')
    hora = st.text_input('Digite a hora', max_chars=5, placeholder='HH:MM')
    tipo = st.radio('', ['Entrada', 'Saída'])

    inserir = st.button('Inserir Ponto')
    if inserir:
        st.text('Dados inseridos:')
        st.text(str(data))
        st.text(hora)
        st.text(unidecode.unidecode(tipo).lower())
        manneger = p.PontoBD()
        ret = manneger.inserPonto(str(data), hora, unidecode.unidecode(tipo).lower())
        manneger.horas()
        if ret == -1:
            st.warning('Ponto já inserido')
        else:
            st.success('Ponto Marcado com sucesso!!!')

elif result_bar == options[-1]:
    st.title(options[-1])
    query = 'select * from time_worked order by data'
    manneger = p.PontoBD()
    result = manneger.getQuery(query)
    st.table(result)

elif result_bar == options[2]:
    st.title(options[2])
    data_comp = dt.date.today()
    select = f"""
    select data, hora, tipo from ponto
    where data = '{data_comp}'
    """
    manneger = p.PontoBD()
    dados = manneger.getQuery(select)
    st.table(dados)