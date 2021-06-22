import pandas as pd
from surprise import KNNBaseline, Dataset, Reader

from comment.models import Comment
from common.singleton import singleton


@singleton
class Recommendation(object):
    def __init__(self):
        self.comments = Comment.objects.all()
        ratings_dict = self.get_data_from_db()
        df = pd.DataFrame(ratings_dict)

        # A reader is still needed but only the rating_scale param is requiered.
        reader = Reader(rating_scale=(1, 10))

        # The columns must correspond to user id, item id and ratings (in that order).
        self._data = Dataset.load_from_df(df[['userID', 'itemID', 'rating']], reader)

        self._train_set = self._data.build_full_trainset()
        self._sim_options = {'name': 'pearson_baseline', 'user_based': False}
        self._algo = KNNBaseline(sim_options=self._sim_options)
        self._algo.fit(self._train_set)

    @property
    def algo(self):
        return self._algo

    def get_data_from_db(self):
        items = []
        users = []
        rating = []

        for r in self.comments:
            items.append(r.user_id)
            users.append(r.book_id)
            rating.append(r.rating)

        return {
            'itemID': items,
            'userID': users,
            'rating': rating
        }
