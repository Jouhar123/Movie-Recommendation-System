import streamlit as st
import pickle
import pandas as pd
import requests

primaryColor="Black"
backgroundColor="Black"

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c705bcf61985bd12cbd8216fb864e40e&language=en-US'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500" +data['poster_path']

def recommend(movie):   
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id    
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommendation system')

selected_movie_name=st.selectbox(
'Hello How may i help you',
movies['title'].values
)

if st.button('Recommend'):
    names,posters=recommend(selected_movie_name)

    col1,col2,col3=st.columns(3)
    with col1: 
        st.header(names[0])
        st.image(posters[0])
    with col2:
        st.header(names[1])
        st.image(posters[1])
    with col3:
        st.header(names[2])
        st.image(posters[2])
