# -*- coding:utf-8 -*-
from flask import Flask, request, Response, render_template
import json
import requests
import settings
from requests_oauthlib import OAuth1Session

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/searchTweet',methods=["POST"])
def getTweet():
    print('Enter getTweet')
    data = request.get_data().decode('utf-8')
    tmp,query = data.split('=')
    q = "q={}".format(query)
    lang = "lang=ja"
    result_type = "result_type=recent"
    count = "count=10"
    entities = "include_entities=true"

    twitter = OAuth1Session(settings.CONSUMER_KEY,settings.CONSUMER_SECRET,settings.ACCESS_TOKEN,settings.ACCESS_TOKEN_SECRET)
    endpoint = "https://api.twitter.com/1.1/search/tweets.json?{}&{}&{}&{}&{}".format(q,lang,result_type,count,entities)
    res = twitter.get(endpoint)
    json_response = res.json()
    print(json.dumps(json_response,indent=4,sort_keys=True,ensure_ascii=False))
    tweet_list = []
    for json_response in json_response['statuses']:
        tweet_dict = {}
        if json_response.get('retweeted_status') is not None:
            tweet_dict['retweet_username'] = json_response['user']['name']
            json_response = json_response['retweeted_status']

        tweet_dict['tweet_id'] = json_response['id_str']
        tweet_dict['username'] = json_response['user']['name']
        tweet_dict['userid'] = json_response['user']['id']
        tweet_dict['screen_name'] = json_response['user']['screen_name']
        tweet_dict['profile_image_url_https'] = json_response['user']['profile_image_url_https']
        tweet_dict['created_at'] = json_response['created_at']
        tweet_dict['text'] = json_response['text']

        if json_response.get('extended_entities') is not None:
            tweet_dict['media_list'] =json_response['extended_entities']['media']

        status = getStatus(tweet_dict['tweet_id'])
        tweet_dict['favorite_count'] = status['favorite_count']
        tweet_dict['favorited'] = status['favorited']
        tweet_dict['retweet_count'] = status['retweet_count']
        tweet_dict['retweeted'] = status['retweeted']
        tweet_dict['following'] = status['user']['following']
        tweet_list.append(tweet_dict)
    
    print("Exit getTweet")
    return render_template('searchTweet.html', tweet_list=tweet_list)

def getStatus(tweet_id):
    twitter = OAuth1Session(settings.CONSUMER_KEY,settings.CONSUMER_SECRET,settings.ACCESS_TOKEN,settings.ACCESS_TOKEN_SECRET)
    endpoint = "https://api.twitter.com/1.1/statuses/lookup.json?id={}".format(tweet_id)
    res = twitter.get(endpoint)
    json_res = res.json()
    return json_res[0]

@app.route('/favorites',methods=["POST"])
def setFavorites():
    print('Enter setFavorites')
    twitter = OAuth1Session(settings.CONSUMER_KEY,settings.CONSUMER_SECRET,settings.ACCESS_TOKEN,settings.ACCESS_TOKEN_SECRET)
    tweet_id = request.form.get('tweet_id')
    endpoint = "https://api.twitter.com/1.1/favorites/create.json?id={}".format(tweet_id)
    print(tweet_id)
    res = twitter.post(endpoint)
    json_res = res.json()
    print(json.dumps(json_res,indent=4,sort_keys=True,ensure_ascii=False))
    print('Exit setFavorites')
    status = getStatus(tweet_id)
    print(status)
    return status

@app.route('/favorites',methods=["DELETE"])
def deleteFavorites():
    print('Enter deleteFavorites')
    twitter = OAuth1Session(settings.CONSUMER_KEY,settings.CONSUMER_SECRET,settings.ACCESS_TOKEN,settings.ACCESS_TOKEN_SECRET)
    tweet_id = request.form.get('tweet_id')
    endpoint = "https://api.twitter.com/1.1/favorites/destroy.json?id={}".format(tweet_id)
    print(tweet_id)
    res = twitter.post(endpoint)
    json_res = res.json()
    print(json.dumps(json_res,indent=4,sort_keys=True,ensure_ascii=False))
    print('Exit deleteFavorites')
    status = getStatus(tweet_id)
    print(status)
    return status

@app.route('/retweet',methods=["POST"])
def setRetweet():
    print('Enter setRetweet')
    twitter = OAuth1Session(settings.CONSUMER_KEY,settings.CONSUMER_SECRET,settings.ACCESS_TOKEN,settings.ACCESS_TOKEN_SECRET)
    tweet_id = request.form.get('tweet_id')
    endpoint = "https://api.twitter.com/1.1/statuses/retweet/{}.json".format(tweet_id)
    print(endpoint)
    res = twitter.post(endpoint) 
    json_res = res.json()
    print(json.dumps(json_res,indent=4,sort_keys=True,ensure_ascii=False))
    print('Exit setRetweet')
    status = getStatus(tweet_id)
    print(status)
    return status

@app.route('/retweet',methods=["DELETE"])
def deleteRetweet():
    print('Enter deleteRetweet')
    twitter = OAuth1Session(settings.CONSUMER_KEY,settings.CONSUMER_SECRET,settings.ACCESS_TOKEN,settings.ACCESS_TOKEN_SECRET)
    tweet_id = request.form.get('tweet_id')
    endpoint = "https://api.twitter.com/1.1/statuses/unretweet/{}.json".format(tweet_id)
    print(endpoint)
    res = twitter.post(endpoint)
    json_res = res.json()
    print(json.dumps(json_res,indent=4,sort_keys=True,ensure_ascii=False))
    print('Exit deleteRetweet')
    status = getStatus(tweet_id)
    print(status)
    return status

@app.route('/friendship',methods=["POST"])
def setFollow():
    print('Enter setFollow')
    twitter = OAuth1Session(settings.CONSUMER_KEY,settings.CONSUMER_SECRET,settings.ACCESS_TOKEN,settings.ACCESS_TOKEN_SECRET)
    user_id = request.form.get('user_id')
    endpoint = "https://api.twitter.com/1.1/friendships/create.json?user_id={}".format(user_id)
    headers={"Content-Type":"application/json"}
    res = twitter.post(endpoint,headers=headers)
    json_res = res.json()
    print(json.dumps(json_res,indent=4,sort_keys=True,ensure_ascii=False))
    
    return json_res

@app.route('/friendship',methods=["DELETE"])
def deleteFollow():
    print('Enter setFollow')
    twitter = OAuth1Session(settings.CONSUMER_KEY,settings.CONSUMER_SECRET,settings.ACCESS_TOKEN,settings.ACCESS_TOKEN_SECRET)
    user_id = request.form.get('user_id')
    endpoint = "https://api.twitter.com/1.1/friendships/destroy.json?user_id={}".format(user_id)
    headers={"Content-Type":"application/json"}
    res = twitter.post(endpoint,headers=headers)
    json_res = res.json()
    print(json.dumps(json_res,indent=4,sort_keys=True,ensure_ascii=False))
    
    return json_res

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)