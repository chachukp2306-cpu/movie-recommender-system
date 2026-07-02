import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster using OMDb API
def fetch_poster(movie_title):
    api_key = "1720430" 
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    try:
        data = requests.get(url).json()
        if data['Response'] == 'True' and 'Poster' in data and data['Poster'] != 'N/A':
            return data['Poster']
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except:
        return "https://via.placeholder.com/500x750?text=Error+Loading+Poster"

# Streamlit UI Configuration
st.set_page_config(page_title="Movie Recommender System", layout="wide")
st.title("Movie Recommendation System")
st.write("A Content-Based Movie Recommendation Engine powering 5000+ movies.")

# Load the production ML model artifacts
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# UI Dropdown Component
selected_movie_name = st.selectbox(
    'Search or select a movie from the database:',
    movies['title'].values
)

# Recommendation Logic Execution
if st.button('Show Recommendations'):
    movie_index = movies[movies['title'] == selected_movie_name].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]
    
    st.write("### Recommended Movies for You:")
    
    # Displaying 5 recommendations in a clean grid layout
    cols = st.columns(5)
    for count, col in enumerate(cols):
        recommended_movie_title = movies.iloc[movies_list[count][0]]['title']
        poster_url = fetch_poster(recommended_movie_title)
        
        with col:
            st.subheader(recommended_movie_title)
            st.image(poster_url, use_container_width=True)
