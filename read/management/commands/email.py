from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.template.loader import get_template
from django.utils import timezone
import feedparser
from ...models import FeedPublication, FeedSubscription
import os

class Command(BaseCommand):
    help = 'Sends an email to all feed subscriptions'

    def handle(self, *args, **kwargs):
        subs = FeedSubscription.objects.all()
        feeds_cache = {}

        for sub in subs:
            to_email = sub.user.email
            email_subject = f"{sub.feed.title} subscriptions"
            feeds_to_email = []
            pubs = FeedPublication.objects.filter(feed=sub.feed)
            for pub in pubs:
                rss_url = pub.pub.rss_url
                if rss_url in feeds_cache:
                    feeds_to_email.append(feeds_cache[rss_url])
                    continue
                feed = feedparser.parse(rss_url)
                feed['entries'] = feed['entries'][:10]
                feeds_to_email.append(feed)
                feeds_cache[rss_url] = feed
            
            template = get_template('read/email.html')
            context = {'feeds': feeds_to_email, 'feed': sub.feed}
            message = template.render(context)

            send_mail(
                subject=email_subject,
                message=message,
                from_email=os.getenv('EMAIL_HOST_USER'),
                recipient_list=[to_email],
                fail_silently=False,
                html_message=message
            )