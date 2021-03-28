import settings
from flask import Flask, request, Response, render_template,jsonify
from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl

class sessionManager:
    def __init__(self):
        self.cosumer_key = settings.CONSUMER_KEY
        self.cosumer_secret = settings.CONSUMER_SECRET
        print(self.cosumer_key)
        print(self.cosumer_secret)
        self.access_token = None
        self.access_secret = None

    def getConsumerKey(self):
        return self.cosumer_key, self.cosumer_secret

    def generateAccessToken(self,oauth_token, oauth_verifier):
        twitter = OAuth1Session(self.cosumer_key, self.cosumer_secret)
        access_endpoint = "https://api.twitter.com/oauth/access_token"
        response = twitter.post(access_endpoint, params={'oauth_token':oauth_token,'oauth_verifier':oauth_verifier})
        access_token_dict = dict(parse_qsl(response.content.decode('utf-8')))
        self.access_token = access_token_dict['oauth_token']
        self.access_secret = access_token_dict['oauth_token_secret']

    def getAllKey(self):
        return (self.cosumer_key, self.cosumer_secret, self.access_token, self.access_secret)