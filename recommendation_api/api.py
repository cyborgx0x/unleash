from typing import List

from fastapi import FastAPI
from loader import load_recommendation_model, make_recommendations

app = FastAPI()

author_recommendation_model = load_recommendation_model(model_file="models/cf_author.pickle")
fiction_recommendation_model = load_recommendation_model(model_file="models/cf_fiction.pickle")


@app.get("/fiction-recommendations/{user_id}", response_model=List[int])
def get_fiction_recommendation(user_id: int):
    recommendations = make_recommendations(fiction_recommendation_model, user_id)
    id_list = [item[0] for item in recommendations]
    return id_list


@app.get("/author-recommendations/{user_id}", response_model=List[int])
def get_author_recommendations(user_id: int):
    recommendations = make_recommendations(author_recommendation_model, user_id)
    id_list = [item[0] for item in recommendations]
    return id_list
