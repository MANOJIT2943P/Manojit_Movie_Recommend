import requests
import streamlit as st
import pandas as pd
import pickle
import gzip

#prepare and load data
movies=pickle.load(open('movies.pkl','rb'))
movies=pd.DataFrame(movies)

with gzip.open('similarity.pkl.gz','rb') as f:
    similarity=pickle.load(f)

#function to fetch poster
def fetch_poster(movie_id):
     url = "https://api.themoviedb.org/3/movie/{}?api_key=fe6aacca86b69ab259c31a74a20127b6&language=en-US".format(movie_id)
     data=requests.get(url)
     data=data.json()
     poster_path = data['poster_path']
     full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
     return full_path

#function to recommend movies
def recommend(mov):
    mov_index= movies[movies['title']==mov].index[0]
    dis=similarity[mov_index]
    movie_list=sorted(list(enumerate(dis)),reverse=True,key=lambda x: x[1])[1:6]

    rec_mov=[]
    rec_mov_poster=[]
    for i in movie_list:
        movie_id=movies.iloc[i[0]].id
        rec_mov.append(movies.iloc[movie_id].title)
        rec_mov_poster.append(fetch_poster(movie_id))

    return rec_mov,rec_mov_poster


#User Interface
st.title("Movie Recommender System")

movie_name=st.selectbox("Select Movie",movies['title'].values)

if st.button("Recommend"):
    rec,pos=recommend(movie_name)

    st.subheader("Top 5 Movies based on {}".format(movie_name))
    
    col1,col2,col3,col4,col5=st.columns(2)

    with col1:
        st.text(rec[0])
        st.image(pos[0])
    with col2:
        st.text(rec[1])
        st.image(pos[1])
    with col3:
        st.text(rec[2])
        st.image(pos[2])
    with col4:
        st.text(rec[3])
        st.image(pos[3])
    with col5:
        st.text(rec[4])
        st.image(pos[4])