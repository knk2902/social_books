from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from register.signals import send_login_notification
from .forms import CustomUserCreationForm
from django.http import HttpResponse
from .models import CustomUser
from .forms import UploadBookForm
from rest_framework.response import Response
from django.http import JsonResponse

from django.contrib.auth import get_user_model
from register.models import UploadedFiles
from register.serializers import UploadedFileSerializer

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from .serializers import CustomUserSerializer, CustomUserCreateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
user = get_user_model()
from django.core.mail import send_mail
from django.conf import settings
from .wrapper import my_books_wrapper
from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from django.http import JsonResponse


def login(request):
    if request.method == "POST":
        usern = request.POST.get("username")
        passw = request.POST.get("password")
        
        if usern and passw:
            user = CustomUser.objects.get(username=usern)
            auth_user = authenticate(request, username=usern, password=passw)
            print(user)
            print(auth_user)
            if auth_user is not None:
                auth_login(request, auth_user)
                # send_login_notification(auth_user)
                return redirect('index')
            else: 
                return redirect('login') 
        else:
            return redirect('login')
    return render(request, "login.html")

def logout_view(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('login')
    
    return render(request, 'login.html')


# def filter(request):
#     return render(request, "filter.html")


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
        return HttpResponse({'success': False})

    return render(request, "register.html", {"form": form})


def index_view(request):
    print(request.user.is_authenticated)
    if not request.user.is_authenticated:
        return redirect("login")
    context = {
        "full_name": request.user.fullname if request.user.is_authenticated else None,
    }
    return render(request, "index.html", context)


# def authors_and_sellers(request):
#     users = CustomUser.objects.filter(visibility=True)
#     return render(request, "filter.html", {"users": users})


def upload_books(request):
    if not request.user.is_authenticated:
        return redirect("login")
    else:
        username = request.user.username
    if request.method == "POST":
        form = UploadBookForm(request.POST, request.FILES)
        if form.is_valid():
            user_pr = form.save(commit=False)
            user_pr.save()
            return render(request, "index.html", {'user_pr': user_pr})
    else:
        form = UploadBookForm()

    return render(request, "upload_books.html", {"form": form, "username": username})
    return HttpResponse({'success': True})


def uploaded_files(request):
    if not request.user.is_authenticated:
        return redirect("login")
    else:
        username = request.user.username
        print(username)
        files = UploadedFiles.objects.all()
        # if username is not None:
        #     files = files.filter(username=username)
    return render(request, "uploaded_files.html", {"files": files})

@my_books_wrapper
def my_books_view(request):
    if request.user.is_authenticated:
        username = request.user.username
        print(username)
        file = UploadedFiles.objects.all()
        if username is not None:
            file = file.filter(username=username)
    return render(request, 'my_books.html', {'uploaded_files': file})


def Authors_sellers(request):
    # users = CustomUser.objects.all()
    if not request.user.is_authenticated:
        return redirect("login")
    else:
        filter_option = request.GET.get("filter", "all")

        # Filter users based on the filter option
        if filter_option == "all":
            users = CustomUser.objects.all()
        elif filter_option == "true":
            users = CustomUser.objects.filter(visibility=True)
        elif filter_option == "false":
            users = CustomUser.objects.filter(visibility=False)
        else:
            users = CustomUser.objects.all()

    context = {
        "users": users,
        "filter_option": filter_option,
    }
    html = render(request, "authors&sellers.html", context).content.decode('utf-8')
    return HttpResponse(html)


class UserDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        # user = CustomUser.objects.all()
        # serializer = CustomUserSerializer(user, data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # else:
        #     return Response(serializer.errors)
        usernames = [user.username for user in CustomUser.objects.all()]
        return Response(usernames)
    
    # def post(self, request):
    #     serializer = CustomUserSerializer(data=request.data)

    #     if not serializer.is_valid():
    #         print(serializer.errors)
    #         return Response(serializer.errors)
    #     serializer.save() 
    #     return Response(serializer.data)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, **args):
        serialzer = self.serializer_class(data=request.data, context={'request': request})
        serialzer.is_valid(raise_exception=True)
        user = serialzer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


# class RegisterUser(APIView):
#     def post(self, request):
#         serializer = CustomUserSerializer(data=request.data)

#         if not serializer.is_valid():
#             return Response(serializer.errors)
        
#         serializer.save()

#         user = CustomUser.objects.get(username=serializer.data['username'])
#         token_obj, _ = Token.objects.get_or_create(user=user)

#         return Response({'payload': serializer.data, 'token': str(token_obj)})

# class FileDetailView(generics.RetrieveAPIView):
#     queryset = UploadedFiles.objects.all()
#     serializer_class = UploadedFileSerializer
#     permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_uploaded_file(request, file_id):
    try:
        file = UploadedFiles.objects.get(username=file_id)
        return Response({'file_url': file.file.url})
    except UploadedFiles.DoesNotExist:
        return Response({'error': 'File not found'}, status=404)

# def send_email(request):
#     subject = 'Hello from social_book'
#     message = 'This is a test email sent from social_book.'
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = ['recipient@example.com']  

#     send_mail(subject, message, email_from, recipient_list)
#     return HttpResponse('Email sent successfully!')

