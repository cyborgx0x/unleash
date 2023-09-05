# Import necessary modules
import pickle

import pandas as pd
from surprise import SVD, Dataset, Reader, accuracy
from surprise.model_selection import train_test_split

# # Load your dataset (replace 'your_data.csv' with your actual file)
# ratings_data = pd.read_csv('your_data.csv')

# # Create a Dataset object
# reader = Reader(rating_scale=(1, 5))
# data = Dataset.load_from_df(ratings_data[['user_id', 'item_id', 'rating']], reader)

data = Dataset.load_builtin("ml-100k")


# Split the dataset
trainset, testset = train_test_split(data, test_size=0.2)

# Choose an algorithm
algo = SVD()

# Train the model
algo.fit(trainset)

# Save the trained model
with open("trained_model.pkl", "wb") as f:
    pickle.dump(algo, f)

# Load the saved model
with open("trained_model.pkl", "rb") as f:
    loaded_algo = pickle.load(f)

# Make predictions
predictions = algo.test(testset)

# Evaluate the model
rmse = accuracy.rmse(predictions)
print(f"RMSE: {rmse}")
