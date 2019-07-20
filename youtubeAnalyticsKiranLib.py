import re
import pandas as pd
import requests
from flask import request
import urllib.parse as urlparse
import urllib
import httplib2
from oauth2client.client import _parse_exchange_token_response


class YoutubeAnalyticsKiranLib:
    def __init__(self):
        self.client_id = '46170919280-a33nkabb4tq942j1c67ad93tf60v3p2m.apps.googleusercontent.com'
        self.client_secret = '_rKXdE9kRTN2vGYsF0pkrYcv'
        self.redirect_url = request.url_root + 'youtube_analytics_call_back_url'
        self.scope = 'https://www.googleapis.com/auth/yt-analytics-monetary.readonly'+' '+'https://www.googleapis.com/auth/yt-analytics.readonly'
        self.auth_url = 'https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=' + self.redirect_url + '&prompt=consent&response_type=code&client_id=' + self.client_id + '&scope=' + self.scope + '&access_type=offline'
        self.access_token_uri = 'https://accounts.google.com/o/oauth2/token'
        self.access_token=''
        self.refresh_token=''
        self.refresh_access_token_url = 'https://www.googleapis.com/oauth2/v4/token'


    def get_auth_url(self):
        return self.auth_url


    def get_access_token(self,call_back_url,user_id,add_credentials_url):
        parsed = urlparse.urlparse(call_back_url)
        auth_code = urlparse.parse_qs(parsed.query)['code']
        print(auth_code)
        access_token_uri = 'https://accounts.google.com/o/oauth2/token'
        # redirect_uri = "http://mysite/login/google/auth"
        params = urllib.parse.urlencode({
            'code': auth_code[0],
            'redirect_uri': self.redirect_url,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code'
        })
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        http = httplib2.Http()
        resp, content = http.request(access_token_uri, method='POST', body=params, headers=headers)
        d = _parse_exchange_token_response(content)
        print(d)
        if resp.status == 200 and 'access_token' in d:
            self.access_token = d['access_token']
            self.refresh_token = d.get('refresh_token', None)
            expires_in = d.get('expires_in')
            scope = d.get('scope')
            token_type = d.get('token_type')
            if self.access_token and self.refresh_token:
                json_post_data = {
                    'access_token': self.access_token,
                    'refresh_token': self.refresh_token,
                    'expires_in': expires_in,
                    'scope': scope,
                    'token_type': token_type
                }
                try:
                    print('i m inside try')
                    print(user_id)
                    response = requests.post(url=add_credentials_url, json=json_post_data)
                    print('added/updated credentials')
                except:
                    print('error while adding or updating credentials')
                    pass
        return self.access_token,self.refresh_token


    def refresh_access_token(self,refresh_token,user_id,add_credentials_url):
        params = urllib.parse.urlencode({
            'refresh_token': refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token'
        })
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        http = httplib2.Http()
        resp, content = http.request(self.refresh_access_token_url, method='POST', body=params, headers=headers)
        d = _parse_exchange_token_response(content)
        print(d)
        access_token=''
        if resp.status == 200 and 'access_token' in d:
            access_token = d['access_token']
            self.refresh_token = d.get('refresh_token', None)
            expires_in = d.get('expires_in')
            scope = d.get('scope')
            token_type = d.get('token_type')
            if self.access_token and self.refresh_token:
                json_post_data = {
                    'access_token': self.access_token,
                    'refresh_token': self.refresh_token,
                    'expires_in': expires_in,
                    'scope': scope,
                    'token_type': token_type
                }
                try:
                    print('i m inside try')
                    print(user_id)
                    response = requests.post(url=add_credentials_url, json=json_post_data)
                    print('added/updated credentials')
                except:
                    print('error while adding or updating credentials')
                    pass
            return access_token
        else:
            return access_token


    def get_view_ids(self,access_token):
        view_ids_url = 'https://www.googleapis.com/analytics/v3/management/accounts/~all/webproperties/~all/profiles?access_token=' + access_token
        response_view_ids = requests.get(url=view_ids_url)
        print(response_view_ids.json())
        response_view_ids_json = response_view_ids.json()
        view_ids = []
        for item in response_view_ids_json['items']:
            view_ids.append(item['id'])
        print(view_ids)
        return view_ids



    ''' function return the google analytics data for given dimension, metrics, start data, end data access token, type,goal number, condition'''
    def google_analytics_reporting_api_data_extraction(self,viewID, dim, met, start_date, end_date, refresh_token,
                                                       transaction_type, goal_number, condition,client_id,client_secret,access_token):
        viewID = viewID
        dim = dim
        met = met
        start_date = start_date
        end_date = end_date
        refresh_token = refresh_token
        access_token = access_token
        transaction_type = transaction_type
        condition = condition
        goal_number = goal_number
        viewID = "".join(['ga%3A', viewID])
        met1 = ''
        if transaction_type == "Goal":
            met1 = "%2C".join([re.sub(":", "%3A", i) for i in met]).replace("XX", str(goal_number))
        elif transaction_type == "Transaction":
            met1 = "%2C".join([re.sub(":", "%3A", i) for i in met])

        dim1 = "%2C".join([re.sub(":", "%3A", i) for i in dim])

        api_url = "https://www.googleapis.com/analytics/v3/data/ga?ids="

        url = "".join(
            [api_url, viewID, '&start-date=', start_date, '&end-date=', end_date, '&metrics=', met1, '&dimensions=',
             dim1, '&max-results=1000000', condition, '&access_token=', access_token])

        data = pd.DataFrame()

        try:
            r = requests.get(url)

            try:
                data = pd.DataFrame(list((r.json())['rows']), columns=[re.sub("ga:", "", i) for i in dim + met])
                data['date'] = start_date
                print("data extraction is successfully completed")

                return data
            except:
                print((r.json()))
        except:
            print((r.json()))
            print("error occured in the google analytics reporting api data extraction")
            return data


    def get_google_analytics_data(self,access_token,viewId):
        viewID=viewId
        dim=['ga:browser','ga:sourceMedium']
        met=['ga:users','ga:revenuePerTransaction','ga:newUsers']
        start_date='2019-07-01'
        end_date='2019-07-10'
        transaction_type='Transaction'
        goal_number=''
        condition='&sort=-ga%3Ausers' # sort the data set by users in descending order
        pd.set_option('display.width', 320)

        data= self.google_analytics_reporting_api_data_extraction(viewID,dim,met,start_date,end_date,self.refresh_token,
                                                                  transaction_type,goal_number,condition,
                                                                  client_id=self.client_id,client_secret=self.client_secret,access_token=access_token)
        print(type(data))
        # print(data)
        return data