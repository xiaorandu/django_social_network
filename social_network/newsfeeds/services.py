from friendships.services import FriendshipService
from newsfeeds.models import NewsFeed
from social_network.cache import USER_NEWSFEEDS_PATTERN
from utils.redis_helper import RedisHelper
from celery import shared_task

@shared_task
def fanout_newsfeeds_task(tweet_id):
    from tweets.models import Tweet
    tweet = Tweet.objects.get(id=tweet_id)
    newsfeeds = [
        NewsFeed(user=follower, tweet=tweet)
        for follower in FriendshipService.get_followers(tweet.user)
    ]
    newsfeeds.append(NewsFeed(user=tweet.user, tweet=tweet))
    NewsFeed.objects.bulk_create(newsfeeds)

    # Push to cache
    for newsfeed in newsfeeds:
        key = USER_NEWSFEEDS_PATTERN.format(user_id=newsfeed.user_id)
        RedisHelper.push_object(key, newsfeed)
        
class NewsFeedService(object):

    @classmethod
    def fanout_to_followers(cls, tweet):
        # Enqueue the task to run asynchronously
        fanout_newsfeeds_task.delay(tweet.id)

    @classmethod
    def get_cached_newsfeeds(cls, user_id):
        queryset = NewsFeed.objects.filter(user_id=user_id).order_by('-created_at')
        key = USER_NEWSFEEDS_PATTERN.format(user_id=user_id)
        return RedisHelper.load_objects(key, queryset)

    @classmethod
    def push_newsfeed_to_cache(cls, newsfeed):
        queryset = NewsFeed.objects.filter(user_id=newsfeed.user_id).order_by('-created_at')
        key = USER_NEWSFEEDS_PATTERN.format(user_id=newsfeed.user_id)
        RedisHelper.push_object(key, newsfeed, queryset)
