from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS
import Model
import searchMovie
app = Flask(__name__)
CORS(app)

mongo_url = "mongodb+srv://aftab:aftab35520@cluster0.zja2qb6.mongodb.net/MovieCollection?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_url)
db = client['MovieCollection']
collection = db['MovieCollection']
try:
    db.command('ping')
    print("MongoDB connected successfully!")
except Exception as e:
    print("Error connecting to MongoDB:", e)

@app.route('/movies/<int:number>', methods=['GET'])
def get_movies(number):
    try:
        limit = 30
        skip = (number - 1) * limit
        movies = list(collection.find({}, {"_id": 0}).skip(skip).limit(limit))

        if not movies:
            return jsonify({"message": "No movies found"}), 404
        return jsonify(movies)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/SimilarMovie/<MovieName>",methods=["GET"])
def SimilarMovies(MovieName):
    return jsonify (Model.SimilarMovie(MovieName))

@app.route("/latestmovies", methods=["GET"])
def latest_movies():
    try:
        latest_movies = list(collection.find({}, {"_id": 0}).sort("releaseDate", -1).limit(18))
        if not latest_movies:
            return jsonify({"message": "No latest movies found"}), 404
        return jsonify(latest_movies)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/search/<name>",methods=['GET'])
def SearchMovieQuiry(name):
    return jsonify(searchMovie.SimilarMovie(name))

if __name__ == '__main__':
    app.run(debug=True)
