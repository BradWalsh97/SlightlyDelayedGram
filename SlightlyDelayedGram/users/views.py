from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from .forms import UserRegisterForm
from .models import Picture

posts = [
    {
        'author': 'Jonathan',
        'title': 'Test Post 1',
        'content': 'Check out this sick pic',
        'date_posted': 'January 17, 2019'
    },
    {
        'author': 'Jonathan',
        'title': 'Test Post 2',
        'content': 'Check out this sick pic',
        'date_posted': 'January 18, 2019'
    },
    {
        'author': 'Jonathan',
        'title': 'Test Post 3',
        'content': 'Check out this sick pic',
        'date_posted': 'January 19, 2019'
    },
]


def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'users/main.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    latest_picture_list = Picture.objects.filter(owner=request.user).order_by('-post_date')
    context = {'latest_picture_list': latest_picture_list}
    return render(request,'users/profile.html', context)


def upload_picture(request):
    try:
        pic = request.FILES['image']
        model = Picture(owner=request.user, picture_object=pic, post_date=timezone.now())
        model.save()
        return redirect('profile')
    except:
        return redirect('profile')

def delete_picture(request, pk):
    if request.method == 'POST':
        picture = Picture.objects.get(pk=pk)
        picture.delete()
    return redirect('profile')
