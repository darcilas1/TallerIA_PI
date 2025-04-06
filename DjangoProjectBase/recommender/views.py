import os
import numpy as np
from django.shortcuts import render
from movie.models import Movie
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv('./api_keys.env')
client = OpenAI(api_key=os.environ.get('openai_apikey'))

def get_embedding(text):
    response = client.embeddings.create(input=[text], model="text-embedding-3-small")
    return np.array(response.data[0].embedding, dtype=np.float32)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def recommend_movie(request):
    recommended_movie = None
    similarity_score = None

    if request.method == "POST":
        prompt = request.POST.get("prompt", "")
        prompt_emb = get_embedding(prompt)

        best_similarity = -1

        for movie in Movie.objects.exclude(description__isnull=True).exclude(description=""):
            movie_emb = get_embedding(movie.description)
            similarity = cosine_similarity(prompt_emb, movie_emb)

            if similarity > best_similarity:
                best_similarity = similarity
                recommended_movie = movie
                similarity_score = similarity

        return render(request, "recommender/result.html", {
            "movie": recommended_movie,
            "similarity": round(similarity_score, 4),
            "prompt": prompt
        })

    return render(request, "recommender/form.html")
