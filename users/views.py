from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.utils import timezone
from .forms import UserRegisterForm
from .models import Picture, Profile
from django.views.generic import ListView, DetailView
from django.db.models import Q


def home(request):
    context = {
        'Pictures': Picture.objects.all()
    }
    return render(request, 'users/main.html', context)


def trending(request):
    context = {
        'Pictures': Picture.objects.all()
    }
    return render(request, 'users/trending.html', context)


class PictureListView(ListView):
    model = Picture
    template_name = 'users/main.html'
    context_object_name = 'Pictures'
    ordering = ['-post_date']


class UserPictureListView(ListView):
    model = Picture
    template_name = 'users/peer_profile.html'
    context_object_name = 'Pictures'
    ordering = ['-post_date']


class PictureDetailView(DetailView):
    model = Picture


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
    return render(request, 'users/profile.html', context)


def peer_profile(request, pk):
    if request.method == 'POST':
        latest_picture_list = Picture.objects.get(pk=pk).order_by('-post_date')
        context = {'latest_picture_list': latest_picture_list}
    return render(request, 'users/peer_profile.html', context)
    # return Picture.objects.filter(owner=username).order_by('-post_date')


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


@login_required
def search(request):
    if request.method == 'POST':
        srch = request.POST['srh']

        if srch:
            match = Profile.objects.filter(Q(user__username__istartswith=srch))

            if match:
                return render(request, 'users/search.html', {'sr': match})
            else:
                messages.error(request, 'no result found')

        else:
            return HttpResponseRedirect('/search/')
    return render(request, 'users/search.html')
