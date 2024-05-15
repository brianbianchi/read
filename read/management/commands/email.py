from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.template.loader import get_template
from django.utils import timezone
import feedparser
from ...models import FeedPublication, FeedSubscription

class Command(BaseCommand):
    help = 'Sends an email to all feed subscriptions'

    def handle(self, *args, **kwargs):
        subs = FeedSubscription.objects.all()
        feeds_cache = {}

        for sub in subs:
            to_email = sub.user.email
            email_subject = f"{sub.feed.title} daily subscriptions"
            feeds_to_email = []
            pubs = FeedPublication.objects.filter(feed=sub.feed)
            for pub in pubs:
                rss_url = pub.pub.rss_url
                if rss_url in feeds_cache:
                    feeds_to_email.append(feeds_cache[rss_url])
                    continue
                feed = feedparser.parse(rss_url)
                feed['entries'] = feed['entries'][:2]
                feeds_to_email.append(feed)
                feeds_cache[rss_url] = feed
            
            template = get_template('read/email.html')
            context = {'feeds': feeds_to_email}
            message = template.render(context)

            # send_mail(
            #     subject=subject,
            #     message=message,
            #     from_email=None,
            #     recipient_list=[to_email],
            #     fail_silently=False,
            #     html_message=message
            # )
            print(message)
                




        # subject = "Your Email Subject"
        # to_email = "briguy2486@aim.com"

        # email_message = EmailMessage(subject, body, 
        # from_email='your_email_address', to=[to_email])
        # email_message.send()

        # order_items = [
        #     {'name': 'Item A', 'quantity': 2},
        #     {'name': 'Item B', 'quantity': 3},
        # ]
        # recipient_name = 'John Doe'
        # template = get_template('read/email.html')
        # context = {'recipient_name': recipient_name, 
        #                           'order_items': order_items}
        # message = template.render(context)

        # send_mail(
        #     subject=subject,
        #     message=message,
        #     from_email=None,
        #     recipient_list=[to_email],
        #     fail_silently=False,
        #     html_message=message
        # )
        # self.stdout.write('sent')
        # time = timezone.now().strftime('%X')
        # self.stdout.write("It's now %s" % time)