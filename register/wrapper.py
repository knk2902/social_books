from django.shortcuts import redirect
from .models import UploadedFiles

def my_books_wrapper(view_func):
    def wrapper(request, *args, **kwargs):
        file = UploadedFiles.objects.filter(username= request.user.username)
        has_uploaded_files = file.exists()
        if request.user.is_authenticated:
            if has_uploaded_files:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('upload_books')
        else:
            return redirect('login')

    return wrapper
