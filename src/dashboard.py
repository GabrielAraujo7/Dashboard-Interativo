import streamlit as st
import pandas as pd
from shapely.geometry import Point, Polygon
import plotly.express as px
import plotly.graph_objects as go

# Configura a página para ocupar toda a largura da tela
st.set_page_config(page_title="Análise de Ociosidade", layout="wide")


@st.cache_data
def load_data():
    dfs = [
        'data/relatorio_semanal_V-1001.xlsx',
        'data/relatorio_semanal_V-1002.xlsx',
        'data/relatorio_semanal_V-1003.xlsx',
        'data/relatorio_semanal_V-1004.xlsx',
        'data/relatorio_semanal_V-1005.xlsx'
    ]
    range_dfs = [pd.read_excel(arq) for arq in dfs]
    df_complex = pd.concat(range_dfs, ignore_index=True)

    df_cerca = pd.read_excel('data/coordenadas_cerca.xlsx')

    lista_coordenadas = list(zip(df_cerca['Longitude'], df_cerca['Latitude']))
    cerca_poligono = Polygon(lista_coordenadas)

    def check_points(row):
        ponto = Point(row['Longitude'], row['Latitude'])
        return cerca_poligono.contains(ponto)

    df_complex['dentro_cerca'] = df_complex.apply(check_points, axis=1)
    df_ociosos = df_complex[df_complex['dentro_cerca']]

    return df_complex, df_ociosos, df_cerca


def create_map(df_map, df_cerca, mode='geral', alvo=''):
    if mode == 'geral':
        fig = px.scatter_mapbox(
            df_map,
            lat='Latitude',
            lon='Longitude',
            color='dentro_cerca',
            color_discrete_map={True: 'green', False: 'red'},
            hover_data=['Motorista', 'Veículo', 'Data/Hora', 'dentro_cerca'],
            zoom=13,
            mapbox_style='open-street-map',
            title='Mapa Geral: Todos os Veículos (dentro / fora da cerca)'
        )
    else:
        fig = px.scatter_mapbox(
            df_map,
            lat='Latitude',
            lon='Longitude',
            color=alvo,
            hover_data=['Motorista', 'Veículo', 'Data/Hora'],
            zoom=13,
            mapbox_style='open-street-map',
            title=f'Mapa de Ociosidade ({alvo}) - Dentro da Cerca'
        )

    fig.update_traces(marker=dict(size=8))

    # Adiciona o polígono da cerca
    coord_lons = df_cerca['Longitude'].tolist() + [df_cerca['Longitude'].iloc[0]]
    coord_lats = df_cerca['Latitude'].tolist() + [df_cerca['Latitude'].iloc[0]]

    fig.add_trace(
        go.Scattermapbox(
            lon=coord_lons,
            lat=coord_lats,
            mode='lines',
            fill='toself',
            fillcolor='rgba(0, 150, 255, 0.15)',
            line=dict(color='blue', width=2),
            name='Cerca'
        )
    )

    # centraliza o mapa pela cerca
    center_lon = float(df_cerca['Longitude'].mean())
    center_lat = float(df_cerca['Latitude'].mean())
    fig.update_layout(mapbox_center={'lat': center_lat, 'lon': center_lon}, margin={'r': 0, 't': 30, 'l': 0, 'b': 0})
    return fig


# Carrega os dados processados
try:
    df_complex, df_ociosos, df_cerca = load_data()
except Exception as e:
    st.error(f"Erro ao ler dados: {e}")
    st.stop()


st.sidebar.title("Navegação")
st.sidebar.markdown("Escolha o painel de visualização:")
menu = st.sidebar.radio("", ["Visão Motoristas", "Visão Veículos", "Visão Geral"])

if menu == "Visão Motoristas":
    st.title("Dashboard: Ociosidade por Motorista")
    target_key = 'Motorista'
    cor = 'Reds'
    df_use = df_ociosos.copy()
    modo = 'motorista'
elif menu == "Visão Veículos":
    st.title("Dashboard: Ociosidade por Caminhão")
    target_key = 'Veículo'
    cor = 'Oranges'
    df_use = df_ociosos.copy()
    modo = 'veiculo'
else:
    st.title("Dashboard: Visão Geral de Todos os Veículos")
    target_key = None
    cor = 'Viridis'
    df_use = df_complex.copy()
    modo = 'geral'

# Preparação temporal
coluna_tempo = 'Data/Hora'
if coluna_tempo not in df_use.columns:
    st.error(f"Coluna '{coluna_tempo}' não encontrada no dataframe")
    st.stop()

# Evitar warnings
df_use = df_use.copy()
df_use[coluna_tempo] = pd.to_datetime(df_use[coluna_tempo], errors='coerce')
df_use['Data_Apenas'] = df_use[coluna_tempo].dt.date
df_use['Hora_Apenas'] = df_use[coluna_tempo].dt.hour

dias_pt = {0: 'Segunda', 1: 'Terça', 2: 'Quarta', 3: 'Quinta', 4: 'Sexta', 5: 'Sábado', 6: 'Domingo'}
df_use['Dia_Semana'] = df_use[coluna_tempo].dt.dayofweek.map(dias_pt)

st.markdown('---')

if modo in ('motorista', 'veiculo'):
    df_agrupado = df_use.groupby(target_key).size().reset_index(name='registros_na_cerca')
    df_agrupado = df_agrupado.sort_values(by='registros_na_cerca', ascending=False)

    total_ocioso = int(df_agrupado['registros_na_cerca'].sum())
    maior_ofensor = df_agrupado.iloc[0][target_key] if not df_agrupado.empty else 'N/A'
    max_registros = int(df_agrupado.iloc[0]['registros_na_cerca']) if not df_agrupado.empty else 0

    col_kpi1, col_kpi2 = st.columns(2)
    col_kpi1.metric("Total de Registros na Cerca", total_ocioso)
    col_kpi2.metric(f"Maior Ofensor ({target_key})", f"{maior_ofensor}", f"{max_registros} registros", delta_color="inverse")

    st.subheader("Visão Geral")
    col1, col2 = st.columns(2)

    with col1:
        fig_bar = px.bar(df_agrupado, x=target_key, y='registros_na_cerca',
                         title=f'Ranking de Ociosidade ({target_key})',
                         text='registros_na_cerca', color='registros_na_cerca', color_continuous_scale=cor)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        fig_pie = px.pie(df_agrupado, values='registros_na_cerca', names=target_key,
                         title=f'Distribuição de Ociosidade ({target_key})', hole=0.3)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown('---')
    st.subheader('Análise Temporal das Paradas')
    col3, col4 = st.columns(2)

    with col3:
        df_linha = df_use.groupby(['Data_Apenas', target_key]).size().reset_index(name='registros_na_cerca')
        fig_linha = px.line(df_linha, x='Data_Apenas', y='registros_na_cerca', color=target_key, markers=True,
                            title='Evolução da Ociosidade por Dia',
                            labels={'Data_Apenas': 'Data', 'registros_na_cerca': 'Qtd. de Registros'})
        st.plotly_chart(fig_linha, use_container_width=True)

    with col4:
        df_hora = df_use.groupby(['Hora_Apenas', target_key]).size().reset_index(name='registros')
        fig_hora = px.line(df_hora, x='Hora_Apenas', y='registros', color=target_key, markers=True,
                           title='Picos de Ociosidade por Hora do Dia',
                           labels={'Hora_Apenas': 'Hora do Dia (0-23h)', 'registros': 'Qtd. de Registros'})
        fig_hora.update_xaxes(dtick=1)
        st.plotly_chart(fig_hora, use_container_width=True)

    st.markdown('---')
    st.subheader('Mapa de Concentração (Dentro da Cerca)')
    fig_map = create_map(df_use, df_cerca, mode='especifico', alvo=target_key)
    st.plotly_chart(fig_map, use_container_width=True)

else:
    total_geral = len(df_use)
    total_dentro = int(df_use['dentro_cerca'].sum())
    total_fora = total_geral - total_dentro

    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    col_kpi1.metric('Total de Registros', total_geral)
    col_kpi2.metric('Dentro da Cerca', total_dentro, delta=f'+{total_dentro}')
    col_kpi3.metric('Fora da Cerca', total_fora, delta=f'+{total_fora}', delta_color='inverse')

    st.subheader('Distribuição Geral')
    df_status = df_use.groupby('dentro_cerca').size().reset_index(name='registros')
    fig_status = px.pie(df_status, values='registros', names='dentro_cerca',
                        title='Percentual Dentro x Fora da Cerca', hole=0.35,
                        color='dentro_cerca', color_discrete_map={True: 'green', False: 'red'})
    st.plotly_chart(fig_status, use_container_width=True)

    st.markdown('---')
    st.subheader('Análise Temporal Geral')
    col3, col4 = st.columns(2)

    with col3:
        df_linha = df_use.groupby(['Data_Apenas']).size().reset_index(name='registros')
        fig_linha = px.line(df_linha, x='Data_Apenas', y='registros', markers=True,
                            title='Evolução de Registros por Dia',
                            labels={'Data_Apenas': 'Data', 'registros': 'Qtd. de Registros'})
        st.plotly_chart(fig_linha, use_container_width=True)

    with col4:
        df_hora = df_use.groupby(['Hora_Apenas']).size().reset_index(name='registros')
        fig_hora = px.line(df_hora, x='Hora_Apenas', y='registros', markers=True,
                           title='Registros por Hora do Dia',
                           labels={'Hora_Apenas': 'Hora do Dia (0-23h)', 'registros': 'Qtd. de Registros'})
        fig_hora.update_xaxes(dtick=1)
        st.plotly_chart(fig_hora, use_container_width=True)

    st.markdown('---')
    st.subheader('Mapa de Concentração (Geral)')
    fig_map = create_map(df_use, df_cerca, mode='geral')
    st.plotly_chart(fig_map, use_container_width=True)
