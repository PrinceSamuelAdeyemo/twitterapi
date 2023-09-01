from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ClientModelSerializer, PostTweetSerializer, DeleteTweetSerializer, ReTweetSerializer, UnReTweetSerializer, \
    ReplyTweetSerializer, QuoteTweetSerializer, ScheduleTweetSerializer, UnScheduleTweetSerializer, SearchNameorTweetsSerializer

from .models import ClientModel, Client2Model
#### The library () being used
from twitter.account import Account
from twitter.scraper import Scraper
from twitter.search import Search


##### Python default libraries
import datetime
import requests
import asyncio
import json
# Create your views here.


email, username, password = "samuelprincetech@gmail.com", "@samfauxaccount", "w5?BrtyF+zDCUqh"
bot_tagName = 'samfauxaccount'
ct0 = '1866e7f385a0475b3f06fd9d66b1986af5382ce8aeda7f38b6370c118a0b9256a1846095b22fd9bd395a978805fe9e75413644c3526ccbf66ba3e3aea1f171fcc83fb2933870be7f207d31a624f1776e'
token = '2c8fc177dfc748a9678089144d87bc864cf42613'
account = Account(email, username, password)
search = Search(email, username, password)

class Login(APIView):
    def post(self, request):
        account = Account(cookies = {ct0, token})
        return Response("Successfully logged in!")


class PostTweet(APIView):
    def post(self, request):        
        serializer = PostTweetSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        tweet_content = serializer.validated_data['tweet_content']
        print(tweet_content)
        try:
            account.tweet(tweet_content)
        
        except:
            #account = Account(cookies = {ct0, token})
            account = Account(email, username, password)
            account.tweet(tweet_content)
        
        return Response(f"Your tweet has been submitted! = {tweet_content}")
   
    
class DeleteTweet(APIView):
    def post(self, request):
        serializer = DeleteTweetSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        tweet_id = serializer.validated_data['tweet_id']
        account = Account(cookies = {ct0, token})

        account.untweet(tweet_id)
        return Response("Your tweet has been deleted!")
    
class Retweet(APIView):
    def post(self, request):
        serializer = ReTweetSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        tweet_id = serializer.validated_data['tweet_id']
        account = Account(cookies = {ct0, token})
        account.retweet(tweet_id)
        return Response(f"The tweet id: {tweet_id} has been retweeted!")
    
class UnRetweet(APIView):
    def post(self, request):
        serializer = UnReTweetSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        tweet_id = serializer.validated_data['tweet_id']
        account = Account(cookies = {ct0, token})
        account.retweet(tweet_id)
        return Response(f"The tweet id: {tweet_id} has been Unretweeted")

class ReplyTweet(APIView):
    def post(self, request):
        serializer = ReplyTweetSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        tweet_id = serializer.validated_data['tweet_id']
        tweet_content = serializer.validated_data['tweet_content']
        
        account = Account(cookies = {ct0, token})
        account.reply(tweet_id, tweet_content)
        return Response(f"The tweet id: {tweet_id} has been replied")

class QuoteTweet(APIView):
    def post(self, request):
        serializer = QuoteTweetSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        tweet_content = serializer.validated_data['tweet_content']
        tweet_id = serializer.validated_data['tweet_id']
        account = Account(cookies = {ct0, token})
        account.quote(tweet_content, tweet_id)
        return Response(f"The tweet id: {tweet_id} has been quoted")

class ScheduleTweet(APIView):
    def post(self, request):
        serializer = ScheduleTweetSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        tweet_content = serializer.validated_data['tweet_content']
        tweet_date = serializer.validated_data['tweet_date']
        tweet_media = serializer.validated_data['photo']
        account = Account(cookies = {ct0, token})
        account.schedule_tweet(tweet_content, tweet_id)
        return Response(f"The tweet id: {tweet_id} has been scheduled")

class UnScheduleTweet(APIView):
    def post(self, request):
        serializer = UnScheduleTweetSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        tweet_id = serializer.validated_data['tweet_id']
        account = Account(cookies = {ct0, token})
        account.unschedule_tweet(tweet_id)
        return Response(f"The tweet id: {tweet_id} has been unscheduled")


class SearchNameorTweets(APIView):
    """
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SearchNameorTweetsSerializer
        elif self.request.method == 'POST':
            return ClientModelSerializer
        else:
            pass
        """
        
    def get(self, request):
        #serializer = self.serializer_class(data = request.data)
        serializer = SearchNameorTweetsSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        
    
    def post(self, request):
        #serializer = self.serializer_class(data = request.data)
        
        today_date = datetime.date.today()
        day_before = today_date - datetime.timedelta(1)
        
        day_begin = datetime.time(hour = 00, minute = 00, second = 00, microsecond = 00)
        current_time = datetime.datetime.now()
        parentTweet = None
        
        ########### Search for all the latest tags ########
        #search = Search(cookies = {ct0, token})
        search = Search(email, username, password)
        #scraper = Scraper(cookies = {ct0, token})
        scraper = Scraper(email, username, password)
        ########## Generate and assign the result to "latest_results"   ###########
        """
        latest_results = search.run(
            f'@samfauxaccount',
            # When the bot is TAGGED, starting from the day before to the current date plus if media (image or video) is attached which is optional by the way.
            #f'@{username} -from:samfauxaccount since:{day_before} until:{today_date} OR @{bot_tagName} filter:media since:{day_before} until:{today_date} ', 
            # When the bot is MENTIONED, starting from the day before to the current date plus if media (image or video) is attached which is optional by the way.
            #f'{username} has:mentions since:{day_before} until:{today_date} OR {bot_tagName} has:mentions since:{day_before} until:{today_date} filter:media', 
            # When the bot is HASH-TAGGED, starting from the day before to the current date plus if media (image or video) is attached which is optional by the way.
            #f'#{username} since:{day_before} until:{today_date} OR @{bot_tagName} filter:media since:{day_before} until:{today_date} ', 
        limit=5,
        latest=True,  # get latest tweets only
        retries=3,
        )
        """
        latest_results = search.run(
                limit=37,
                retries=5,
                queries=[
                    {
                        'category': 'Latest',
                        'query': '@samfauxaccount'
                    },
                ]
        )
        
    #try:
        ###### Get the tweet details of the people that tagged the bot  #############   
        str_tweet_ids = latest_results[0][0].get('globalObjects').get('tweets').keys()
        liststr_tweet_ids = list(str_tweet_ids)
        alldatareceived = {}
        
        for i in range(len(list(str_tweet_ids))):
            #Get the list of all the ids that tagged the bot over time
            tagtweet_id = latest_results[0][0].get('globalObjects').get('tweets').get(str(liststr_tweet_ids[i]))
            
            ### Should check if the tagtweet is a quote status or a reply-status,
            # If it is a reply-status
            if tagtweet_id.get('is_quote_status') == False and (tagtweet_id.get('in_reply_to_status_id')) != None:
                
                usertag_id = tagtweet_id.get('user_id') #  (The person that actually tagged)
                tweet_id = tagtweet_id.get('id')
                in_reply_to_status_id = tagtweet_id.get('in_reply_to_status_id')
                url = scraper.tweets_details([in_reply_to_status_id])[0]['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][0]['content']['itemContent']['tweet_results']['result']['legacy']['entities']['media'][0]['display_url']
                """
                created_at = tagtweet_id.get('created_at')
                full_text = tagtweet_id.get('full_text')
                """
                #search_status = ClientModel.objects.get(usertag_id = usertag_id, in_reply_to_status_id = in_reply_to_status_id)
                
                if search_status:
                    alldatareceived = None
                
                else:
                    in_reply_to_user_id = tagtweet_id.get('in_reply_to_user_id')
                    in_reply_to_screen_name = tagtweet_id.get('in_reply_to_screen_name')
                    
                    usertag_geo = tagtweet_id.get('geo')
                    usertag_coordinates = tagtweet_id.get('coordinates')
                    usertag_place = tagtweet_id.get('place')
                    is_quote_status = tagtweet_id.get('is_quote_status')
                    conversation_id = tagtweet_id.get('conversation_id')
                    
                    print("\nFor tweet details")
                    
                    vids = scraper.tweets_details([1673292522846846980])[0]['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][0]['content']['itemContent']['tweet_results']['result']['legacy']['extended_entities']['media'][0]#['video_info']['variants']
                    if "video_info" in vids:
                        #vids = scraper.tweets_details([1673292522846846980])[0]['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][0]['content']['itemContent']['tweet_results']['result']['legacy']['extended_entities']['media'][0]['video_info']['variants']
                        vids = vids['video_info']['variants']
                    
                        video_links = []
                        for i in range(len(vids)):
                            if "bitrate" in vids[i]:
                                video_links.append(vids[i])
                            
                            else:
                                pass
                        
                        datareceived = { 
                            (i+1) :{
                                "Created at": f"{created_at}",
                                "tweet_id": f"{tweet_id}",
                                #"full_text": f"{full_text}",
                                "in_reply_to_status_id": f"{in_reply_to_status_id}",
                                "in_reply_to_screen_name": f"{in_reply_to_screen_name}",
                                "usertag_id": f"{usertag_id}",
                                "is_quote_status": f"{is_quote_status}",
                                "tweet_media_url": f"{video_links}",
                            }
                        }
                        alldatareceived ={**alldatareceived, **datareceived}      
                        
                alldatareceived ={**alldatareceived, **datareceived}
                print(alldatareceived)
                alldataforparent = alldatareceived
                
                #serializer = ClientModelSerializer(data = alldataforparent)
                #serializer.is_valid(raise_exception=True)
            #print(request.data)
            
            
            
                #alldataforparent.get(str(i)).pop('in_reply_to_status_id')
            """    
            sendfor_parenttweet = requests.post('http://127.0.0.1:8000/searchbot_tag', json = alldataforparent)
            
            if sendfor_parenttweet.status_code == 200:
                response = sendfor_parenttweet.json
                print("ALL RESPONSES")
                print(response)
                print("ALL RESPONSES")
                
            else:
                response = 'Not caught'
                """  
     
        """    
        except AttributeError:
            return Response("Attribute Error")
        """        
            
        #print(in_reply_to_status_id)
        #return Response(alldatareceived)
        return Response(latest_results[0][0].get('globalObjects'))
   
      
class Tt(APIView):
    def post(self, request):
        
        email, username, password = "samuelprincetech@gmail.com", "@samfauxaccount", "w5?BrtyF+zDCUqh"
        ct0 = '1866e7f385a0475b3f06fd9d66b1986af5382ce8aeda7f38b6370c118a0b9256a1846095b22fd9bd395a978805fe9e75413644c3526ccbf66ba3e3aea1f171fcc83fb2933870be7f207d31a624f1776e'
        token = '2c8fc177dfc748a9678089144d87bc864cf42613'

        account = Account(email, username, password)
        search = Search(email, username, password)
        scraper = Scraper(email, username, password)
        #search = Search(cookies = {ct0, token})
        #scraper = Scraper(email, username, password)
        #print(latest_results)
        
        print("\nFor tweet details")
        
        today_date = datetime.date.today()
        
        all_details, details = {}, {}
        res = search.run(
                limit=5,
                retries=3,
                queries=[
                    {
                        'category': 'Latest',
                        'query': f'(@samfauxaccount -from:samfauxaccount) since:{today_date}'
                    },
                ]
        )        
        print(len(res[0]))
        for tag in range(len(res[0])):
            #Main tweet id [important]
            tweet = res[0][tag]["content"]["itemContent"]["tweet_results"]["result"]
            
            if not "in_reply_to_status_id_str" in tweet["legacy"]:
                pass
            
            else:
                maintweet_id = tweet["legacy"]["in_reply_to_status_id_str"]
            #maintweet_id = tweet["legacy"]["in_reply_to_status_id_str"]
        
            # For the video of the main tweet
                #if "video_info" in scraper.tweets_details([maintweet_id])[0]['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][0]['content']['itemContent']['tweet_results']['result']:
                vids_details = scraper.tweets_details([maintweet_id])[0]['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][0]['content']['itemContent']['tweet_results']['result']['legacy']
                url = vids_details['entities']['media'][0]['display_url']
                vids = vids_details['extended_entities']['media'][0]['video_info']['variants']
                for i in range(len(vids)): #632000
                    print(i)
                    if ("bitrate" in vids[i]):
                        if (vids[i]['bitrate'] == 632000):
                            small_vid_bitrate = vids[i]['bitrate']
                            small_vid_url = vids[i]['url']
                            
                        elif (vids[i]['bitrate'] == 950000):# and (vids[i]['bitrate'] < 1500000): #950000
                            medium_vid_bitrate = vids[i]['bitrate']
                            medium_vid_url = vids[i]['url']
                            
                        elif (vids[i]['bitrate'] == 2176000): #2176000
                            large_vid_bitrate = vids[i]['bitrate']
                            large_vid_url = vids[i]['url']
                        
                        else:
                            large_vid_bitrate = 'none'
                            large_vid_url = 'none'
                
                                  
                #vids = vids['video_info']['variants']
                #if "video_info" in vids:
                    #vids = scraper.tweets_details([1673292522846846980])[0]['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][0]['content']['itemContent']['tweet_results']['result']['legacy']['extended_entities']['media'][0]['video_info']['variants']
                    #vids = vids['video_info']['variants']
                
                tagtweet_id = tweet["rest_id"]
                user_tagger = tweet["core"]["user_results"]["result"]["rest_id"]
                user_tagger_men = tweet["core"]["user_results"]["result"]["legacy"]["screen_name"]
                # For main tweet owner
                tweet_owner = tweet["legacy"]["in_reply_to_user_id_str"]
                
            #Note: Use for loop
                details = {
                    (tag + 1):
                        {    # The main tweet owner id and the main tweet id
                            "Main tweetowner ID": tweet_owner,
                            "Main tweet ID": maintweet_id,
                            # The one who tagged the bot [id, username]
                            "User tagger id": user_tagger,
                            "User tagger username": user_tagger_men,
                            # The tagged tweet [reply to the main tweet] id
                            "tagtweet ID": tagtweet_id,
                            # The id and the link of the video in particular
                            #"video_url": maintweet_id,
                            
                            "main_video": {
                                "small":{
                                    "bitrate": small_vid_bitrate,
                                    "vidurl": small_vid_url,
                                },
                                "medium": {
                                    "bitrate": medium_vid_bitrate,
                                    "vidurl": medium_vid_url,
                                },
                                #"large": {
                                 #   "bitrate": large_vid_bitrate,
                                  #  "vidurl": large_vid_url,
                                #},
                    
                            },  
                        }
                }
                
                
                
                
                all_details = {**all_details, **details}
                    
        all_details = {**all_details, **details}
        
        """
        for i in range(len(all_details)):
            clientdetail = all_details[i]
            ""
            client = ClientModel(user_tagger_username = clientdetail["User tagger username"], user_tagger_id= clientdetail["user_tagger"], 
                                tweet_owner_id = clientdetail["Main tweetowner ID"], maintweet_id = clientdetail["Main tweet ID"], 
                                tagtweet_id = clientdetail["tagtweet ID"], small_vids_url = clientdetail["main_video"]["small"]["vidurl"], 
                                medium_vids_url = clientdetail["main_video"]["medium"]["vidurl"], large_vids_url = clientdetail["main_video"]["large"]["vidurl"])
            ""
            if User(username = str(clientdetail["user_tagger"]), password = "Default").exists():
                pass
            else:
                # Save the tagger to the Default User class
                user = User(username = str(clientdetail["user_tagger"]), password = "Default")
                user.save()
                # Save the main tweet owner to the Client2 Table
                client2 = Client2Model(tweet_owner_id = clientdetail["Main tweetowner ID"], maintweet_id = clientdetail["Main tweet ID"],)
                client2.save()
                # Save the tagger again to the Client Table/Model with extensive information.
                client = ClientModel(user_tagger_username = clientdetail["User tagger username"], user_tagger_id= clientdetail["user_tagger"], 
                            tagtweet_id = clientdetail["tagtweet ID"], small_vids_url = clientdetail["main_video"]["small"]["vidurl"], 
                            medium_vids_url = clientdetail["main_video"]["medium"]["vidurl"], large_vids_url = clientdetail["main_video"]["large"]["vidurl"])
                client.save()
                client.add(client2)
                #serializer = SearchNameorTweetsSerializer(clientdetail)
                #serializer.is_valid(raise_exception=True)
          """  
        #serializer = SearchNameorTweetsSerializer(data = all_details)
        #serializer.is_valid(raise_exception=True)
        
        """
                "main_video": {
                    "small":{
                        "bitrate": small_vid_bitrate,
                        "vidurl": small_vid_url,
                    },
                    "medium": {
                        "bitrate": medium_vid_bitrate,
                        "vidurl": medium_vid_url,
                    },
                    "large": {
                        "bitrate": large_vid_bitrate,
                        "vidurl": large_vid_url,
                    },
                    
                },  
            """
        #return Response(res)
        #return Response(res[0][0]["content"]["itemContent"]["tweet_results"]["result"]["legacy"]["in_reply_to_status_id_str"])
        #return Response(scraper.tweets_details([1673220010913800193]))
        #return Response(serializer)
        
        print("done")
        try:
            print(all_details[0])
            
        except:
            print("Can't print it")
            
        return Response(all_details)
        #return Response(scraper.tweets_details([1672281571905220611]))