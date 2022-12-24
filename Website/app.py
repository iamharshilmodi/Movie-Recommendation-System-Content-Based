import streamlit as st
import pickle
import requests
import base64


st.set_page_config(layout="wide")

hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''

st.markdown(hide_img_fs, unsafe_allow_html=True)

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('bg7.jpg')

movies = pickle.load(open('movies.pkl', 'rb'))
movie_list = movies['title'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie = st.selectbox(
    'Type or select a movie from the drop down menu',
    movie_list)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x:x[1])[1:6]

    recommended_name = []
    recommended_poster = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_name.append(movies.iloc[i[0]].title)
        recommended_poster.append(fetch_poster(movie_id))

    return recommended_name, recommended_poster


if st.button('Recommend'):
    recommended_name,recommended_poster  = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_name[0])
        st.image(recommended_poster[0])
    with col2:
        st.text(recommended_name[1])
        st.image(recommended_poster[1])
    with col3:
        st.text(recommended_name[2])
        st.image(recommended_poster[2])
    with col4:
        st.text(recommended_name[3])
        st.image(recommended_poster[3])
    with col5:
        st.text(recommended_name[4])
        st.image(recommended_poster[4])