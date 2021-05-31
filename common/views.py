import logging

from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.hashers import make_password
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from common.constant import Constant
from common.models import College, User
from common.serializers import CollegeSerializer, UserSerializer, UserLoginSerializer, UserPasswordSerializer
from common.utils import get_upload_file_path


def get_default_password():
    return {'password': make_password('12345678.Abc')}


class BaseError(ValidationError):
    def __init__(self, detail=None, code=None):
        super(BaseError, self).__init__(detail={'detail': detail})


class LibraryPagination(PageNumberPagination):
    """
        customer pagination
    """
    # default page size
    page_size = 10
    # page size param in page size
    page_size_query_param = 'page_size'
    # page param in api
    page_query_param = 'page'
    # max page size
    max_page_size = 100


class LibraryViewSetMixin(object):
    pagination_class = LibraryPagination
    filter_backends = [DjangoFilterBackend]
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, **kwargs):
        super(LibraryViewSetMixin, self).__init__(**kwargs)
        self.filterset_fields = []
        self.init_filter_field()

    def init_filter_field(self):
        """
        Init filter field by the fields' intersection in model and serializer
        e.g. `book/?id=1&authors=2`
        :return:  None
        """
        serializer = self.get_serializer_class()
        if not hasattr(serializer, 'Meta'):
            return
        meta = serializer.Meta

        if not hasattr(meta, 'model'):
            return
        model = meta.model

        if not hasattr(meta, 'fields'):
            ser_fields = []
        else:
            ser_fields = meta.fields

        for field in ser_fields:
            if not hasattr(model, field):
                continue
            self.filterset_fields.append(field)

    def perform_update(self, serializer):
        user = self.fill_user(serializer, 'update')
        serializer.save(**user)

    def perform_create(self, serializer):
        user = self.fill_user(serializer, 'create')
        serializer.save(**user)

    @staticmethod
    def fill_user(serializer, mode):
        """
        before save, fill user info into para from session
        :param serializer: Model's serializer
        :param mode: create or update
        :return: None
        """
        request = serializer.context['request']

        user_id = request.user.id
        ret = {'modifier': user_id}

        if mode == 'create':
            ret['creator'] = user_id
        return ret

    def get_pk(self):
        if hasattr(self, 'kwargs'):
            return self.kwargs.get('pk')


class BaseModelViewSet(LibraryViewSetMixin, viewsets.ModelViewSet):
    pass


class CollegeViewSet(BaseModelViewSet):
    queryset = College.objects.all().order_by('name')
    serializer_class = CollegeSerializer
    permission_classes = [permissions.IsAdminUser]


class UserViewSet(BaseModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        user = self.fill_user(serializer, 'create')
        user.update(get_default_password())
        serializer.save(**user)


class UserLoginViewSet(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=200)
        else:
            ret = {'detail': 'Username or password is wrong'}
            return Response(ret, status=403)


class UserLogoutViewSet(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        auth_logout(request)
        return Response({'detail': 'logout successful !'})


class PasswordUpdateViewSet(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserPasswordSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        """
        Parameter: id->user's id your will reset, not your self
        """
        user_id = request.data.get('id', '')
        user = User.objects.get(id=user_id)

        if user is not None and user.is_active:
            user.password = get_default_password()
            user.save()
            return Response({
                'detail': 'password reset successful !'
            })
        else:
            ret = {'detail': 'User does not exist !'}
            return Response(ret, status=403)

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        password = request.data.get('password', '')
        new_password = request.data.get('new_password', '')
        user = User.objects.get(id=user_id)
        if user.check_password(password):
            ret = {'detail': 'old password is wroong !'}
            return Response(ret, status=403)

        user.set_password(new_password)
        user.save()
        return Response({
            'detail': 'password changed successful !'
        })


class ConstantViewSet(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserPasswordSerializer
    queryset = QuerySet()

    def get(self, request, *args, **kwargs):
        ret = {}
        for key in dir(Constant):
            if not key.startswith("_"):
                ret[key] = getattr(Constant, key)
        return Response(ret)


class ImageUploadViewSet(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):

        try:
            if request.method == 'POST' and request.FILES:
                uploaded_file = request.FILES['file']

                full_file_path, file_path = get_upload_file_path(uploaded_file.name)
                self.handle_uploaded_file(uploaded_file, full_file_path)

                response = {
                    'url': file_path
                }
                return Response(response)

        except Exception as e:
            logging.getLogger('default').error(e, exc_info=True)
            raise BaseError(detail='Upload failed', code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def handle_uploaded_file(f, file_path):
        destination = open(file_path, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()