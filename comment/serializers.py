from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    book_info = serializers.SerializerMethodField(read_only=True)
    user_info = serializers.SerializerMethodField(read_only=True)
