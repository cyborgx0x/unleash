import pickle
from collections import defaultdict


def load_recommendation_model(model_file="trained_model.pkl"):
    """
    Load the saved model from a file.

    Args:
        model_file (str): The path to the saved model file.

    Returns:
        The loaded model.
    """
    with open(model_file, "rb") as f:
        loaded_model = pickle.load(f)

    return loaded_model


def make_recommendations(model, user_id, num_recommendations=10):
    """
    Make recommendations for a given user.

    Args:
        model: The recommendation model.
        user_id (str): The ID of the user to make recommendations for.
        num_recommendations (int): The number of recommendations to make.

    Returns:
        A list of the top-N recommendations for the user.
    """
    top_n_recommendations = defaultdict(list)

    item_ids = list(model.trainset.all_items())

    for item_id in item_ids:
        predicted_rating = model.predict(user_id, item_id).est
        top_n_recommendations[user_id].append((item_id, predicted_rating))

    top_n_recommendations[user_id].sort(key=lambda x: x[1], reverse=True)

    return top_n_recommendations[user_id][:num_recommendations]
