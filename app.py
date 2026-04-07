from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import requests

app = Flask(__name__)
CORS(app)

# 1. Load the data you saved from your notebook
# Make sure these files are in the same folder as app.py
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=e2912b398842c8f833b28cf8b2ec0297&language=en-US"
    try:
        response = requests.get(url)
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        return "https://via.placeholder.com/500x750?text=No+Poster"
    except:
        return "https://via.placeholder.com/500x750?text=Error"

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    movie_user_likes = data.get('movie')
    
    try:
        # Recommendation Logic
        movie_index = movies[movies['title'].str.lower() == movie_user_likes.lower()].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]
        
        recommended_movies = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append({
                "title": movies.iloc[i[0]].title,
                "poster": fetch_poster(movie_id)
            })
            
        return jsonify({"success": True, "movies": recommended_movies})
    except Exception as e:
        return jsonify({"success": False, "message": "Movie not found or server error."})

if __name__ == "__main__":
    app.run(debug=True, port=5000)