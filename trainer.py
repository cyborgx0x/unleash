import pickle

import pandas as pd
from sqlalchemy import literal
from surprise import SVD, Dataset, Reader

from app import app, db
from app.models import Like


class Trainer:
    """
    ## Abstract

    Cung cấp phương thức làm việc khi train model gợi ý fiction phù hợp với người dùng

    # Phương pháp

    - Gợi ý dựa trên ACF
    - Gợi ý dựa trên Content Based

    Chuẩn bị:
    - Dataset
    """

    data = ...

    def train(self):
        ...


def content_based_recommendation():
    """
    ## Train mô hình gợi ý dựa trên nội dung của truyện


    Các đặc trưng bao gồm có:
    - tag
    - short desc
    - desc

    Dữ liệu được chuẩn bị:

    """


def collaborative_filtering_recommendation():
    """
    ## Train mô hình dựa theo CF

    Đặc trưng:
    - Rating của người dùng với truyện
    - Like của người dùng
    """


def train_recommendation_model():
    """
    Train theo CF
    Dựa trên like của người dùng
    """
    q = db.session.query(Like.user_id, Like.fiction_id, literal(1).label("like"))
    like = q.all()

    data = pd.DataFrame(like, columns=["user_id", "fiction_id", "like"])

    reader = Reader(rating_scale=(0, 1))
    dataset = Dataset.load_from_df(data[["user_id", "fiction_id", "like"]], reader)
    algo = SVD()
    trainset = dataset.build_full_trainset()
    algo.fit(trainset)
    return algo


with app.app_context():
    model = train_recommendation_model()
    with open("cf_fiction.pickle", "wb") as f:
        pickle.dump(model, f)

    print("Model trained and saved successfully.")
