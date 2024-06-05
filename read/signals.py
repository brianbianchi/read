from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import FeedPublication, FeedSubscription

@receiver(post_save, sender=FeedSubscription)
def feed_sub_post_save(sender, instance, created, **kwargs):
    if created:
        feed = instance.feed
        feed.num_subs += 1
        feed.save()

@receiver(post_delete, sender=FeedSubscription)
def feed_sub_post_delete(sender, instance, **kwargs):
    feed = instance.feed
    feed.num_subs -= 1
    feed.save()

@receiver(post_save, sender=FeedPublication)
def feed_pub_post_save(sender, instance, created, **kwargs):
    if created:
        feed = instance.feed
        feed.num_pubs += 1
        feed.save()
        pub = instance.pub
        pub.num_feeds += 1
        pub.save()

@receiver(post_delete, sender=FeedPublication)
def feed_pub_post_delete(sender, instance, **kwargs):
    feed = instance.feed
    feed.num_pubs -= 1
    feed.save()
    pub = instance.pub
    pub.num_feeds -= 1
    pub.save()