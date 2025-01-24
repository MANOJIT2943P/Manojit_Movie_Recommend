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



#function to recommend movies
def recommend(mov):
    mov_index= movies[movies['title']==mov].index[0]
    dis=similarity[mov_index]
    movie_list=sorted(list(enumerate(dis)),reverse=True,key=lambda x: x[1])[1:6]

    rec_mov=[]
    for i in movie_list:
        rec_mov.append(movies.iloc[i[0]].title)

    return rec_mov


#User Interface
st.title("Movie Recommender System")

movie_name=st.selectbox("Select Movie",movies['title'].values)

if st.button("Recommend"):
    rec=recommend(movie_name)

    st.subheader('Top 5 Movies based on "{}" '.format(movie_name))

    base_url="https://www.google.com/search?q={} movie"

    

    for movie in rec:
        col1,col2=st.columns([0.8, 0.2])
        with col1:
            st.text(movie)
        with col2:
            st.link_button("Know More",base_url.format(movie))