from django.db import models
from django.contrib.auth.models import User
from django.contrib import auth
#from django.contrib.auth.

# Create your models here.
class UserModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    

class Client2Model(models.Model):
    tweet_owner_id = models.IntegerField(),
    maintweet_id = models.IntegerField(),
    
class ClientModel(models.Model):
    tweetowner = models.ManyToManyField(Client2Model)
    user_tagger_username = models.CharField(max_length = 50),
    user_tagger_id = models.IntegerField(),
    
    tagtweet_id = models.IntegerField(),
    small_vids_url = models.URLField(),
    medium_vids_url = models.URLField(),
    large_vids_url = models.URLField(),
    
    """
    id = models.IntegerField(primary_key=True)
    tweet_id = models.IntegerField()
    in_reply_to_status_id = models.IntegerField()
    in_reply_to_screen_name = models.CharField(max_length=60)
    usertag_id = models.IntegerField(unique=True)
    is_quote_status = models.BooleanField()
    tweet_media_url = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    """
    def __str__(self):
        return self.user_tagger_id
    