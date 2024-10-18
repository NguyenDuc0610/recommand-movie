from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)


# Định nghĩa hàm recommend
def recommend(movie):
    matching_movies = movies[movies['title'].str.contains(movie, case=False)]

    if not matching_movies.empty:
        recommended_movies = matching_movies['title'][:20].tolist()
        return recommended_movies
    else:
        # Xử lý trường hợp không tìm thấy phim
        return ["Không tìm thấy phim"]


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)


@app.route('/')
def home():
    movie_options = movies['title'].values
    return render_template('index.html', movie_options=movie_options)


@app.route('/recommend', methods=['POST'])
def get_recommendations():
    selected_movie = request.form['selected_movie']
    recommendations = recommend(selected_movie)
    return render_template('recommendations.html', recommendations=recommendations)


if __name__ == '__main__':
    app.run(debug=True)
