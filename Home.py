import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from utils import visualize_type
import altair as alt

url: str = 'https://docs.google.com/spreadsheets/d/1JMutCrRaKG3PsU0fgve98aSjKAP4miARE9hIGAQRSdk/edit?usp=sharing'
conn: GSheetsConnection = st.experimental_connection('job_skills', type=GSheetsConnection)

df: pd.DataFrame = conn.read(spreadsheet=url, worksheet=0)
df = df.drop(840)
df = df.drop_duplicates()

st.header('TOP ANIME IN IMDB')
st.subheader('')
st.write('Didapatkan dari dataset kaggle')
st.dataframe(df)

st.sidebar.header("Anime Filter: ")
Genre = st.sidebar.multiselect(
    "Select the genre: ",
    options=df["Genre"].unique(),
    default=df["Genre"].unique()
)

st.subheader('Top 10 Anime')
st.write('Top 10 anime according to User Rating')

top_10_anime: pd.DataFrame = df[['Title', 'User Rating']].sort_values(by=['User Rating'], ascending=False).head(10)
top_10_anime['User Rating'] = top_10_anime['User Rating'].astype(float)

top_10_anime_chart = (
    alt.Chart(top_10_anime).mark_bar().encode(
        x = alt.X('Title', sort='-y'),
        y = alt.Y('User Rating')
    )
)

st.altair_chart(top_10_anime_chart, use_container_width=True)

st.divider()

st.subheader('Top 10 Genres')
st.write('Top 10 genres with most anime')

top_10_genres: pd.DataFrame = df['Genre'].apply(lambda x: x.replace(' ,', ',').replace(', ', ',').split(','))

Genres: list = []
for i in top_10_genres: Genres += i
Genres: pd.DataFrame = pd.DataFrame(Genres, columns=['Genres']).value_counts().head(10).reset_index()
Genres.columns = ['Genre', 'Count']

genre_chart = (
    alt.Chart(Genres).mark_bar().encode(
        x = alt.X('Count'),
        y = alt.Y('Genre', sort='-x')
    )
)

st.altair_chart(genre_chart, use_container_width=True)

st.divider()

st.subheader('Certificate Spread')
st.write('The spread of give certificates')

certificate_spread: pd.DataFrame = df['Certificate'].value_counts().reset_index()
certificate_spread.columns = ['Certificate', 'Count']

certificate_spread_chart = (
    alt.Chart(certificate_spread).mark_bar().encode(
        x = alt.X('Certificate', sort='-y'),
        y = alt.Y('Count')
    )
)

st.altair_chart(certificate_spread_chart, use_container_width=False)

st.divider()

st.subheader('Biggest Gross Income')
st.write('Anime with the biggest gross income')

gross_income: pd.DataFrame = df[['Title', 'Gross']].dropna()
gross_income['Gross'] = gross_income['Gross'].astype(int)
gross_income = gross_income.sort_values(by=['Gross'], ascending=False).head(10)

gross_income_chart = (
    alt.Chart(gross_income).mark_bar().encode(
        x = alt.X('Gross'),
        y = alt.Y('Title', sort='-x')
    )
)

st.altair_chart(gross_income_chart, use_container_width=True)

st.divider()

st.subheader('Most Present Actors/Actressess')
st.write('Actors/Actressess with most appearance in shows')

top_10_actors: pd.DataFrame = df['Stars'].dropna().apply(lambda x: x.split(','))

Actors:list = []
for i in top_10_actors: Actors += i
Actors:pd.DataFrame = pd.DataFrame(Actors, columns=['Actors']).value_counts().head(10).reset_index()
Actors.columns = ['Actor/Actress', 'Count']

actors_chart = (
    alt.Chart(Actors).mark_bar().encode(
        x = alt.X('Count'),
        y = alt.Y('Actor/Actress', sort='-x')
    )
)

st.altair_chart(actors_chart, use_container_width=True)

st.divider()

st.subheader('Longest Shows')
st.write('Shows with the longest runtime')

show_runtime:pd.DataFrame = df[['Title', 'Runtime']].dropna()
show_runtime['Runtime'] = show_runtime['Runtime'].apply(lambda x: x.split(' ')[0].replace(',', '')).astype(float)
show_runtime = show_runtime.sort_values(by=['Runtime'], ascending=False).head(10)
show_runtime.columns = ['Title', 'Runtime(minutes)']

show_runtime_chart = (
    alt.Chart(show_runtime).mark_bar().encode(
        x = alt.X('Runtime(minutes)'),
        y = alt.Y('Title', sort='-x')
    )
)

st.altair_chart(show_runtime_chart, use_container_width=True)

st.divider()

st.subheader('Runtime Rating Correlation')
st.write('Correlation between runtime and rating')

runtime_rating:pd.DataFrame = df[['Runtime', 'User Rating']].dropna()
runtime_rating['Runtime'] = runtime_rating['Runtime'].apply(lambda x: x.split(' ')[0].replace(',', '')).astype(float)
q_high = runtime_rating['Runtime'].quantile(0.95)
q_low = runtime_rating['Runtime'].quantile(0.05)
runtime_rating = runtime_rating[(runtime_rating['Runtime'] < q_high) & (runtime_rating['Runtime'] > q_low)]
runtime_rating['User Rating'] = runtime_rating['User Rating'].astype(float)
runtime_rating.columns = ['Runtime(minutes)', 'User Rating']

runtime_rating_chart = (
    alt.Chart(runtime_rating).mark_point().encode(
        x = 'Runtime(minutes)',
        y = 'User Rating'
    )
)

st.altair_chart(runtime_rating_chart, use_container_width=True)

st.divider()

st.subheader('Rating Gross Correlation')
st.write('Correlation between rating and gross')

rating_gross:pd.DataFrame = df[['User Rating', 'Gross']].dropna()
rating_gross['Gross'] = rating_gross['Gross'].astype(int)
rating_gross['User Rating'] = rating_gross['User Rating'].astype(float)
q_high = rating_gross['Gross'].quantile(0.95)
q_low = rating_gross['Gross'].quantile(0.05)
rating_gross = rating_gross[(rating_gross['Gross'] < q_high) & (rating_gross['Gross'] > q_low)]

rating_gross_chart = (
    alt.Chart(rating_gross).mark_point().encode(
        x = 'Gross',
        y = 'User Rating'
    )
)

st.altair_chart(rating_gross_chart, use_container_width=True)