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
        movie_id=movies.iloc[i[0]].id
        rec_mov.append(movies.iloc[movie_id].title)

    return rec_mov


#User Interface
st.title("Movie Recommender System")

movie_name=st.selectbox("Select Movie",movies['title'].values)

if st.button("Recommend"):
    rec,pos=recommend(movie_name)

    st.subheader("Top 5 Movies based on {}".format(movie_name))
    
    col1,col2,col3,col4,col5=st.columns(2)

    with col1:
        st.text(rec[0])
    with col2:
        st.text(rec[1])
    with col3:
        st.text(rec[2])
    with col4:
        st.text(rec[3])
    with col5:
        st.text(rec[4])