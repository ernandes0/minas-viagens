import streamlit as st
import pandas as pd
import numpy as np
from utils.data import Data
import plotly.graph_objects as go

st.set_page_config(layout="wide")

class HomePage:
    def __init__(self):
        self.data_join_diaria_orgao = Data().get_data_join_diaria_orgao()
        self.data_diaria = Data().get_data_diaria()
      
    def set_filters(self):
        st.sidebar.header('Filtros')
        self.date_filter()

    def date_filter(self):
        df = self.data_join_diaria_orgao
        # Cria um seletor de datas inicial e final
        data_inicial = '2012-01-09'
        data_final = '2022-11-24'

        data_inicial = pd.to_datetime(data_inicial)
        data_final = pd.to_datetime(data_final)
        delta = data_final - data_inicial
        num_dias = delta.days + 1

        # Converte as datas selecionadas para strings no formato yyyy-mm-dd
        data_inicial_str = data_inicial.strftime('%Y-%m-%d')
        data_final_str = data_final.strftime('%Y-%m-%d')

        # Cria um slider para selecionar o número de registros a serem exibidos
        num_registros = st.sidebar.slider('Intervalo de dias', 1, num_dias, num_dias, key='slider')

        # Atualiza as datas inicial e final de acordo com o intervalo selecionado
        data_final_selecionada = data_final
        data_inicial_selecionada = data_final - pd.Timedelta(days=num_registros-1)
        data_inicial_str = data_inicial_selecionada.strftime('%Y-%m-%d')
        data_final_str = data_final_selecionada.strftime('%Y-%m-%d')
        st.sidebar.write(f'Intervalo selecionado referente a data :    {data_inicial_str} a {data_final_str}')

        # Filtra a base de dados pelos valores selecionados
        self.data_join_diaria_orgao = df.loc[df['dt_inicio_trecho'].between(data_inicial_str, data_final_str)]

    def exploratory(self):
        st.subheader('Informações Pertinentes')
        maior_valor = self.data_join_diaria_orgao['vr_diaria'].max()
        #Separa o espaço do Streamlit em colunas
        row5_spacer1, row5_1, row5_spacer2, row5_2, row5_spacer3= st.columns((.2, 2.3, .4, 4.4, .2))
        with row5_1:
            st.write('No geral, a base trabalhada apresenta registros \n\n referentes a 10 anos.')
            st.write('')
            st.write('')
            st.write(f'\n\n\nDurante o período de tempo determinado o maior valor de uma diária foi de: {maior_valor}.')
        with row5_2:
            df2 = self.data_diaria.agg(Minimum_Date=('dt_inicio_trecho', np.min), Maximum_Date=('dt_inicio_trecho', np.max))
            df2.rename(columns = {'dt_inicio_trecho':'Data geral'}, inplace = True)
            st.write(df2)

    def raw_data_table(self):
        st.subheader('Quais órgãos mais enviam funcionários em viagens? e quais são os destinos mais comuns?')
        row5_spacer1, row5_1, row5_spacer2, row5_2, row5_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
        with row5_1:
            st.markdown('Investigando a quantidade de viagens envolvendo os órgãos, percebemos uma dicrepância entre algumas instituições. De cara, é perceptível que o órgão que mais enviou viajantes foi a secretaria de justiça e segurança pública, com 333 mil viagens somadas. (para melhor visualização, ampliar gráfico)')
        with row5_2:
            df = self.data_join_diaria_orgao.groupby('nome_orgao',  as_index=False)['nome'].count().rename(columns={'count':'nome_orgao', 'nome':'quantidade'})
            fig = go.Figure([go.Bar(x = df['nome_orgao'], y= df['quantidade'])])
            st.plotly_chart(fig, use_container_width=True)
    
    def visita_estado(self):
        st.subheader('Destinos mais comuns:')
        row5_spacer1, row5_1, row5_spacer2, row5_2, row5_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
        with row5_2:
            st.markdown('Entre todos os 76 órgãos, foram realizadas mais de um milhão de viagens, com isso, é possível observar os destinos mais comuns. Como esperado, a maior parte de todas as viagens são realizadas entre os municípios do próprio estado de Minas, Com São Paulo ficando em segundo. Todas as viagens internacionais somam apenas 515.')
        with row5_1:
            df2 = self.data_join_diaria_orgao['nome'].value_counts(dropna=False)
            df_value_counts = pd.DataFrame(df2)
            df_value_counts = df_value_counts.reset_index()
            df_value_counts.columns = ['destinos', 'quantidade']
            df_value_counts
            st.write(df_value_counts.head(200))

    def gasto_ano(self):
        st.subheader('qual a média de gasto separados por ano?')
        row5_spacer1, row5_1, row5_spacer2, row5_2, row5_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
        with row5_2:
            st.markdown('É possível notar algumas inconsistências relacionadas aos gastos anuais, onde no ano de 2013, não foi registrado nenhum gasto relacionado a diárias. No entanto, a partir do ano de 2016, parece haver uma maior adesão aos cadastros.')
        with row5_1:
            df_por_ano = self.data_diaria.groupby('ano_particao', as_index = False)["vr_diaria"].sum().rename(columns={'ano_particao':'ano', 'vr_diaria':'valor_total'})
            st.write(df_por_ano)
        with row5_2:
            fig = go.Figure([go.Bar(x = df_por_ano['ano'], y= df_por_ano['valor_total'])])
            st.plotly_chart(fig, use_container_width=True)

home = HomePage()
home.set_filters()
home.exploratory()
home.raw_data_table()
home.visita_estado()
home.gasto_ano()