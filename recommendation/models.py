import pandas as pd
from comment.models import Comment
from common.singleton import singleton


@singleton
class Recommendation(object):
    def __init__(self):
        self.comments = Comment.objects.all()
