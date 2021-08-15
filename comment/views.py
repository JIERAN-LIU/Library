import random
import string

from django.contrib.auth.hashers import make_password
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Book
from comment.models import CommentSummary, Comment
from comment.serializers import CommentSerializer
from common.constant import Constant
from common.models import College, User
from common.views import BaseModelViewSet, get_random_password


class CommentViewSet(BaseModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        user = self.fill_user(serializer, 'create')
        user['user_id'] = serializer.context['request'].user.id
        serializer.save(**user)
        self.update_summary(serializer)

    @staticmethod
    def update_summary(serializer):
        data = serializer.validated_data
        book_id = data['book'].id
        rating = data['rating']

        summaries = CommentSummary.objects.filter(book_id=book_id)
        if len(summaries):
            summary = summaries[0]
            rating_number = summary.rating_number + 1
            summary.rating = round(((summary.rating * summary.rating_number + rating) / rating_number), 2)
            summary.rating_number = rating_number
        else:
            summary = CommentSummary(book_id=book_id, rating=rating, rating_number=1)
        summary.save()


class CommentGenerate(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        from faker import Faker
        fake: Faker = Faker()
        readers = []
        college_list = [c.id for c in list(College.objects.all())]
        username_dict = {u.username: u.username for u in list(User.objects.all())}
        email_dict = {u.email: u.email for u in list(User.objects.all())}
        for i in range(100):

            username = fake.user_name()
            while username in username_dict:
                username = fake.user_name()

            email = fake.email()
            while email in email_dict:
                email = fake.email()

            reader = User(**{
                'username': username,
                'nickname': username,
                'password': make_password(get_random_password()),
                'is_superuser': False,
                'email': email,
                'avatar': 'upload/2021/07/14/keai.jpeg',
                'gender': random.choice(Constant.GENDERS)[0],
                'student_id': ''.join(random.sample(string.digits, 9)),
                'college_id': random.choice(college_list),
                'role': 'Reader',
                'is_active': True
            })
            readers.append(reader)
        User.objects.bulk_create(readers)
        readers = list(User.objects.filter(is_active=True, role='Reader'))
        books = list(Book.objects.filter(status=Constant.BOOK_STATUS_AVAILABLE))
        comment_summaries = {s.book.id: s for s in list(CommentSummary.objects.all())}
        comments = []
        comment_set = set()
        for i in range(1445):
            user: User = random.choice(readers)
            book: Book = random.choice(books)
            if str(user.id) + '_' + str(book.id) in comment_set:
                continue

            comment = Comment(**{
                'user': user,
                'book': book,
                'rating': random.randint(1, 10),
                'content': fake.paragraph()
            })
            comments.append(comment)
            comment_set.add(str(user.id) + '_' + str(book.id))

            if comment.book.id in comment_summaries:
                comment_summary = comment_summaries[comment.book.id]
                rating_number = comment_summary.rating_number + 1
                comment_summary.rating = round(
                    (comment_summary.rating * comment_summary.rating_number + comment.rating) / (
                        rating_number), 2)
                comment_summary.rating_number = rating_number
            else:
                comment_summary = CommentSummary(book=comment.book, rating=comment.rating, rating_number=1)
                comment_summaries[comment.book.id] = comment_summary

        Comment.objects.bulk_create(comments)

        create_summaries = []
        update_summaries = []
        for summary in comment_summaries.values():
            if summary.id:
                update_summaries.append(summary)
            else:
                create_summaries.append(summary)

        CommentSummary.objects.bulk_update(update_summaries, ('rating_number', 'rating'))
        CommentSummary.objects.bulk_create(create_summaries)

        return Response({'detail': 'comments generation has done'})
