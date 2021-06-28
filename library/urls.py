from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# drf_yas 从这里开始（Swagger)
schema_view = get_schema_view(
    openapi.Info(
        title="Library Management System build with Django REST framework API",
        description="Library Management System based on KNN recommendation algorithm and Full-text search Engine ",
        default_version='v1',
        terms_of_service="",
        contact=openapi.Contact(email="zgj0607@163.com"),
        license=openapi.License(name="GPLv3 License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# here is end

urlpatterns = [
    path('', include('book.urls', namespace='book')),
    path('', include('borrow.urls', namespace='borrow')),
    path('', include('common.urls', namespace='common')),
    path('', include('comment.urls', namespace='comment')),
    path('', include('recommendation.urls', namespace='recommendation')),
    path('', include('search.urls', namespace='search')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(
        r"swagger(?P<format>\.json|\.yaml)",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
