from flask import Flask, jsonify, request
from pymongo import MongoClient
import pandas as pd
import numpy as np
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

mongo_url = "mongodb+srv://aftab:aftab35520@cluster0.zja2qb6.mongodb.net/MovieCollection?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_url)
db = client['MovieCollection']
collection = db['MovieCollection']


def SimilarMovie(MovieName):
    data = list(collection.find({}, {"_id": 0}))
    df = pd.DataFrame(data)
    df['name'] = df['name'].astype(str).fillna('')
    df['genre'] = df['genre'].astype(str).fillna('')
    df['description'] = df['description'].astype(str).fillna('')
    dfCol = df['name'] + ' ' + df["genre"] + ' ' + df['description']

    dfCol.dropna(inplace=True)
    Tf=TfidfVectorizer(stop_words="english")
    Vector=Tf.fit_transform(dfCol)
    Similarty=cosine_similarity(Vector)
    moviesList=df["name"].tolist()
    similar_movies = difflib.get_close_matches(MovieName, moviesList, n=1, cutoff=0.4) 
    if similar_movies:
        similarMovie = similar_movies[0] 
        print(f"Similar movie: {similarMovie}") 
    else:
        print(f"No similar movies found for '{MovieName}'")

    indexOfSimilarMovie=df[df.name==similarMovie].index.values[0]  
    similarity_score = list(enumerate(Similarty[indexOfSimilarMovie]))  
    similartyScore=list(enumerate(Similarty[indexOfSimilarMovie]))
    SortSimilartyScore=sorted(similartyScore,key=lambda x:x[1],reverse=True)
    similarity_score = list(enumerate(Similarty[indexOfSimilarMovie]))
    similartyScore=list(enumerate(Similarty[indexOfSimilarMovie]))
    SortSimilartyScore=sorted(similartyScore,key=lambda x:x[1],reverse=True)
    data=[]
    for i in range(0,8):
      index=SortSimilartyScore[i][0]
      title_from_index = df[df.index==index]['name'].values[0]
      link = df[df.index==index]['link'].values[0]
      language = df[df.index==index]['language'].values[0]
      poster = df[df.index==index]['poster'].values[0]
      description = df[df.index==index]['description'].values[0]
      releaseDate = df[df.index==index]['releaseDate'].values[0]
      imdbRating = df[df.index==index]['imdbRating'].values[0]
      data.append({'name':title_from_index,'link':link,'language':language,'poster':poster,'description':description,'releaseDate':releaseDate,'imdbRating':imdbRating})
    return data