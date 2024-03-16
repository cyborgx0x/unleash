import pickle

import pandas as pd
from sqlalchemy import literal
from surprise import SVD, Dataset, Reader

from app import app, db
from app.models import AuthorFollowing, Like


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


def train_recommendation_model(model_type):
    """
    Train theo CF
    Dựa trên like của người dùng
    """
    if model_type == "fiction":
        q = db.session.query(Like.user_id, Like.fiction_id, literal(1).label("like"))
        like = q.all()

        data = pd.DataFrame(like, columns=["user_id", "fiction_id", "like"])

        reader = Reader(rating_scale=(0, 1))
        dataset = Dataset.load_from_df(data[["user_id", "fiction_id", "like"]], reader)
    elif model_type == "author":
        q = db.session.query(
            AuthorFollowing.user_id,
            AuthorFollowing.author_id,
            literal(1).label("follow"),
        )
        follows = q.all()

        data = pd.DataFrame(follows, columns=["user_id", "author_id", "follow"])

        reader = Reader(rating_scale=(0, 1))
        dataset = Dataset.load_from_df(data[["user_id", "author_id", "follow"]], reader)
    algo = SVD()
    trainset = dataset.build_full_trainset()
    algo.fit(trainset)
    return algo

