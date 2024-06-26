from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import redirect, render
import requests, re
from bs4 import BeautifulSoup
from .forms import FeedForm, RegisterForm
from .models import Feed, Publication, FeedPublication, FeedSubscription

def home(request):
    return render(request, 'read/home.html')

def user(request, name):
    user = User.objects.get_by_natural_key(username=name)
    feeds_created = Feed.objects.filter(author = user)
    subs = FeedSubscription.objects.filter(user = user)
    feeds_subscribed = list(map(lambda s:s.feed, subs))
    return render(request, 'read/user.html', {"user": user, "feeds_created": feeds_created, "feeds_subscribed": feeds_subscribed})

def feeds(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed
    PAGE_SIZE = 5
    page = request.GET.get('page') or 1
    feeds = Feed.objects.all()
    paginator = Paginator(feeds, PAGE_SIZE)
    #todo order by date
    feeds_page = paginator.get_page(page)
    return render(request, 'read/feeds.html', {'feeds': feeds_page})

def pub(request, id):
    if request.method != 'GET':
        return HttpResponseNotAllowed
    pub = Publication.objects.get(id=id)
    try:
        feeds_pubs = FeedPublication.objects.filter(pub=pub)
        feeds = list(map(lambda s:s.feed, feeds_pubs))
    except:
        feeds = None
    return render(request, 'read/pub.html', {'pub': pub, 'feeds': feeds})

def pubs(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed
    PAGE_SIZE = 25
    page = request.GET.get('page') or 1
    pubs = Publication.objects.all()
    paginator = Paginator(pubs, PAGE_SIZE)
    #todo order by date
    pubs_page = paginator.get_page(page)
    return render(request, 'read/pubs.html', {'pubs': pubs_page})

def view_feed(request, id):
    if request.method != 'GET':
        return HttpResponseNotAllowed
    feed = Feed.objects.get(id=id)
    try:
        feed_pubs = FeedPublication.objects.filter(feed=feed)
        pubs = list(map(lambda s:s.pub, feed_pubs))
    except FeedPublication.DoesNotExist:
        pubs = None
    try:
        feed_subs = FeedSubscription.objects.filter(feed=feed)
        subs = list(map(lambda s:s.user, feed_subs))
    except FeedPublication.DoesNotExist:
        subs = None
    subd = False
    if request.user:
        try:
            user_subs = FeedSubscription.objects.filter(feed=feed, user=request.user.id)
            if len(user_subs):
                subd = True
        except FeedSubscription.DoesNotExist:
            subd = False
    return render(request, 'read/feed.html', {'feed': feed, 'pubs': pubs, 'subs': subs, 'subd': subd})

@login_required(login_url="/login")
def create_feed(request):
    if request.method == 'POST':
        form = FeedForm(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.author = request.user
            feed.save()
            sub = FeedSubscription(feed=feed, user=request.user)
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
            sub = FeedPublication(pub=pub, feed=feed)
            sub.save()
        return redirect(f'/feed/{feed.id}')

@login_required(login_url="/login")
def delete_feed(request, id):
    feed = Feed.objects.get(id=id)
    if request.user != feed.author:
        return HttpResponseForbidden
    feed.delete()
    return redirect(f'/user/{request.user.username}')

@login_required(login_url="/login")
def edit_sub(request, id):
    feed = Feed.objects.get(id=id)
    sub = FeedSubscription.objects.filter(feed=feed, user=request.user)
    if len(sub):
        sub[0].delete()
    else:
        new_sub = FeedSubscription()
        new_sub.user = request.user
        new_sub.feed = feed
        new_sub.save()
    return redirect(f'/feed/{id}')
    
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {"form": form})

@login_required(login_url="/login")
def create_pub(request):
    if request.method == 'POST':
        url = (request.POST.get('link'))
        rss = get_rss_feed(url)
        if rss:
            title = (request.POST.get('title'))
            pub = Publication(pub_url = url, rss_url = rss, title = title)
            pub.save()
            return redirect('/pubs')
        
    return render(request, 'read/create_pub.html')

def get_rss_feed(website_url):
    if website_url is None or not website_url.startswith('https://'):
        return None
    if website_url.startswith('https://www.reddit.com/'):
        if not website_url.endswith('/'):
            website_url = website_url + '/'
        return str(website_url + '.rss')
    source_code = requests.get(website_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, features="html.parser")
    for link in soup.find_all("link", {"type" : "application/rss+xml"}):
        href = link.get('href')
        if not href.startswith('http'):
            if href.startswith('/') and website_url.endswith('/'):
                href = href[1:]
            if not href.startswith('/') and not website_url.endswith('/'):
                href = '/' + href
            href = website_url + href
        return str(href)

