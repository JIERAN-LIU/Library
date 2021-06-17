from rest_framework import serializers

from common.models import User, College


class UserSerializer(serializers.ModelSerializer):
    college_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'avatar', 'email', 'is_active', 'role',
                  'admission_at', 'student_id', 'gender', 'college', 'college_info', ]

    @staticmethod
    def get_college_info(obj):
        if obj.college:
            return {'id': obj.college.id, 'name': obj.college.name}
        return {}


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
