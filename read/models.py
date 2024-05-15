from django.db import models
from django.contrib.auth.models import User

class Publication(models.Model):
    title = models.CharField(max_length=200)
    pub_url = models.CharField(max_length=200)
    rss_url = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + "\n" + self.pub_url
    

class Feed(models.Model):
    OPTIONS = [
        (1, 'Once a day'),
        (7, 'Once a week'),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    email_frequency = models.IntegerField(choices=OPTIONS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + "\n" + self.description
    
class FeedPublication(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    pub = models.ForeignKey(Publication, on_delete=models.CASCADE)

    def __str__(self):
        return self.feed.title + "\n" + self.pub.title
    
class FeedSubscription(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.feed.title + "\n" + self.user.username
    