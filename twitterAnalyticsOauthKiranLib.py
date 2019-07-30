import re
import pandas as pd
import requests
from flask import request
import urllib.parse as urlparse
import urllib
import httplib2
from oauth2client.client import _parse_exchange_token_response


class TwitterAnalyticsOauthKiranLib:
    def __init__(self):
        self.CONSUMER_KEY = "lOhkeJRZhYXvkm0lYq1ZgTtYa"
        self.CONSUMER_SECRET = "TbMKSZBbcqhnedjjqG66JuStxunBdKLelfjgxTW4UNJndbatJa"
        self.bearer_token_url = 'https://api.twitter.com/oauth2/token?'

    def get_bearer_token(self):
        params = urllib.parse.urlencode({
            'oauth_consumer_key': self.CONSUMER_KEY,
            'oauth_nonce': self.CONSUMER_SECRET,
            'grant_type': 'client_credentials'
        })
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        http = httplib2.Http()
        resp, content = http.request(self.bearer_token_url, method='POST', body=params, headers=headers)
        d = _parse_exchange_token_response(content)
        print(d)
        # access_token = ''
        # if resp.status == 200 and 'access_token' in d:
        #     access_token = d['access_token']
