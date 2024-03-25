import streamlit as st
import pandas as pd
import json
import plotly.express as px

with open('geojson.json','r') as file:
    geo = json.loads(file.read())
df = pd.read_csv('petro tratado.csv')
df.dropna(subset='POLO', inplace=True)
df.drop('NÍVEL', axis=1, inplace=True)
col1, col2 = st.columns(2)
with col1:
    st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Logo_petrobras.gif/320px-Logo_petrobras.gif')
with col2:
    st.title('Candidato/Vaga Petrobras 2024')




def create_map(data: pd.DataFrame, color, labels):
    fig = px.choropleth_mapbox(data, geojson=geo, locations='POLO',
                            featureidkey='name',
                            color=color,
                            color_continuous_scale="Viridis",
                            range_color=(0, 12),
                            mapbox_style="carto-positron",
                            zoom=3, center = {"lat": -15.793889, "lon": -47.882778},
                            opacity=0.5,
                            custom_data=labels,

                            )
    fig.update_traces(
    hovertemplate="<br>".join([
        "Polo: %{customdata[0]}",
        "Inscritos: %{customdata[1]}",
        "Vagas: %{customdata[2]}",
        "Demanda: %{customdata[3]}",
    ])
)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, showlegend=True)
    return fig



def filter_area(df, area):
    df = df.loc[df['ÁREA PROFISSIONAL']==area]    
    group = df.drop('ÁREA PROFISSIONAL', axis=1)#.groupby('POLO').sum()
    # for col in (colunas:=group.columns):
    #     if 'DEMANDA' in col:
    #         index = colunas.get_indexer([col])
    #         group[col] = group[colunas[index-2]].values/group[colunas[index-1]].values
    # group = group.reset_index().sort_values('INSCRITOS TOTAL', ascending = False)
    for col in group.columns:
        group[col] = group[col].astype(str)
    return group


with st.sidebar:
    area = st.selectbox('Área Profissional', key='ÁREA PROFISSIONAL', options=df['ÁREA PROFISSIONAL'].unique(), index=1)

    vaga = st.selectbox("Vaga", key='vaga', options=['Total', 'AC', 'PCD', 'PN'], index=0)


group = filter_area(df, area)
st.title(area)
if vaga == 'Total':
    st.write(create_map(group, 'INSCRITOS TOTAL', ['POLO', 'INSCRITOS TOTAL', 'VAGAS TOTAL', 'DEMANDA TOTAL']))
elif vaga == 'AC':
    st.write(create_map(group, 'INSCRITOS AC',  ['POLO', 'INSCRITOS AC', 'VAGAS AC', 'DEMANDA AC']))
elif vaga == 'PCD':
    st.write(create_map(group, 'INSCRITOS PCD',  ['POLO', 'INSCRITOS PCD', 'VAGAS PCD', 'DEMANDA PCD']))
else:
    st.write(create_map(group, 'INSCRITOS PN',  ['POLO', 'INSCRITOS PN', 'VAGAS PN', 'DEMANDA PN']))




