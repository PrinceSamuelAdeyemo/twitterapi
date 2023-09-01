from django.urls import path
from .views import PostTweet, DeleteTweet, Retweet, UnRetweet, ReplyTweet, SearchNameorTweets, Tt

urlpatterns = [
    path('posttweet', PostTweet.as_view(), name = 'posttweet'),
    path('deletetweet', DeleteTweet.as_view(), name = 'deletetweet'),
    path('retweet', Retweet.as_view(), name = 'retweet'),
    path('unretweet', UnRetweet.as_view(), name = 'unretweet'),
    path('replytweet',ReplyTweet.as_view(), name = 'replytweet'),
    #path('posttweet',PostTweet.as_view(), name = 'posttweet'),
    path('searchbot_tag', SearchNameorTweets.as_view(), name = 'searchbot_tag'),
    path('tt', Tt.as_view(), name='tt'),
]
