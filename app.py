import streamlit as st
import pickle
import difflib
import pandas as pd
import numpy as np
import difflib
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer 
st.title("Movie suggestion page By K.Rohit Kumar")
mov_list=pickle.load(open('movies.pkl','rb'))
all_mov_list=mov_list['title'].values
def suggest_movies(title):
     netflix=pd.read_csv('movies.csv')
     features=['genres','keywords','tagline','cast','director','overview']
     for i in features:
         netflix[i]=netflix[i].fillna('')
     all_features=netflix['cast']+' '+netflix['genres']+' '+' '+netflix['keywords']+' '+netflix['tagline']+netflix['director']+netflix['overview']

     vect=TfidfVectorizer()
     feature_vector=vect.fit_transform(all_features)
     similarity = cosine_similarity(feature_vector)
     all_titles = mov_list['title'].tolist()
     movie = title
     all_close_match = difflib.get_close_matches(movie, all_titles)
     close_match = all_close_match[0]
     index = mov_list[mov_list.title == close_match]['index'].values[0]
     similarity_score = list(enumerate(similarity[index]))
     sorted_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)
     count = 1
     suggestions=[]
     for i in sorted_movies:
          index = i[0]
          title_from_data = mov_list[mov_list.index == index]['title'].values[0]
          if count <= 5:
               suggestions.append(title_from_data)
               count += 1
     return suggestions


user_title = st.selectbox(
     'Hey there! please enter the title of your favorite movie : ',
     all_mov_list)

st.write('You selected:', user_title)
if st.button('Suggest'):
     for i in suggest_movies(user_title):
          st.write(i)
