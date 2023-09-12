
from sqlalchemy import create_engine
from surprise import SVD, Dataset, Reader, accuracy
import pandas as pd
import pickle
from surprise.model_selection import train_test_split


def train_recommendation_model(database_url, table_name, model_file="trained_model.pkl"):
    # Create a SQLAlchemy database connection
    engine = create_engine(database_url)
    
    # Query the data from the database
    query = f"SELECT user_id, item_id, rating FROM {table_name}"
    df = pd.read_sql(query, engine)

    # Define the rating scale
    reader = Reader(rating_scale=(1, 5))

    # Create a Dataset object
    data = Dataset.load_from_df(df[['user_id', 'item_id', 'rating']], reader)

    # Split the dataset
    trainset, _ = train_test_split(data, test_size=0.2)  # Use 100% of the data for training

    # Choose an algorithm
    algo = SVD()

    # Train the model
    algo.fit(trainset)

    # Save the trained model
    with open(model_file, "wb") as f:
        pickle.dump(algo, f)

    print("Model trained and saved successfully.")

train_recommendation_model("sqlite:///sample.db", "ratings", "trained_model.pkl")