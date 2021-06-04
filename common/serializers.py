from rest_framework import serializers

from common.models import User, College


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar', 'email', 'is_active', 'role',
                  'admission_at', 'student_id', 'gender', 'college']


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }


class UserPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'new_password']

    @staticmethod
    def get_new_password(obj):
        return obj.password or ''


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['id', 'name']
