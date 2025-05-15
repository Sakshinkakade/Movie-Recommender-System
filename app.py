import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_title):
    # Replace 'your_api_key' with your OMDb API key
    api_key = '99de9e6'
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if data['Response'] == 'True' and 'Poster' in data:
        return data['Poster']
    else:
        return None  # Return None if no poster is found or an error occurs


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = i[0]

        # Fetch movie title and poster
        movie_title = movies.iloc[i[0]].title
        poster_url = fetch_poster(movie_title)

        recommended_movies.append(movie_title)
        recommended_posters.append(poster_url)

    return recommended_movies, recommended_posters


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Select a movie:",
    movies['title'].values)

if st.button("Recommend"):
    recommendations, posters = recommend(selected_movie_name)

    # Create aligned layout for posters and titles
    cols = st.columns(len(recommendations))  # Create columns for alignment
    for col, movie, poster in zip(cols, recommendations, posters):
        with col:
            if poster:
                st.image(poster, use_container_width=True)  # Display poster
            else:
                st.image("https://via.placeholder.com/150", use_column_width=True)  # Fallback for missing posters
            st.write(f"**{movie}**")  # Movie title below poster
