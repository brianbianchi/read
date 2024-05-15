from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import redirect, render
from .forms import FeedForm, RegisterForm
from .models import Feed, Publication, FeedPublication, FeedSubscription

def home(request):
    pubs = Publication.objects.all()
    return render(request, 'read/home.html', {"pubs": pubs})

def user(request, name):
    user = User.objects.get_by_natural_key(username=name)
    feeds = Feed.objects.filter(author = user)
    return render(request, 'read/user.html', {"user": user, "feeds": feeds})

def feeds(request):
    PAGE_SIZE = 5
    page = request.GET.get('page') or 1
    feeds = Feed.objects.all()
    paginator = Paginator(feeds, PAGE_SIZE)
    #todo order by date
    feeds_page = paginator.get_page(page)
    return render(request, 'read/feeds.html', {'feeds': feeds_page})

def view_feed(request, id):
    if request.method != 'GET':
        return HttpResponseNotAllowed
    feed = Feed.objects.get(id=id)
    try:
        subs = FeedPublication.objects.filter(feed=feed)
    except FeedPublication.DoesNotExist:
        subs = None
    return render(request, 'read/feed.html', {'feed': feed, 'subs': subs})

@login_required(login_url="/login")
def create_feed(request):
    if request.method == 'POST':
        form = FeedForm(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.author = request.user
            feed.save()
            sub = FeedSubscription()
            sub.feed = feed
            sub.user = request.user
            sub.save()
            return redirect(f"/feed/{feed.id}")
    else:
        form = FeedForm()

    return render(request, 'read/create_feed.html', {"form": form})

@login_required(login_url="/login")
def edit_feed(request, id):
    feed = Feed.objects.get(id=id)
    if request.user != feed.author:
        return HttpResponseForbidden
    pubs = Publication.objects.all()
    pubs_dict = {pub: False for pub in pubs}
    if request.method == 'GET':
        try:
            subs = FeedPublication.objects.filter(feed=feed)
            keys = pubs_dict.keys()
            for sub in subs:
                if sub.pub in keys:
                    pubs_dict[sub.pub] = True
        finally:
            return render(request, 'read/edit_feed.html', {'feed': feed, 'pubs': pubs_dict})
    if request.method == 'POST':
        form_subs = request.POST.getlist('subs')
        FeedPublication.objects.filter(feed=feed).delete()
        for sub_rss_url in form_subs:
            pub = next((pub for pub in pubs if pub.rss_url == sub_rss_url), None)
            sub = FeedPublication()
            sub.pub = pub
            sub.feed = feed
            sub.save()
        return redirect(f'/feed/{feed.id}')
    
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {"form": form})
