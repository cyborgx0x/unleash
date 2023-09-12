import pickle
import pandas as pd
from surprise import SVD, Dataset, Reader, accuracy
from surprise.model_selection import train_test_split
from sqlalchemy import create_engine


def load_recommendation_model(model_file="trained_model.pkl"):
    # Load the saved model
    with open(model_file, "rb") as f:
        loaded_algo = pickle.load(f)

    return loaded_algo

from collections import defaultdict

def make_recommendations(model, user_id, num_recommendations=10):
    # Create a dictionary to store the top-N recommendations
    top_n_recommendations = defaultdict(list)

    # Get a list of all item IDs in the dataset
    item_ids = list(model.trainset.all_items())

    # Predict ratings for all items and store them in the dictionary
    for item_id in item_ids:
        predicted_rating = model.predict(user_id, item_id).est
        top_n_recommendations[user_id].append((item_id, predicted_rating))

    # Sort the recommendations by predicted rating in descending order
    top_n_recommendations[user_id].sort(key=lambda x: x[1], reverse=True)

    # Get the top-N recommendations for the user
    top_n_recommendations[user_id] = top_n_recommendations[user_id][:num_recommendations]

    return top_n_recommendations[user_id]


if __name__ == "__main__":
    
    # Loading the trained model for inference
    loaded_model = load_recommendation_model()

    user_id = "1"  # Replace with the user you want to recommend items to
    recommendations = make_recommendations(loaded_model, user_id)
    print(recommendations)
