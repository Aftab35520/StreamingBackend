from flask import Flask, jsonify, request
from pymongo import MongoClient
import pandas as pd
from thefuzz import process
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


mongo_url = "mongodb+srv://aftab:aftab35520@cluster0.zja2qb6.mongodb.net/MovieCollection?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_url)
db = client['MovieCollection']
collection = db['MovieCollection']
def SimilarMovie(MovieName):
    data = list(collection.find({}, {"_id": 0}))
    df = pd.DataFrame(data)

    if df.empty:
        return jsonify({"message": "No movies in the database"}), 404

    df["name"] = df["name"].astype(str).fillna('')
    df["genre"] = df["genre"].astype(str).fillna('')
    df["description"] = df["description"].astype(str).fillna('')

    dfCol = df["name"] + " " + df["genre"] + " " + df["description"]
    Tf = TfidfVectorizer(stop_words="english")
    Vector = Tf.fit_transform(dfCol)
    Similarty = cosine_similarity(Vector)
    moviesList = df["name"].tolist()
    closest_match = process.extractOne(MovieName, moviesList, score_cutoff=60)
    if not closest_match:
        return jsonify({"message": f"No similar movies found for '{MovieName}'"}), 404
    similarMovie = closest_match[0]
    indexOfSimilarMovie = df[df.name == similarMovie].index.values[0]
    similarity_score = list(enumerate(Similarty[indexOfSimilarMovie]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    results = []
    for i in range(min(8, len(sorted_similar_movies))):
        index = sorted_similar_movies[i][0]
        movie_data = df.iloc[index].to_dict()
        results.append(movie_data)
    return results

