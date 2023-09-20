from app import db
from app.models import Like
from sqlalchemy import literal
import pandas as pd

def get_recommendations(user_id, algo):
    """
    Get recommendations for a specific user
    """
    q = db.session.query(Like.user_id, Like.fiction_id, literal(1).label("like"))
    like = q.all()

    data = pd.DataFrame(like, columns=["user_id", "fiction_id", "like"])

    # Create a list of all fiction IDs
    fiction_ids = list(set(data["fiction_id"]))

    # Create a list of tuples containing the user ID and each fiction ID
    user_fiction = [(user_id, fiction_id) for fiction_id in fiction_ids]

    # Predict the ratings for the user and each fiction
    predictions = algo.test(user_fiction)

    # Sort the predictions by the predicted rating in descending order
    sorted_predictions = sorted(predictions, key=lambda x: x.est, reverse=True)

    # Get the top 10 fiction IDs from the sorted predictions
    top_10_fiction_ids = [prediction.iid for prediction in sorted_predictions[:10]]

    return top_10_fiction_ids
