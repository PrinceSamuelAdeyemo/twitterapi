from rest_framework import serializers
from .models import UserModel, ClientModel

class UserModelSerializer(serializers.ModelSerializer):
    #user_model = UserModel()
    
    class Meta:
        model = UserModel
        fields = "__all__"
    
    def create(self, **validated_data):
        user = User(email = validated_data['email'], password = validated_data['password'])
        user.set_password(password = validated_data['password'])
        user.save()
        return user
    
class ClientModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientModel
        fields = "__all__"
        
    def create(self, **validated_data):
        
        client = ClientModel(user_tagger_username = validated_data["User tagger username"], user_tagger_id= validated_data["user_tagger"], 
                            tweet_owner_id = validated_data["Main tweetowner ID"], maintweet_id = validated_data["Main tweet ID"], 
                            tagtweet_id = validated_data["tagtweet ID"], small_vids_url = validated_data["main_video"]["small"]["vidurl"], 
                            medium_vids_url = validated_data["main_video"]["medium"]["vidurl"], large_vids_url = validated_data["main_video"]["large"]["vidurl"])
        
        """
        client = ClientModel(tweet_id = validated_data['tweet_id'], in_reply_to_status_id= validated_data['in_reply_to_status_id'],
                             in_reply_to_screen_name = validated_data['in_reply_to_screen_name'], usertag_id=validated_data['usertag_id'], 
                             is_quote_status=validated_data['is_quote_status'], tweet_media_url=validated_data['tweet_media_url'], 
                             created_at=['created_at'])
        """
        client.save()
        return client

class PostTweetSerializer(serializers.Serializer):
    tweet_content = serializers.CharField(max_length=256)
    tweet_media = serializers.FileField(required=False, allow_null=True)
    
class DeleteTweetSerializer(serializers.Serializer):
    tweet_id = serializers.IntegerField()
    
class ReTweetSerializer(serializers.Serializer):
    tweet_id = serializers.IntegerField()
    
class UnReTweetSerializer(serializers.Serializer):
    tweet_id = serializers.IntegerField()

class ReplyTweetSerializer(serializers.Serializer):
    tweet_content = serializers.CharField(max_length=256)
    tweet_id = serializers.IntegerField()
    
class QuoteTweetSerializer(serializers.Serializer):
    tweet_content = serializers.CharField(max_length=256)
    tweet_id = serializers.IntegerField()
    
class ScheduleTweetSerializer(serializers.Serializer):
    tweet_content = serializers.CharField(max_length=256)
    date = serializers.DateTimeField(default_timezone='UTC')
    tweet_media = serializers.FileField(required=False, allow_null=True)
    
class UnScheduleTweetSerializer(serializers.Serializer):
    tweet_id = serializers.IntegerField()
    
class ScheduleReplySerializer(serializers.Serializer):
    tweet_content = serializers.CharField(max_length=256)
    date = serializers.DateTimeField(default_timezone='UTC')
    tweet_id = serializers.IntegerField()
    tweet_media = serializers.FileField(required=False, allow_null=True)
    
class DmSerializer(serializers.Serializer):
    tweet_content = serializers.CharField(max_length=256)
    tweet_id = serializers.IntegerField()
    tweet_media = serializers.FileField(required=False, allow_null=True)
    
class CreatePollSerializer(serializers.Serializer):
    #choice = ['']
    poll_question = serializers.CharField(max_length=256)
    poll_choice = serializers.CharField(max_length=256)
    poll_duration = serializers.DateTimeField(default_timezone='UTC')



############## ACTIONS DONE IN A SPECIFIC TWEET ################
class LikePostSerializer(serializers.Serializer):
    tweet_like = serializers.BooleanField(required=True, allow_null=False)
    tweet_id = serializers.IntegerField()

class UnLikePostSerializer(serializers.Serializer):
    tweet_unlike = serializers.BooleanField(required=True, allow_null=False)
    tweet_id = serializers.IntegerField()

class MuteAccountSerializer(serializers.Serializer):
    account_mute = serializers.BooleanField(required=True, allow_null=False)
    account_id = serializers.IntegerField()
    
class UnMuteAccountSerializer(serializers.Serializer):
    account_unmute = serializers.BooleanField(required=True, allow_null=False)
    account_id = serializers.IntegerField()

class EnableAccountNotificationsSerializer(serializers.Serializer):
    enable_account_not = serializers.BooleanField(required=True, allow_null=False)
    account_id = serializers.IntegerField()

class DisableAccountNotificationsSerializer(serializers.Serializer):
    disable_account_not = serializers.BooleanField(required=True, allow_null=False)
    account_id = serializers.IntegerField()

class BlockAccountSerializer(serializers.Serializer):
    block_account = serializers.BooleanField(required=True, allow_null=False)
    account_id = serializers.IntegerField()

class UnBlockAccountSerializer(serializers.Serializer):
    disable_account = serializers.BooleanField(required=True, allow_null=False)
    account_id = serializers.IntegerField()



######## Actions done in the user's profile  ###########

class UpdateProfileImageSerializer(serializers.Serializer):
    profile_image = serializers.FileField(required=False, allow_null=True)

class UpdateProfileBanner(serializers.Serializer):
    profile_banner = serializers.FileField(required=False, allow_null=True)

class UpdateProfileInfo(serializers.Serializer):
    profile_name = serializers.CharField(max_length=256)
    profile_description = serializers.CharField(max_length=256)
    profile_location = serializers.CharField(max_length=256)

########## Actions done a topic ################

class FollowTopicSerializer(serializers.Serializer):
    follow_topic = serializers.BooleanField(required=True, allow_null=False)
    topic_id = serializers.IntegerField()

class FollowTopicSerializer(serializers.Serializer):
    unfollow_topic = serializers.BooleanField(required=True, allow_null=False)
    topic_id = serializers.IntegerField()

########### List section for the user's account ################
"""
account.add_list_member(222, 1234)
account.remove_list_member(222, 1234)
account.delete_list(222)
account.pin_list(222)
account.unpin_list(222)
"""

class CreateListSerializer(serializers.Serializer):
    list_name = serializers.CharField(max_length=256)
    list_description = serializers.CharField(max_length=256)
    private = serializers.BooleanField(default=False, allow_null=False)
    
class UpdateListSerializer(serializers.Serializer):
    list_id = serializers.IntegerField()
    list_name = serializers.CharField(max_length=256)
    list_description = serializers.CharField(max_length=256)
    private = serializers.BooleanField(default=False, allow_null=False)

class UpdateListBannerSerializer(serializers.Serializer):
    list_id = serializers.IntegerField()
    list_bannerimage = serializers.FileField(required=True, allow_null=False)

class DeleteListBannerSerializer(serializers.Serializer):
    list_id = serializers.IntegerField()

class SearchNameorTweetsSerializer(serializers.Serializer):
    #name = serializers.CharField(max_length = 50, required=False)
    user_tagger_username = serializers.CharField(max_length = 50),
    user_tagger_id = serializers.IntegerField(),
    tweet_owner_id = serializers.IntegerField(),
    maintweet_id = serializers.IntegerField(),
    tagtweet_id = serializers.IntegerField(),
    small_vids_url = serializers.URLField(),
    medium_vids_url = serializers.URLField(),
    large_vids_url = serializers.URLField(),
    
