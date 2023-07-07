from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from register.views import FileDetailView
from rest_framework.authtoken import views as views1
from .views import CustomAuthToken, UserDetailAPI
from django.views.decorators.csrf import csrf_exempt
from register.views import get_uploaded_file

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('index/', views.index_view, name='index'),
    # path('filter/', views.authors_and_sellers, name='filter'),
    path('upload-books/', views.upload_books, name='upload_books'),
    path('uploaded-files/', views.uploaded_files, name='uploaded_files'),
    path('authors-sellers/', views.Authors_sellers, name='Authors'),
    # path('auth/', views1.obtain_auth_token),
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.jwt')),
    path('api/files/<str:file_id>/', get_uploaded_file, name='get_uploaded_file'),
    # path('', include('register.urls')),
    path('api/token/auth', csrf_exempt(CustomAuthToken.as_view())),
    path("api/users/", UserDetailAPI.as_view()),
    # path('register/', RegisterUser.as_view()),
    path('my-books/', views.my_books_view, name='my_books'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
