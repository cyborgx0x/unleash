from celery import shared_task

from app.trainer import *
from app import app

@shared_task
def crawl_truyenfull():
    print("crawl truyen full")


@shared_task
def train_recommendation():
    with app.app_context():
        author_model = train_recommendation_model(model_type="author")
        fiction_model = train_recommendation_model(model_type="fiction")
        with open("models/cf_fiction.pickle", "wb") as f:
            pickle.dump(fiction_model, f)
        with open("models/cf_author.pickle", "wb") as f:
            pickle.dump(author_model, f)
        print("Model trained and saved successfully.")

        return "Train Complete"
