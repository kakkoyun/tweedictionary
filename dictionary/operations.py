from django.conf import settings
from urllib import urlencode
from urllib2 import urlopen
from dictionary.models import Entry
from django.shortcuts import get_object_or_404
import oauth2 as oauth
import twitter
import bitly

def send(request,entry_id):
    twitter_user = request.user.social_auth.get(provider='twitter')

    if not twitter_user.tokens:
        return

    access_token = twitter_user.tokens['oauth_token']
    access_token_secret = twitter_user.tokens['oauth_token_secret']

    #token = oauth.Token(access_token,access_token_secret)
    consumer_key = settings.TWITTER_CONSUMER_KEY
    consumer_secret = settings.TWITTER_CONSUMER_SECRET
    #consumer = oauth.Consumer(consumer_key,consumer_secret)
    #client = oauth.Client(consumer,token)

    api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
          access_token_key=access_token,
          access_token_secret=access_token_secret)

    twit = (get_object_or_404(Entry, id=entry_id).content)[:114] + "... " + shorten_url("http://www.tweedictionary.com/entry/%s" %entry_id)
    api.PostUpdate(twit)
    #twit = get_object_or_404(Entry, id=entry_id).content

def shorten_url(long_url):
    username = settings.BITLY_USERNAME
    password = settings.BITLY_PASSWORD
    api_key = settings.BITLY_API_KEY

    api = bitly.Api(login=username, apikey=api_key)
    short_url = api.shorten(long_url)
#    bitly_url = "https://api-ssl.bit.ly/v3/shorten?login=%s&apiKey=%s&longUrl=%s&format=txt" %(username, api_key, long_url)
#    short_url = urlopen(bitly_url).read()
    return short_url

#API Address: https://api-ssl.bitly.com
#GET /v3/shorten?access_token=ACCESS_TOKEN&longUrl=http%3A%2F%2Fgoogle.com%2F
