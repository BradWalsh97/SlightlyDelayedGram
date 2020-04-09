from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.utils import timezone
from .forms import UserRegisterForm, CommentForm
from .models import Picture, Profile, Comment
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db.models import Count


@login_required
def home(request):
    profile = get_object_or_404(Profile, id=request.user.pk)
    picture_list = Picture.objects.filter(owner__in=profile.following.all()).order_by('-post_date')

    context = {
        'Pictures': picture_list
    }
    return render(request, 'users/main.html', context)


def trending(request):
    context = {
        'Pictures': Picture.objects.annotate(like_count=Count('likes')).order_by('-like_count')
    }
    return render(request, 'users/trending.html', context)


class PictureListView(ListView):
    model = Picture
    template_name = 'users/main.html'
    context_object_name = 'Pictures'
    ordering = ['-post_date']


def picture_detail(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    comments = Comment.objects.filter(picture=picture)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.picture = picture  # Changed from .post to .picture MAY BE WRONG
            comment.author = request.user
            comment_form.save()
    else:
        comment_form = CommentForm()

    context = {
        'picture': picture,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'users/picture_detail.html', context)


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
    context = {
        'latest_picture_list': latest_picture_list
    }
    return render(request, 'users/profile.html', context)


@login_required
def follow_user(request):
    profile = get_object_or_404(Profile, id=request.POST.get('profile_id'))
    requesting_user = get_object_or_404(Profile, id=request.user.pk)
    is_followed = False
    if profile.followed.filter(id=request.user.pk).exists():
        profile.followed.remove(request.user)
        requesting_user.following.remove(profile.user)
        is_followed = False
    else:
        profile.followed.add(request.user)
        requesting_user.following.add(profile.user)
        is_followed = True
        send_mail('Follow Notification',
                  requesting_user.user.email + ' is now following you!',
                  'SlightlyDelayedGram123@gmail.com',
                  [profile.user.email],
                  fail_silently=False)
    return HttpResponseRedirect(profile.get_absolute_url())


def like_picture(request):
    post = get_object_or_404(Picture, id=request.POST.get('picture_id'))
    is_liked = False
    if post.likes.filter(id=request.user.pk).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(post.get_absolute_url())


@login_required
def peer_profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    requesting_user = Profile.objects.get(user=request.user)
    is_followed = False
    if profile.followed.filter(id=request.user.pk).exists():
        is_followed = True

    # Determine if profile is followable

    latest_picture_list = Picture.objects.filter(owner=profile.user).order_by('-post_date')
    context = {
        'latest_picture_list': latest_picture_list,
        'profile': profile,
        'is_followed': is_followed,
    }
    return render(request, 'users/peer_profile.html', context)


def upload_picture(request):
    try:
        pic = request.FILES['image']
        model = Picture(owner=request.user, picture_object=pic, post_date=timezone.now())
        model.save()
        profile = get_object_or_404(Profile, id=request.user.pk)
        print(profile.user)
        for follower in profile.followed.all():
            user_email = User.objects.get(username=follower).email
            print(user_email)
            send_mail('New Picture Notification',
                      request.user.username + ' has posted!',
                      'SlightlyDelayedGram123@gmail.com',
                      [user_email],
                      fail_silently=False)

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
