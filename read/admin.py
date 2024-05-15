from django.contrib import admin
from .models import Feed, Publication, FeedPublication, FeedSubscription

models = [Feed, Publication, FeedPublication, FeedSubscription]
admin.site.register(models)