import datetime
import http
import re
import urllib
from functools import wraps
import json
from io import StringIO
import csv
import time
#
import copy

import parser

import httplib2
import requests
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, jsonify, make_response,abort
from itsdangerous import URLSafeSerializer, BadSignature
# from model.ConnecsiModel import ConnecsiModel
# from passlib.hash import sha256_crypt
#from flask_oauthlib.client import OAuth
import os
# from flask_paginate import Pagination, get_page_parameter
from flask_uploads import UploadSet, configure_uploads, IMAGES
from configparser import ConfigParser

import urllib.parse as urlparse

from oauth2client.client import _parse_exchange_token_response
import pandas as pd
import  stripe


connecsiApp = Flask(__name__)
connecsiApp.secret_key = 'connecsiSecretKey'
config = ConfigParser()
dir_path = os.path.dirname(os.path.realpath(__file__))
# ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
config.read(dir_path+'/config.ini')
base_url = config.get('auth', 'base_url')
# base_url = 'https://kiranpadwaltestconnecsi.pythonanywhere.com/Apis/'




photos = UploadSet('photos', IMAGES)
campaign_files = UploadSet('campaignfiles')
brands_classified_files = UploadSet('brandsclassifiedfiles', IMAGES)
offer_files = UploadSet('offerfiles', IMAGES)
message_files = UploadSet('messagefiles', IMAGES)
message_agreements = UploadSet('messageagreements',('pdf', 'docx'))

# ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
# print(ROOT_DIR+'\\static\\img')

# print(os.getcwd()+'\\brands_profile_img')

connecsiApp.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
connecsiApp.config['UPLOADED_CAMPAIGNFILES_DEST'] = 'static/campaign_files'
connecsiApp.config['UPLOADED_BRANDSCLASSIFIEDFILES_DEST'] = 'static/brands_classified_files'
connecsiApp.config['UPLOADED_OFFERFILES_DEST'] = 'static/offer_files'
connecsiApp.config['UPLOADED_MESSAGEFILES_DEST'] = 'static/message_files'
connecsiApp.config['UPLOADED_MESSAGEAGREEMENTS_DEST'] = 'static/message_agreements'



configure_uploads(connecsiApp, photos)
configure_uploads(connecsiApp, campaign_files)
configure_uploads(connecsiApp, brands_classified_files)
configure_uploads(connecsiApp, offer_files)
configure_uploads(connecsiApp, message_files)
configure_uploads(connecsiApp, message_agreements)


# oauth = OAuth(connecsiApp)

# linkedin = oauth.remote_app(
#     'linkedin',
#     consumer_key='86ctp4ayian53w',
#     consumer_secret='3fdovLJRbWrQuu3u',
#     request_token_params={
#         'scope': 'r_basicprofile,r_emailaddress',
#         'state': 'RandomString',
#     },
#     base_url='https://api.linkedin.com/v1/',
#     request_token_url=None,
#     access_token_method='POST',
#     access_token_url='https://www.linkedin.com/uas/oauth2/accessToken',
#     authorize_url='https://www.linkedin.com/uas/oauth2/authorization',
# )

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('Unauthorized, Please login','danger')
            return redirect(url_for('index'))
    return wrap


@connecsiApp.route('/')
# @is_logged_in
def index():
    title='Connesi App Login Panel'
    data=[]
    data.append(title)
    return render_template('user/login.html',data=data)


@connecsiApp.route('/privacy_policy')
def privacy_policy():
    return render_template('user/privacy_policy.html')

@connecsiApp.route('/terms_use')
def terms_use():
    return render_template('user/terms_use.html')

# @connecsiApp.route('/loginLinkedin')
# def loginLinkedin():
#     return linkedin.authorize(callback=url_for('authorized', _external=True))

@connecsiApp.route('/registerBrand')
def registerBrand():
    return render_template('user/registerFormBrand.html')


@connecsiApp.route('/forgotPassword')
def forgotPassword():
    return render_template('user/forgotPassword.html')

@connecsiApp.route('/resetemail', methods=['GET','POST'])
def resetemail():
    if request.method == 'POST':
        payload = request.form.to_dict()
        email_id = payload.get('reset_email')
        url = base_url + '/Messages/ForgotPassword/' + str(email_id)
        # print(payload)
        try:
            response = requests.post(url, json=payload)
            print(response.json())
            print('email sent')
        except:
            pass
        flash("Email sent successfully", 'success')
        return render_template("user/login.html")


@connecsiApp.route('/saveBrand',methods=['GET','POST'])
def saveBrand():
    if request.method == 'POST':
        url = base_url+'Brand/register'
        payload = request.form.to_dict()
        print(payload)
        del payload['confirm_password']
        print(payload)
        title = 'Connesi App Login Panel'
        try:
            response = requests.post(url, json=payload)
            print(response.json())
            result_json = response.json()
            print(result_json['response'])
            result = result_json['response']
            # exit()
            if result == 1:
                user = {'email_id': payload['email']}
                activation_link = get_activation_link(user=user)
                print(activation_link)
                email_content = welcomemail(activation_link=activation_link)
                payload1 = {
                  "from_email_id": "business@connecsi.com",
                  "to_email_id": request.form.get('email'),
                  "date": datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"),
                  "subject": "Welcome To Connecsi",
                  # "message": "Please click "+activation_link+" to activate your account"
                  "message": "'"+email_content+"'"
                }
                user_id = 1
                type = 'brand'
                url = base_url + 'Messages/sentWelcomeEmail/' + str(user_id) + '/' + type
                try:
                    response = requests.post(url=url, json=payload1)
                    data = response.json()
                    print('email sent')
                except:
                    pass
                flash("Successfully Registered and Activation link has been sent to your email address", 'success')
                title = 'Connesi App Login Panel'
                return render_template('user/login.html', title=title)
            else:
                flash("Internal error please try later", 'danger')
                return render_template('user/login.html', title=title)
        except:
            flash("Internal error please try later", 'danger')
            return render_template('user/registerFormBrand.html',title='Register Brand')
#
#
#
# @connecsiApp.route('/welcomemail')
def welcomemail(activation_link):
    resp_template = render_template('brand_activation_link_template.html',activation_link=activation_link)
    # print(resp_template)
    return resp_template
    # return render_template('brand_activation_link_template.html',activation_link=activation_link)


# @connecsiApp.route('/welcomemail_inf')
def welcomemail_inf():
    resp_template = render_template('welcomemail_inf_template.html')
    # print(resp_template)
    return resp_template
    # return render_template('brand_activation_link_template.html',activation_link=activation_link)


def email_temp_from_brands_to_inf(message_id):
    resp_template = render_template('message_template_from_brands_to_inf.html',message_id=message_id)
    # print(resp_template)
    return resp_template


def get_serializer(secret_key=None):
    if secret_key is None:
        secret_key = connecsiApp.secret_key
    return URLSafeSerializer(secret_key)

@connecsiApp.route('/users/activate/<payload>')
def activate_user(payload):
    s = get_serializer()
    email_id=''
    try:
        email_id = s.loads(payload)
        print(email_id)
    except BadSignature:
        abort(404)
    activate_user_url = base_url+'Brand/Confirm_email/'+str(email_id)
    requests.post(url=activate_user_url)
    flash('Brand User with '+email_id+' is Activated now you can login','success')
    return redirect(url_for('index'))

def get_activation_link(user):
    s = get_serializer()
    payload = s.dumps(user['email_id'])
    print('payload = ',payload)
    return url_for('activate_user', payload=payload, _external=True)

# @connecsiApp.route('/test_activate_user')
# def test_activate_user():
#     user = {'id':'123'}
#     activation_link = get_activation_link(user=user)
#     print('activation_link =',activation_link)
#     return activation_link

#Logout
@connecsiApp.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('index'))

#
# # User login
# @connecsiApp.route('/login',methods=['POST'])
# def login():
#     if request.method=='POST':
#         if 'brand' in request.form:
#             url = base_url + 'User/login'
#             payload = request.form.to_dict()
#             print(payload)
#             del payload['brand']
#             print(payload)
#             title = ''
#             try:
#                 response = requests.post(url, json=payload)
#                 print('user response =',response.json())
#                 result_json = response.json()
#                 user_id = result_json['user_id']
#                 confirmed_email = result_json['confirmed_email']
#                 print('confirmed email = ',confirmed_email)
#                 print(user_id)
#                 # exit()
#                 if user_id:
#                     if confirmed_email =='confirmed':
#                         flash("logged in", 'success')
#                         session['logged_in'] = True
#                         session['email_id']=payload.get('email')
#                         session['type'] = 'brand'
#                         session['user_id']=user_id
#                         print(session['user_id'])
#                         return redirect(url_for('admin'))
#                     else:
#                         flash("You have not Activated your account, To Activate your account please click on the activation link sent to your email address", 'danger')
#                         return render_template('user/login.html', title=title)
#
#                 else:
#                     flash("Internal error please try later", 'danger')
#                     return render_template('user/login.html', title=title)
#             except:
#                 flash("Internal error please try later", 'danger')
#                 return render_template('user/login.html', title='Login')
#         elif 'influencer' in request.form:
#             email_id = request.form.get('inf_username')
#             password = request.form.get('inf_password')
#             print(email_id)
#             print(password)

@connecsiApp.route('/login',methods=['POST'])
def login():
    if request.method=='POST':
        if 'brand' in request.form:
            url = base_url + 'User/login'
            payload = request.form.to_dict()
            print(payload)
            del payload['brand']
            print(payload)
            title = ''
            try:
                response = requests.post(url, json=payload)
                print('user response =',response.json())
                result_json = response.json()
                user_id = result_json['user_id']
                response2=getSubscriptionValues(str(user_id))
                print('hello response',response2,response2['data'])
                if(not len(response2['data'])):
                    #adding free subscription for first login Free
                    check=freeSubscription(str(user_id))
                    if(check['response']==1):
                        print("free package ADDED")
                    else:
                        print("free package NOT added")
                confirmed_email = result_json['confirmed_email']
                print('confirmed email = ',confirmed_email)
                print(user_id)
                # exit()
                if user_id:
                    if confirmed_email =='confirmed':
                        flash("logged in", 'success')
                        session['logged_in'] = True
                        session['email_id']=payload.get('email')
                        session['type'] = 'brand'
                        session['user_id']=user_id
                        print(session['user_id'])
                        return redirect(url_for('admin'))
                    else:
                        flash("You have not Activated your account, To Activate your account please click on the activation link sent to your email address", 'danger')
                        return render_template('user/login.html', title=title)

                else:
                    flash("Internal error please try later", 'danger')
                    return render_template('user/login.html', title=title)
            except:
                flash("Internal error please try later", 'danger')
                return render_template('user/login.html', title='Login')
        elif 'influencer' in request.form:
            email_id = request.form.get('inf_username')
            password = request.form.get('inf_password')
            print(email_id)
            print(password)



@connecsiApp.route('/admin')
@is_logged_in
def admin():
    title='Dashboard'
    top10Inf_url = base_url + 'Youtube/top10Influencers'

    try:
        response = requests.get(top10Inf_url)
        # print(response.json())
        top10Inf = response.json()
        print(top10Inf)
        # for item in top10Inf['data']:
        #     # print(item)
        #     # print(item['channel_id'])
        #     total_videos_url = base_url + 'Youtube/totalVideos/'+str(item['channel_id'])
        #     try:
        #         response = requests.get(total_videos_url)
        #         total_videos = response.json()
        #         # print(total_videos)
        #         for item1 in total_videos['data']:
        #             # print(item1)
        #             item.update(item1)
        #
        #     except:pass
        #     print(item)

        user_id = session['user_id']
        from templates.campaign.campaign import Campaign
        campaignObj = Campaign(user_id=user_id)
        # campaignObj = templates.campaign.campaign.Campaign(user_id=user_id)
        view_campaign_data = campaignObj.get_all_campaigns()
        view_campaign_data_list = []
        for item in view_campaign_data['data']:
            if item['deleted'] != 'true':
                view_campaign_data_list.append(item)
        # print(view_campaign_data_list)
        for item1 in view_campaign_data_list:
            campaign_id = item1['campaign_id']
            channel_status_campaign = requests.get(
                url=base_url + 'Campaign/channel_status_for_campaign_by_campaign_id/' + str(campaign_id))
            # print(channel_status_campaign.json())
            channel_status_campaign_json = channel_status_campaign.json()
            try:
                item1.update({'status': channel_status_campaign_json['data'][0]['status']})
            except:
                item1.update({'status': ''})
                pass
        print('final campaign list with status = ',view_campaign_data_list)
        return render_template('index.html', title=title, top10Inf=top10Inf)
    except Exception as e:
        print(e)

#
#
@connecsiApp.route('/getTop20Influencers/<string:channel_name>',methods=['GET'])
@is_logged_in
def getTop20Influencers(channel_name):
       try:
           url = base_url + 'Youtube/searchChannels/' + channel_name
           payload = {"channel": channel_name, "category_id": "", "country": "", "min_lower": 0, "max_upper": 100000000,
                      "sort_order": "High To Low",
                      "offset": 0
                      }
           response = requests.post(url=url,json=payload)

           response_json = response.json()
           if(channel_name=="Youtube"):
               for item in response_json['data']:
                   url= base_url + 'Youtube/totalVideos/' + str(item['channel_id'])
                   totalVideos=requests.get(url=url)
                   totalVideos=totalVideos.json()
                   print (totalVideos)
                   item.update({'totalVideos':totalVideos['data'][0]['total_videos']})

           elif (channel_name == "Twitter"):
               for item in response_json['data']:
                   item.update({'totalVideos':100})
           elif (channel_name == "Instagram"):
               for item in response_json['data']:
                   item.update({'totalVideos': 100})

           print (response_json['data'])
           return jsonify(results=response_json['data'])
       except Exception as e:
           print(e)
           return e


# @connecsiApp.route('/profileView')
# @is_logged_in
# def profileView():
#     title='Profile View'
#     type = session['type']
#     user_id = session['user_id']
#     if type == 'brand':
#         url = base_url + 'Brand/'+str(user_id)
#         try:
#             response = requests.get(url)
#             # print(response.json())
#             data_json = response.json()
#             print(data_json)
#             return render_template('user/user-profile-page.html', data=data_json, title=title)
#         except Exception as e:
#             print(e)
#     else:
#         table_name = 'users_inf'



@connecsiApp.route('/profileView')
@is_logged_in
def profileView():
    title='Profile View'
    type = session['type']
    user_id = session['user_id']
    allValue=getSubscriptionValues(str(user_id))
    subscriptionData=allValue
    subType=allValue['data'][0]['package_name']
    if type == 'brand':
        url = base_url + 'Brand/'+str(user_id)
        try:
            response = requests.get(url)
            # print(response.json())
            data_json = response.json()
            print(data_json)
            return render_template('user/user-profile-page.html', subscriptionData=subscriptionData,type=subType,data=data_json, title=title)
        except Exception as e:
            print(e)
    else:
        table_name = 'users_inf'


@connecsiApp.route('/editProfile')
@is_logged_in
def editProfile():
    title='Edit Profile'
    type = session['type']
    user_id = session['user_id']
    if type == 'brand':
        url = base_url + 'Brand/'+str(user_id)
        try:
            response = requests.get(url)
            # print(response.json())
            data_json = response.json()
            print(data_json)
            return render_template('user/edit-profile-page.html', data=data_json, title=title)
        except Exception as e:
            print(e)
    else:
        table_name = 'users_inf'

@connecsiApp.route('/updateProfile',methods=['GET','POST'])
@is_logged_in
def updateProfile():
    user_id = session['user_id']
    if request.method == 'POST':
        url = base_url+ 'Brand/'+str(user_id)
        payload = request.form.to_dict()
        print(payload)
        try:
            response = requests.put(url=url,json=payload)
            result_json = response.json()
            # return redirect(url_for('/profileView'))
            flash('Successfully Updated Profile Data','success')
            return profileView()
        except:pass


@connecsiApp.route('/uploadProfilePic',methods=['GET','POST'])
@is_logged_in
def uploadProfilePic():
    user_id = session['user_id']
    if request.method == 'POST' and 'profile_pic' in request.files:
        filename = photos.save(request.files['profile_pic'])
        url = base_url + 'Brand/updateProfilePic/' + str(user_id)
        payload = {}
        payload.update({'profile_pic':filename})
        print(payload)
        try:
            response = requests.put(url=url, json=payload)
            result_json = response.json()
            # return redirect(url_for('/profileView'))
            flash('Successfully Updated Profile Pic', 'success')
            return editProfile()
        except:
            pass


@connecsiApp.route('/changePassword',methods=['POST'])
@is_logged_in
def changePassword():
    user_id=session['user_id']
    if request.method == 'POST':
        url = base_url+ 'Brand/changePassword/'+str(user_id)
        payload = request.form.to_dict()
        # print(payload)
        del payload['con_new_password']
        # print(payload)
        try:
            response = requests.put(url=url,json=payload)
            result_json = response.json()
            # return redirect(url_for('/profileView'))
            flash('Password Updated','success')
            return profileView()
        except:pass



# @connecsiApp.route('/searchInfluencers',methods=['POST','GET'])
# @is_logged_in
# def searchInfluencers():
#     start = time.time()
#     user_id = session['user_id']
#     url_regionCodes = base_url + 'Youtube/regionCodes'
#     url_videoCat = base_url + 'Youtube/videoCategories'
#     regionCodes_json=''
#     videoCat_json=''
#     form_filters=''
#     country_name=''
#     view_campaign_data=''
#     data=''
#     favInfList_data=''
#     try:
#         response_regionCodes = requests.get(url=url_regionCodes)
#         regionCodes_json = response_regionCodes.json()
#     except Exception as e:
#         print(e)
#     try:
#         response_videoCat = requests.get(url=url_videoCat)
#         videoCat_json = response_videoCat.json()
#     except Exception as e:
#         print(e)
#
#     lookup_string = ''
#     for cat in videoCat_json['data']:
#         lookup_string += ''.join(',' + cat['video_cat_name'])
#     # lookup_string = lookup_string.replace('&', 'and')
#
#     print('before getting campaigns')
#     from templates.campaign import campaign
#     campaignObj = campaign.Campaign(user_id=user_id)
#     view_campaign_data = campaignObj.get_all_campaigns()
#     for item in view_campaign_data['data']:
#         if item['deleted']=='true':
#             view_campaign_data['data'].remove(item)
#
#     print('after getting campaigns')
#     print(view_campaign_data)
#     try:
#         url = base_url + '/Brand/getInfluencerFavList/' + str(user_id)
#         response = requests.get(url=url)
#         favInfList_data = response.json()
#         linechart_id = 1
#         for item in favInfList_data['data']:
#             item.update({'linechart_id': linechart_id})
#             linechart_id += 1
#     except Exception as e:
#         print(e)
#         pass
#     ###### POST METHOD#######
#     print('before POST METHOD')
#     if request.method == 'POST':
#         print('i m inside POST METHOD')
#         string_word = request.form.get('string_word')
#         category = string_word.replace('and','&')
#         sort_order = request.form.get('sort_order')
#         print(sort_order)
#         print(category)
#         category_id=''
#         for cat in videoCat_json['data']:
#             if cat['video_cat_name'] == category:
#                 print("category id = ",cat['video_cat_id'])
#                 category_id = cat['video_cat_id']
#
#         form_filters = request.form.to_dict()
#         print('post form filters =',form_filters)
#         if form_filters['country']:
#             url_country_name = base_url + 'Youtube/regionCode/'+form_filters['country']
#             try:
#                 response_country_name = requests.get(url=url_country_name)
#                 country_name_json = response_country_name.json()
#                 print(country_name_json['data'][0][1])
#                 country_name = country_name_json['data'][0][1]
#             except Exception as e:
#                 print(e)
#             form_filters.update({'country_name':country_name})
#         print('final form filters = ',form_filters)
#
#         payload = request.form.to_dict()
#         payload.update({'category_id': str(category_id)})
#         payload.update({'min_lower':payload.get('min_lower')})
#         payload.update({'max_upper':payload.get('max_upper')})
#
#         try:
#             if form_filters['offset']:
#                 payload.update({'offset':int(form_filters['offset'])})
#             else:
#                  payload.update({'offset': 0})
#                  print('i m in else no offset set')
#         except:
#                payload.update({'offset': 0})
#                pass
#
#         print('payload form filter = ',payload)
#
#         try:
#             channel = request.form.get('channel')
#             print('channel name = ',channel)
#             url = base_url+'Youtube/searchChannels/'+channel
#             print(url)
#             # del payload['channel']
#             # del payload['string_word']
#             print(payload)
#             response = requests.post(url, json=payload)
#             print(response.json())
#             data = response.json()
#             linechart_id=1
#             for item in data['data']:
#                 item.update({'linechart_id':linechart_id})
#                # print(item)
#                 linechart_id+=1
#             # try:
#             #     exportCsv(data=data)
#             # except Exception as e:
#             #     print(e)
#             #     pass
#             if form_filters['channel']=='Twitter':
#                 for item in data['data']:
#                     item.update({'total_videos':100})
#                     # total_videos_url = base_url + 'Youtube/totalVideos/' + str(item['channel_id'])
#                     # try:
#                     #     response = requests.get(total_videos_url)
#                     #     total_videos = response.json()
#                     #     for item1 in total_videos['data']:
#                     #         item.update(item1)
#                         # print(item)
#                     # except:
#                     #     pass
#             if form_filters['channel'] == 'Youtube':
#                 for item in data['data']:
#                     total_videos_url = base_url + 'Youtube/totalVideos/' + str(item['channel_id'])
#                     try:
#                         response = requests.get(total_videos_url)
#                         total_videos = response.json()
#                         for item1 in total_videos['data']:
#                             item.update(item1)
#                         print(item)
#                     except:
#                         pass
#             if form_filters['channel']=='Instagram':
#                 for item in data['data']:
#                     item.update({'total_videos':100})
#                     # total_videos_url = base_url + 'Youtube/totalVideos/' + str(item['channel_id'])
#                     # try:
#                     #     response = requests.get(total_videos_url)
#                     #     total_videos = response.json()
#                     #     for item1 in total_videos['data']:
#                     #         item.update(item1)
#                         # print(item)
#                     # except:
#                     #     pass
#             # print(data)
#             return render_template('search/searchInfluencers.html', regionCodes=regionCodes_json,
#                                    lookup_string=lookup_string, form_filters=form_filters,data=data,view_campaign_data=view_campaign_data
#                                    ,favInfList_data=favInfList_data,payload_form_filter=payload)
#         except Exception as e:
#             print(e)
#             print('i m hee')
#             return render_template('search/searchInfluencers.html', regionCodes=regionCodes_json,
#                                lookup_string=lookup_string,form_filters=form_filters,data=data,view_campaign_data=view_campaign_data
#                                    ,favInfList_data=favInfList_data,payload_form_filter=payload)
#
#
#     else:
#         print('Not POST METHOD')
#         payload = {"channel":"Youtube","category_id": "","country": "US","min_lower": 0,"max_upper": 100000000,"sort_order": "High To Low",
#             "offset": 0
#         }
#         try:
#             url = base_url + '/Youtube/searchChannels/youtube'
#             response = requests.post(url, json=payload)
#             print(response.json())
#             data = response.json()
#             linechart_id = 1
#             for item in data['data']:
#                 item.update({'linechart_id': linechart_id})
#                 # print(item)
#                 linechart_id += 1
#             form_filters = {'channel': 'Youtube', 'string_word': '', 'country': 'US', 'min_lower': '0', 'max_upper': '100000000', 'sort_order': 'High To Low', 'country_name': 'Poland'}
#         except:
#             pass
#
#         # try:
#         #     exportCsv(data=data)
#         # except Exception as e:
#         #     print(e)
#         #     pass
#         print('I M HERE BEFORE GETTING TOTAL VIDEOS')
#         for item in data['data']:
#             total_videos_url = base_url + 'Youtube/totalVideos/' + str(item['channel_id'])
#             try:
#                 response = requests.get(total_videos_url)
#                 total_videos = response.json()
#                 for item1 in total_videos['data']:
#                     item.update(item1)
#                 # print(item)
#             except:
#                 pass
#         end = time.time()
#         print(end - start)
#         return render_template('search/searchInfluencers.html', regionCodes=regionCodes_json,
#                                lookup_string=lookup_string,form_filters=form_filters,data=data,pagination='',view_campaign_data=view_campaign_data,
#                                favInfList_data=favInfList_data,payload_form_filter=payload)




@connecsiApp.route('/searchInfluencers',methods=['POST','GET'])
@is_logged_in
def searchInfluencers():
    start = time.time()
    user_id = session['user_id']
    url_regionCodes = base_url + 'Youtube/regionCodes'
    url_videoCat = base_url + 'Youtube/videoCategories'
    regionCodes_json=''
    videoCat_json=''
    form_filters=''
    country_name=''
    subValues=getSubscriptionValues(str(user_id))
    countExportList=0
    packageName=''
    countAddToFavorites=0
    countAlerts=0
    countMessages=0
    messageSubscription={
        'Export Lists':'',
        'Add to Favorites':'',
        'Alerts':'',
        'Messages':''
    }
    for i in subValues['data']:
        print(i['feature_name'])
        if(i['feature_name'].lower()=='export lists'):
            countExportList=i['units']
            packageName=i['package_name']
            messageSubscription['Export Lists'] = 'Your have less Export Lists units than the influencers in current export List. Add more in custom or upgrade your ' + packageName + ' package.'
        if(i['feature_name'].lower()=='add to favorites'):
            countAddToFavorites=i['units']
            messageSubscription['Add to Favorites'] = ''
        if(i['feature_name'].lower()=='alerts'):
            countAlerts=i['units']
            messageSubscription['Alerts']=''
        if (i['feature_name'].lower() == 'messages'):
            countMessages = i['units']
            messageSubscription['Messages'] = ''

    if(countMessages==-1):
        messageSubscription['Messages']="Your "+packageName+" package doesn't have this feature. Please Upgrade your subscription to use this feature."
    elif(countMessages==0):
        messageSubscription['Messages']="You ran out of Messages feature of "+packageName+" package. PLease add more in custom or upgrade your subscription."

    if (countExportList == 0):
        messageSubscription[
            'Export Lists'] = "You ran out of Export Lists feature of " + packageName + " package. PLease add more in custom or upgrade your subscription."

    if(countAddToFavorites==0):
        messageSubscription['Add to Favorites']="You ran out of Add to Favorites feature of "+packageName+" package. PLease add more in custom or upgrade your subscription."

    if(countAlerts==-1):
        messageSubscription['Alerts']="Your "+packageName+" package doesn't have this feature. Please Upgrade your subscription to use this feature."
    elif(countAlerts==0):
        messageSubscription['Alerts']="You ran out of Alerts(Milestone Based) feature of "+packageName+" package. PLease add more in custom or upgrade your subscription."

    view_campaign_data=''
    data=''
    favInfList_data=''
    try:
        response_regionCodes = requests.get(url=url_regionCodes)
        regionCodes_json = response_regionCodes.json()
    except Exception as e:
        print(e)
    try:
        response_videoCat = requests.get(url=url_videoCat)
        videoCat_json = response_videoCat.json()
    except Exception as e:
        print(e)

    lookup_string = ''
    for cat in videoCat_json['data']:
        lookup_string += ''.join(',' + cat['video_cat_name'])
    # lookup_string = lookup_string.replace('&', 'and')

    print('before getting campaigns')
    from templates.campaign import campaign
    campaignObj = campaign.Campaign(user_id=user_id)
    view_campaign_data = campaignObj.get_all_campaigns()
    for item in view_campaign_data['data']:
        if item['deleted']=='true':
            view_campaign_data['data'].remove(item)

    print('after getting campaigns')
    print(view_campaign_data)
    try:
        url = base_url + '/Brand/getInfluencerFavList/' + str(user_id)
        response = requests.get(url=url)
        favInfList_data = response.json()
        linechart_id = 1
        for item in favInfList_data['data']:
            item.update({'linechart_id': linechart_id})
            linechart_id += 1
    except Exception as e:
        print(e)
        pass
    ###### POST METHOD#######
    print('before POST METHOD')
    if request.method == 'POST':
        print('i m inside POST METHOD')
        string_word = request.form.get('string_word')
        category = string_word.replace('and','&')
        sort_order = request.form.get('sort_order')
        print(sort_order)
        print(category)
        category_id=''
        for cat in videoCat_json['data']:
            if cat['video_cat_name'] == category:
                print("category id = ",cat['video_cat_id'])
                category_id = cat['video_cat_id']

        form_filters = request.form.to_dict()
        print('post form filters =',form_filters)
        if form_filters['country']:
            url_country_name = base_url + 'Youtube/regionCode/'+form_filters['country']
            try:
                response_country_name = requests.get(url=url_country_name)
                country_name_json = response_country_name.json()
                print(country_name_json['data'][0][1])
                country_name = country_name_json['data'][0][1]
            except Exception as e:
                print(e)
            form_filters.update({'country_name':country_name})
        print('final form filters = ',form_filters)

        payload = request.form.to_dict()
        payload.update({'category_id': str(category_id)})
        payload.update({'min_lower':payload.get('min_lower')})
        payload.update({'max_upper':payload.get('max_upper')})

        try:
            if form_filters['offset']:
                payload.update({'offset':int(form_filters['offset'])})
            else:
                 payload.update({'offset': 0})
                 print('i m in else no offset set')
        except:
               payload.update({'offset': 0})
               pass

        print('payload form filter = ',payload)

        try:
            channel = request.form.get('channel')
            print('channel name = ',channel)
            url = base_url+'Youtube/searchChannels/'+channel
            print(url)
            # del payload['channel']
            # del payload['string_word']
            print(payload)
            response = requests.post(url, json=payload)
            print(response.json())
            data = response.json()
            linechart_id=1
            for item in data['data']:
                item.update({'linechart_id':linechart_id})
               # print(item)
                linechart_id+=1
            # try:
            #     exportCsv(data=data)
            # except Exception as e:
            #     print(e)
            #     pass
            if form_filters['channel']=='Twitter':
                for item in data['data']:
                    item.update({'total_videos':100})
                    # total_videos_url = base_url + 'Youtube/totalVideos/' + str(item['channel_id'])
                    # try:
                    #     response = requests.get(total_videos_url)
                    #     total_videos = response.json()
                    #     for item1 in total_videos['data']:
                    #         item.update(item1)
                        # print(item)
                    # except:
                    #     pass
            if form_filters['channel'] == 'Youtube':
                for item in data['data']:
                    total_videos_url = base_url + 'Youtube/totalVideos/' + str(item['channel_id'])
                    try:
                        response = requests.get(total_videos_url)
                        total_videos = response.json()
                        for item1 in total_videos['data']:
                            item.update(item1)
                        print(item)
                    except:
                        pass
            if form_filters['channel']=='Instagram':
                for item in data['data']:
                    item.update({'total_videos':100})
                    # total_videos_url = base_url + 'Youtube/totalVideos/' + str(item['channel_id'])
                    # try:
                    #     response = requests.get(total_videos_url)
                    #     total_videos = response.json()
                    #     for item1 in total_videos['data']:
                    #         item.update(item1)
                        # print(item)
                    # except:
                    #     pass
            # print(data)
            return render_template('search/searchInfluencers.html', countMessages=countMessages,packageName=packageName,countAlerts=countAlerts,countAddToFavorites=countAddToFavorites,messageSubscription=messageSubscription,countExportList=countExportList,regionCodes=regionCodes_json,
                                   lookup_string=lookup_string, form_filters=form_filters,data=data,view_campaign_data=view_campaign_data
                                   ,favInfList_data=favInfList_data,payload_form_filter=payload)
        except Exception as e:
            print(e)
            print('i m hee')
            return render_template('search/searchInfluencers.html',countMessages=countMessages,packageName=packageName,countAlerts=countAlerts,countAddToFavorites=countAddToFavorites, messageSubscription=messageSubscription,countExportList=countExportList,regionCodes=regionCodes_json,
                               lookup_string=lookup_string,form_filters=form_filters,data=data,view_campaign_data=view_campaign_data
                                   ,favInfList_data=favInfList_data,payload_form_filter=payload)


    else:
        print('Not POST METHOD')
        payload = {"channel":"Youtube","category_id": "","country": "US","min_lower": 0,"max_upper": 100000000,"sort_order": "High To Low",
            "offset": 0
        }
        try:
            url = base_url + '/Youtube/searchChannels/youtube'
            response = requests.post(url, json=payload)
            print(response.json())
            data = response.json()
            linechart_id = 1
            for item in data['data']:
                item.update({'linechart_id': linechart_id})
                # print(item)
                linechart_id += 1
            form_filters = {'channel': 'Youtube', 'string_word': '', 'country': 'US', 'min_lower': '0', 'max_upper': '100000000', 'sort_order': 'High To Low', 'country_name': 'Poland'}
        except:
            pass

        # try:
        #     exportCsv(data=data)
        # except Exception as e:
        #     print(e)
        #     pass
        print('I M HERE BEFORE GETTING TOTAL VIDEOS')
        for item in data['data']:
            total_videos_url = base_url + 'Youtube/totalVideos/' + str(item['channel_id'])
            try:
                response = requests.get(total_videos_url)
                total_videos = response.json()
                for item1 in total_videos['data']:
                    item.update(item1)
                # print(item)
            except:
                pass
        end = time.time()
        print(end - start)
        return render_template('search/searchInfluencers.html',packageName=packageName,countMessages=countMessages,countAlerts=countAlerts,countAddToFavorites=countAddToFavorites, messageSubscription=messageSubscription,countExportList=countExportList,regionCodes=regionCodes_json,
                               lookup_string=lookup_string,form_filters=form_filters,data=data,pagination='',view_campaign_data=view_campaign_data,
                               favInfList_data=favInfList_data,payload_form_filter=payload)



#
@connecsiApp.route('/addFundsBrands')
@is_logged_in
def addFundsBrands():
    return render_template('user/add_funds.html')


@connecsiApp.route('/saveFundsBrands',methods=['POST'])
@is_logged_in
def saveFundsBrands():
    if request.method == 'POST':
       payload = request.form.to_dict()
       print(payload)
       user_id = session['user_id']
       url = base_url+'Payments/'+str(user_id)
       try:
           response = requests.post(url=url, json=payload)
           result_json = response.json()
           flash('saved funds','success')
           return viewMyPayments()
       except:
           pass
    else:
        flash('No Funds added','danger')
        return redirect(url_for('addFundsBrands'))



@connecsiApp.route('/payment',methods=['POST'])
@is_logged_in
def payment():
    print(request.form.to_dict())
    data=request.form.to_dict()
    pub_key = 'pk_test_KCfQnVzaUJoSOE8Yk3B8qvGM00rakAIYnH'
    secret_key = 'sk_test_4YZbWgXJul77g819JY5REXLL005jjbeXaG'
    amount=0
    if(data['package_name']=='Custom'):
        amount = data['price1']
    elif (data['package_name'] == 'Basic'):
        amount = data['price2']
    elif (data['package_name'] == 'Professional'):
        amount = data['price3']
    elif (data['package_name'] == 'Enterprise'):
        amount = data['price4']
    stripe.api_key = secret_key
    # print(user_id,date,email_id,amount,description)
    amount=int(amount)*100
    print(amount,type(amount))
    return render_template('payment/payment.html',amount=amount,data=data,pub_key=pub_key)

@connecsiApp.route('/thanks')
@is_logged_in
def thanks():
    return render_template('payment/thanks.html')

@connecsiApp.route('/pay', methods=['POST'])
def pay():
    secret_key = 'sk_test_4YZbWgXJul77g819JY5REXLL005jjbeXaG'
    stripe.api_key = secret_key
    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])
    data=request.form.to_dict()
    subScriptionData=data['data']
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=data['amount'],
        currency='usd',
        description='Package',
        metadata = {'email_id': session['email_id'],'connecsi_user_id':session['user_id'],'stripe_customer_id':customer.id}
    )
    print(charge)

    print('customer id =',customer.id)
    print('reciept url = ',charge.receipt_url)
    if customer.id and charge.receipt_url:
       try:
           payload={
               "customer_id":customer.id,
               "amount":data['amount'],
               "description":"Subscription/Package/Features added",
               "receipt_url":charge.receipt_url
           }
           print(payload)
           save_payment_url = base_url + 'Payments/' + str(session['user_id'])
           print(save_payment_url)
           res = requests.post(url=base_url+'Payments/'+str(session['user_id']),json=payload)
           if res.status_code==201:
              return render_template('payment/thanks.html', data=subScriptionData)
       except Exception as e:
           print(e)
    # customer_list = stripe.Customer.list()
    # print(customer_list)
       return render_template('payment/thanks.html', data=subScriptionData)
    else:
        return render_template('payment/error.html',data=subScriptionData)


@connecsiApp.route('/viewMyPayments')
@is_logged_in
def viewMyPayments():
    data = ''
    user_id = session['user_id']
    url = base_url + 'Payments/'+str(user_id)
    try:
        response = requests.get(url=url)
        data = response.json()
        print(data)
        return render_template('user/view_my_payments.html', data=data)
    except:
        pass
    return render_template('user/view_my_payments.html',data=data)


# @connecsiApp.route('/addCampaign')
# @is_logged_in
# def addCampaign():
#     url_regionCodes = base_url + 'Youtube/regionCodes'
#     regionCodes_json = ''
#     try:
#         regionCodes_response = requests.get(url=url_regionCodes)
#         regionCodes_json = regionCodes_response.json()
#         print(regionCodes_json)
#     except:pass
#     url_videoCat = base_url + 'Youtube/videoCategories'
#     videoCat_json=''
#     try:
#         response_videoCat = requests.get(url=url_videoCat)
#         videoCat_json = response_videoCat.json()
#         print(videoCat_json)
#     except Exception as e:
#         print(e)
#     return render_template('campaign/add_campaignForm.html',regionCodes=regionCodes_json,videoCategories = videoCat_json)

@connecsiApp.route('/addCampaign')
@is_logged_in
def addCampaign():
    url_regionCodes = base_url + 'Youtube/regionCodes'
    regionCodes_json = ''
    subscriptionValue=getSubscriptionValues(str(session["user_id"]))
    campaign_count=0
    classified_count=0
    feature_name=''
    messageSubscription = {
        'Create Campaign': '',
        'Classified Ads Posting': ''
    }
    for i in subscriptionValue['data']:
        if(i['feature_name']=='Create Campaign'):
            campaign_count=i['units']
            feature_name=i['feature_name']
        elif(i['feature_name']=='Classified Ads Posting'):
            classified_count=i['units']
    if(classified_count==0):
        messageSubscription['Classified Ads Posting']="You ran out of Classified Ads Posting Units of your "+subscriptionValue['data'][0]['package_name']+" package. Continue without posting it as a Classified Ads. Or Just upgrade your subscription"
    elif classified_count==-1:
        messageSubscription['Classified Ads Posting'] = " Your package " + \
        subscriptionValue['data'][0]['package_name'] + "does not have this feature"
    if(campaign_count==0):
        messageSubscription['Create Campaign']="You ran out of "+feature_name+" Units of your "+subscriptionValue['data'][0]['package_name']+" package. You can add more create campaigns in custom option or upgrade subscription."
    try:
        regionCodes_response = requests.get(url=url_regionCodes)
        regionCodes_json = regionCodes_response.json()
        print(regionCodes_json)
    except:pass
    url_videoCat = base_url + 'Youtube/videoCategories'
    videoCat_json=''
    try:
        response_videoCat = requests.get(url=url_videoCat)
        videoCat_json = response_videoCat.json()
        print(videoCat_json)
    except Exception as e:
        print(e)
    return render_template('campaign/add_campaignForm.html',classified_count=classified_count,messageSubscription=messageSubscription,campaign_count=campaign_count,regionCodes=regionCodes_json,videoCategories = videoCat_json)


@connecsiApp.route('/editCampaign/<string:campaign_id>',methods=['GET'])
@is_logged_in
def editCampaign(campaign_id):
    url_regionCodes = base_url + 'Youtube/regionCodes'
    regionCodes_json = ''
    try:
        regionCodes_response = requests.get(url=url_regionCodes)
        regionCodes_json = regionCodes_response.json()
        print(regionCodes_json)
    except:
        pass
    url_videoCat = base_url + 'Youtube/videoCategories'
    videoCat_json = ''
    try:
        response_videoCat = requests.get(url=url_videoCat)
        videoCat_json = response_videoCat.json()
        print(videoCat_json)
    except Exception as e:
        print(e)
    print(campaign_id)
    user_id = session['user_id']
    from templates.campaign.campaign import Campaign
    campaignObj = Campaign(user_id=user_id, campaign_id=campaign_id)
    view_campaign_details_data = campaignObj.get_campaign_details()
    try:
        for item in view_campaign_details_data['data']:
            item['from_date'] = datetime.datetime.strptime(item['from_date'],'%d-%b-%y').date()
            item['to_date'] = datetime.datetime.strptime(item['to_date'], '%d-%b-%y').date()
            item['arrangements'] = item['arrangements'].replace('/', '')
            item['arrangements'] = item['arrangements'].replace(' ', '')
            item['kpis'] = item['kpis'].replace(' ', '')
    except Exception as e:
        print(e)
    return render_template('campaign/edit_campaignForm.html', view_campaign_details_data=view_campaign_details_data,
                           regionCodes=regionCodes_json, videoCategories=videoCat_json)



@connecsiApp.route('/updateCampaign',methods=['POST'])
@is_logged_in
def updateCampaign():
    if request.method == 'POST':
        payload = request.form.to_dict()
        # print('payload = ',payload)
        campaign_id = request.form.get('campaign_id')
        # exit
        del payload['campaign_id']
        # print(payload)
        # print(campaign_id)
        # exit()
        channels = request.form.getlist('channels')
        channels_string = ','.join(channels)
        payload.update({'channels':channels_string})
        regions = request.form.getlist('country')
        regions_string = ','.join(regions)
        payload.update({'regions':regions_string})


        arrangements = request.form.getlist('arrangements')
        arrangements_string = ','.join(arrangements)
        payload.update({'arrangements': arrangements_string})

        kpis = request.form.getlist('kpis')
        kpis_string = ','.join(kpis)
        payload.update({'kpis': kpis_string})

        is_classified_post = request.form.get('is_classified_post')
        # print('is classified = ',is_classified_post)
        try:
            del payload['country']
            del payload['is_classified_post']
        except:pass
        # if is_classified_post == 'on':
        #     payload.update({'is_classified_post':'TRUE'})
        # else:
        #     payload.update({'is_classified_post':'FALSE'})
        files = request.files.getlist("campaign_files")
        # print(files)
        # exit()
        filenames=[]
        for file in files:
            filename = campaign_files.save(file)
            filenames.append(filename)


        user_id = session['user_id']
        url_campaign = base_url + 'Campaign/' + str(campaign_id) + '/' + str(user_id)
        response_campaign = requests.get(url=url_campaign)
        result_json_campaign = response_campaign.json()
        # print('cam data',result_json_campaign)

        for item in result_json_campaign['data']:
            files_string = item['files']
            print(files_string)
            if files_string:
               filenames.append(files_string)

        filenames_string = ','.join(filenames)
        print('file name string', filenames_string)
        payload.update({'files': filenames_string})

        print('last payload',payload)
        # exit()

        if is_classified_post == 'on':
            payload.update({'is_classified_post':'TRUE'})
            print('payload inside if =',payload)
            for file in files:
                # brands_classified_files.save(file)
                campaign_files.save(file)
            user_id = session['user_id']
            classified_url = base_url + 'Classified/' + str(user_id)
            print(classified_url)
            classified_payload = copy.deepcopy(payload)
            classified_payload['classified_name'] = classified_payload.pop('campaign_name')
            classified_payload['classified_description'] = classified_payload.pop('campaign_description')
            classified_payload['convert_to_campaign'] = classified_payload.pop('is_classified_post')
            print('classified_payload=',classified_payload)
            try:
                requests.post(url=classified_url, json=classified_payload)
            except Exception as e:
                print(e)
                pass

        else:
            payload.update({'is_classified_post':'FALSE'})


        url = base_url + 'Campaign/'+str(campaign_id)+'/' + str(user_id)
        print(url)
        try:
            response = requests.put(url=url, json=payload)
            result_json = response.json()
            print(result_json)
            flash('Updated Campaign', 'success')
            return viewCampaigns()
        except Exception as e:
            print(e)
            flash('campaign didnt saved Please try again later','danger')
            pass
    else:
        flash('Unauthorized', 'danger')


@connecsiApp.route('/deleteCampaign/<string:campaign_id>',methods=['GET'])
@is_logged_in
def deleteCampaign(campaign_id):
    print(campaign_id)
    user_id= session['user_id']
    url = base_url + 'Campaign/' + str(campaign_id) + '/' + str(user_id)
    print(url)
    try:
        response = requests.delete(url=url)
        result_json = response.json()
        print(result_json)
        res = requests.put(url=base_url + 'Campaign/update_campaign_status/' + str(campaign_id) + '/' + 'InActive')
        flash('Deleted Campaign', 'success')
        return viewCampaigns()
    except Exception as e:
        print(e)
        flash('Please try again later', 'danger')
        pass

@connecsiApp.route('/deletedCampaigns',methods=['GET','POST'])
@is_logged_in
def deletedCampaigns():
    user_id=session['user_id']
    # import templates
    from templates.campaign.campaign import Campaign
    campaignObj = Campaign(user_id=user_id)
    # campaignObj = templates.campaign.campaign.Campaign(user_id=user_id)
    view_campaign_data = campaignObj.get_all_campaigns()
    deleted_campaign_list = []
    for item in view_campaign_data['data']:
        if item['deleted'] =='true':
            deleted_campaign_list.append(item)

    print(deleted_campaign_list)
    return render_template('campaign/deleted_campaigns.html',view_campaign_data=deleted_campaign_list)





@connecsiApp.route('/viewCampaigns',methods=['GET','POST'])
@is_logged_in
def viewCampaigns():
    user_id=session['user_id']
    # import templates
    from templates.campaign.campaign import Campaign
    campaignObj = Campaign(user_id=user_id)
    # campaignObj = templates.campaign.campaign.Campaign(user_id=user_id)
    view_campaign_data = campaignObj.get_all_campaigns()
    view_campaign_data_list = []
    for item in view_campaign_data['data']:
        if item['deleted'] !='true':
            view_campaign_data_list.append(item)
    print(view_campaign_data_list)
    for item1 in view_campaign_data_list :
        campaign_id = item1['campaign_id']
        channel_status_campaign = requests.get(url=base_url+'Campaign/channel_status_for_campaign_by_campaign_id/'+ str(campaign_id))
        print(channel_status_campaign.json())
        channel_status_campaign_json = channel_status_campaign.json()
        try:
            item1.update({'status':channel_status_campaign_json['data'][0]['status']})
        except:
            item1.update({'status':''})
            pass
    print(view_campaign_data_list)
    return render_template('campaign/viewCampaigns.html',view_campaign_data=view_campaign_data_list)


@connecsiApp.route('/viewInfCampaigns',methods=['GET','POST'])
@is_logged_in
def viewInfCampaigns():
    channel_id = session['user_id']
    url = base_url+'Influencer/getMyCampaigns/'+str(channel_id)
    response = requests.get(url=url)
    response_json = response.json()
    print(response_json)
    for item in response_json['data']:
        print(item)
    return render_template('campaign/view_all_inf_campaigns.html',view_inf_campaigns_data=response_json)




@connecsiApp.route('/getCampaigns',methods=['GET','POST'])
@is_logged_in
def getCampaigns():
    user_id=session['user_id']
    from templates.campaign.campaign import Campaign
    campaignObj = Campaign(user_id=user_id)
    view_campaign_data = campaignObj.get_all_campaigns()
    return jsonify(results=view_campaign_data['data'])

@connecsiApp.route('/viewCampaignDetails/<string:campaign_id>',methods=['GET'])
@is_logged_in
def viewCampaignDetails(campaign_id):
    user_id = session['user_id']
    from templates.campaign.campaign import Campaign
    campaignObj = Campaign(user_id=user_id,campaign_id=campaign_id)
    view_campaign_details_data = campaignObj.get_campaign_details()

    channel_status_campaign = requests.get(url=base_url + 'Campaign/channel_status_for_campaign_by_campaign_id/' + str(campaign_id))
    print('status of channel =',channel_status_campaign.json())
    channel_status_campaign_data=channel_status_campaign.json()
    # print('my data',view_campaign_details_data)
    campaign_status = 'Queued'
    for item in view_campaign_details_data['data']:
        if item['campaign_status'] == 'Active':
            print(item['campaign_status'])
        elif item['campaign_status'] == 'Finished':
            print(item['campaign_status'])
        elif item['campaign_status'] == 'InActive':
            print(item['campaign_status'])
        elif item['campaign_status'] == 'Queued':
            print(item['campaign_status'])
        elif item['campaign_status'] == 'New':
            resposnse = requests.put(url=base_url + 'Campaign/update_campaign_status/' + str(campaign_id) + '/' + str(campaign_status))


    for item in view_campaign_details_data['data'][0]['youtube_inf_data']:
        print(item)
        proposal_id = item['proposal_id']
        proposal_channels = item['proposal_channels']
        if proposal_channels:
            channel_id_list = proposal_channels.split(',')
            icr = []
            for channel in channel_id_list:
                channel_id_final = channel.split('@')
                print(channel_id_final)
                url_inf_report = base_url + 'Campaign/InfluencerCampaignReport/' + str(campaign_id) + '/' + str(proposal_id) + '/' + str(channel_id_final[1])
                inf_campaign_report_res = requests.get(url=url_inf_report)
                inf_campaign_report = inf_campaign_report_res.json()
                icr.append(inf_campaign_report['data'])
                item.update({'icr_data_list':icr})
            print(item)
            for item1 in item['icr_data_list']:
                print(item1)
    return render_template('campaign/viewCampaignDetails.html',view_campaign_details_data=view_campaign_details_data,channel_status_campaign_data=channel_status_campaign_data)


@connecsiApp.route('/viewInfCampaignDetails/<string:proposal_id>',methods=['GET'])
@is_logged_in
def viewInfCampaignDetails(proposal_id):
    channel_id = session['user_id']
    url = base_url+'Influencer/getMyCampaignDetails/'+str(channel_id)+'/'+str(proposal_id)
    response = requests.get(url=url)
    view_inf_campaign_details_data = response.json()
    print('inf data',view_inf_campaign_details_data)

    bcr_list = []
    infcr=[]
    for item in view_inf_campaign_details_data['data']:
        user_id = item['user_id']
        campaign_id=item['campaign_id']
        proposal_channels= item['proposal_channels']
        channel_id_list = proposal_channels.split(',')
        for channel in channel_id_list:
            channel_id_final = channel.split('@')
            print(channel_id_final)
            url = base_url + 'Campaign/BrandCampaignReport/' + str(user_id) + '/' + str(campaign_id) +'/'+str(channel_id_final[1])
            response_bcr = requests.get(url=url)
            brand_campaign_report = response_bcr.json()
            bcr_list.append(brand_campaign_report)
            infcr_url = base_url + 'Campaign/InfluencerCampaignReport/' + str(campaign_id) + '/' + str(proposal_id) + '/' + str(channel_id_final[1])
            response_infcr = requests.get(url=infcr_url)
            infcr.append(response_infcr.json())
            # print('bcr data', brand_campaign_report)
    print('bcr list = ',bcr_list)
    print('infcr = ',infcr)
    # for item in infcr:
    #     # print(item['data'])
    #     for item1 in item['data']:
    #         print(item1)
    return render_template('campaign/view_inf_campaign_details.html',
                           view_inf_campaign_details_data=view_inf_campaign_details_data,
                           bcr=bcr_list,infcr=infcr)



@connecsiApp.route('/saveInfReport', methods=['POST'])
@is_logged_in
def saveInfReport():
    payload = request.form.to_dict()
    campaign_id = request.form.get('campaign_id')
    channel_id = request.form.get('channel_id')
    proposal_id = request.form.get('proposal_id')
    url = base_url + 'Campaign/InfluencerCampaignReport/' + str(campaign_id) + '/' + str(proposal_id)+'/'+str(channel_id)
    print(payload)
    print(url)
    try:
        response = requests.post(url=url, json=payload)
        data = response.json()
        inf_campaign_report_res = requests.get(url=url)
        inf_campaign_report = inf_campaign_report_res.json()
        print(inf_campaign_report)
        return jsonify(results=inf_campaign_report['data'])
    except Exception as e:
        print(e)
        return 'server error'


@connecsiApp.route('/delInfReport/<string:inf_campaign_report_id>', methods=['GET'])
@is_logged_in
def delInfReport(inf_campaign_report_id):

    del_report_url = base_url + 'Campaign/getInfluencerCampaignReportByReportId/' + str(inf_campaign_report_id)

    try:
        response = requests.delete(url=del_report_url)
        data = response.json()

        # url = base_url + 'Campaign/InfluencerCampaignReport/' + str(campaign_id) + '/' + str(proposal_id) + '/' + str(channel_id)
        # inf_campaign_report_res = requests.get(url=url)
        # inf_campaign_report = inf_campaign_report_res.json()
        # print(inf_campaign_report)
        return 'Successfully Deleted'
    except Exception as e:
        print(e)
        return 'server error'

@connecsiApp.route('/updateInfReport', methods=['POST'])
@is_logged_in
def updateInfReport():
    payload = request.form.to_dict()
    inf_campaign_report_id = request.form.get('inf_campaign_report_id')
    update_report_url = base_url + 'Campaign/getInfluencerCampaignReportByReportId/' + str(inf_campaign_report_id)
    try:
        response = requests.put(url=update_report_url,json=payload)
        data = response.json()
        return 'Successfully Updated'
    except Exception as e:
        print(e)
        return 'server error'


@connecsiApp.route('/getInfReportByReportId/<string:inf_campaign_report_id>', methods=['GET'])
@is_logged_in
def getInfReportByReportId(inf_campaign_report_id):

    get_report_url = base_url + 'Campaign/getInfluencerCampaignReportByReportId/' + str(inf_campaign_report_id)

    try:
        response = requests.get(url=get_report_url)
        data = response.json()
        print(data)
        return jsonify(results=data['data'])
    except Exception as e:
        print(e)
        return 'server error'

@connecsiApp.route('/getInfCampaignReports/<string:campaign_id>/<string:proposal_id>/<string:channel_id>',methods=['GET','POST'])
def getInfCampaignReports(campaign_id,proposal_id,channel_id):
    try:
        print(campaign_id,proposal_id,channel_id)
        url = base_url + 'Campaign/InfluencerCampaignReport/' + str(campaign_id) + '/' + str(proposal_id) + '/' + str(channel_id)
        inf_campaign_report_res = requests.get(url=url)
        inf_campaign_report = inf_campaign_report_res.json()
        print(inf_campaign_report)
        return jsonify(results=inf_campaign_report['data'])
    except Exception as e:
        print(e)
        return 'server error'

@connecsiApp.route('/getCampaignDetails/<string:campaign_id>',methods=['GET'])
@is_logged_in
def getCampaignDetails(campaign_id):
    user_id = session['user_id']
    from templates.campaign.campaign import Campaign
    campaignObj = Campaign(user_id=user_id,campaign_id=campaign_id)
    view_campaign_details_data = campaignObj.get_campaign_details()
    return jsonify(results=view_campaign_details_data['data'])

# @connecsiApp.route('/saveCampaign',methods=['POST'])
# @is_logged_in
# def saveCampaign():
#     if request.method == 'POST':
#         payload = request.form.to_dict()
#         print(payload)
#         # exit()
#         channels = request.form.getlist('channels')
#         channels_string = ','.join(channels)
#         payload.update({'channels':channels_string})
#         regions = request.form.getlist('country')
#         regions_string = ','.join(regions)
#         payload.update({'regions':regions_string})
#
#
#         arrangements = request.form.getlist('arrangements')
#         arrangements_string = ','.join(arrangements)
#         payload.update({'arrangements': arrangements_string})
#
#         kpis = request.form.getlist('kpis')
#         kpis_string = ','.join(kpis)
#         payload.update({'kpis': kpis_string})
#
#         is_classified_post = request.form.get('is_classified_post')
#         print('is classified = ',is_classified_post)
#         try:
#             del payload['country']
#             del payload['is_classified_post']
#         except:pass
#
#         files = request.files.getlist("campaign_files")
#         print(files)
#         # exit()
#         filenames=[]
#         for file in files:
#             if (file.filename):
#                 filename = campaign_files.save(file)
#                 filenames.append(filename)
#         filenames_string = ','.join(filenames)
#         payload.update({'files': filenames_string})
#         print(payload)
#         # exit()
#         if is_classified_post == 'on':
#             payload.update({'is_classified_post':'TRUE'})
#             print('payload inside if =',payload)
#             for file in files:
#                 # brands_classified_files.save(file)
#                 if(file.filename):
#                     campaign_files.save(file)
#             user_id = session['user_id']
#             classified_url = base_url + 'Classified/' + str(user_id)
#             print(classified_url)
#             classified_payload = copy.deepcopy(payload)
#             classified_payload['classified_name'] = classified_payload.pop('campaign_name')
#             classified_payload['classified_description'] = classified_payload.pop('campaign_description')
#             classified_payload['convert_to_campaign'] = classified_payload.pop('is_classified_post')
#             print('classified_payload=',classified_payload)
#             try:
#                 requests.post(url=classified_url, json=classified_payload)
#             except Exception as e:
#                 print(e)
#                 pass
#
#         else:
#             payload.update({'is_classified_post':'FALSE'})
#
#         user_id = session['user_id']
#         url = base_url + 'Campaign/' + str(user_id)
#         print(url)
#         print('campaign payload = ',payload)
#         try:
#             response = requests.post(url=url, json=payload)
#             result_json = response.json()
#             print(result_json)
#             flash('saved Campaign', 'success')
#             return viewCampaigns()
#         except Exception as e:
#             print(e)
#             flash('campaign didnt saved Please try again later','danger')
#             pass
#     else:
#         flash('Unauthorized', 'danger')


@connecsiApp.route('/saveCampaign',methods=['POST'])
@is_logged_in
def saveCampaign():
    if request.method == 'POST':
        payload = request.form.to_dict()
        print(payload)
        # exit()
        channels = request.form.getlist('channels')
        channels_string = ','.join(channels)
        payload.update({'channels':channels_string})
        regions = request.form.getlist('country')
        regions_string = ','.join(regions)
        payload.update({'regions':regions_string})


        arrangements = request.form.getlist('arrangements')
        arrangements_string = ','.join(arrangements)
        payload.update({'arrangements': arrangements_string})

        kpis = request.form.getlist('kpis')
        kpis_string = ','.join(kpis)
        payload.update({'kpis': kpis_string})

        is_classified_post = request.form.get('is_classified_post')
        print('is classified = ',is_classified_post)
        try:
            del payload['country']
            del payload['is_classified_post']
        except:pass

        files = request.files.getlist("campaign_files")
        print(files)
        # exit()
        filenames=[]
        for file in files:
            if (file.filename):
                filename = campaign_files.save(file)
                filenames.append(filename)
        filenames_string = ','.join(filenames)
        payload.update({'files': filenames_string})
        print(payload)
        # exit()
        if is_classified_post == 'on':
            payload.update({'is_classified_post':'TRUE'})
            print('payload inside if =',payload)
            for file in files:
                # brands_classified_files.save(file)
                if(file.filename):
                    campaign_files.save(file)
            user_id = session['user_id']
            classified_url = base_url + 'Classified/' + str(user_id)
            print(classified_url)
            classified_payload = copy.deepcopy(payload)
            classified_payload['classified_name'] = classified_payload.pop('campaign_name')
            classified_payload['classified_description'] = classified_payload.pop('campaign_description')
            classified_payload['convert_to_campaign'] = classified_payload.pop('is_classified_post')
            print('classified_payload=',classified_payload)
            try:
                requests.post(url=classified_url, json=classified_payload)
            except Exception as e:
                print(e)
                pass

        else:
            payload.update({'is_classified_post':'FALSE'})

        user_id = session['user_id']
        url = base_url + 'Campaign/' + str(user_id)
        print(url)
        print('campaign payload = ',payload)
        try:
            response = requests.post(url=url, json=payload)
            result_json = response.json()
            print(result_json)
            check = subscriptionReduction("Create Campaign")
            if (check['response'] == 1):
                print("done subscription create campaign")
                if(payload['is_classified_post']=='TRUE'):
                    check1 = subscriptionReduction("Classified Ads Posting")
                    if(check1['response']==1):
                        print("done subscription create campaign with classified ads posting")
            flash('saved Campaign', 'success')
            return viewCampaigns()
        except Exception as e:
            print(e)
            flash('campaign didnt saved Please try again later','danger')
            pass
    else:
        flash('Unauthorized', 'danger')



@connecsiApp.route('/calendarView',methods=['GET'])
@is_logged_in
def calendarView():
    user_id = session['user_id']
    from templates.campaign.campaign import Campaign
    campaignObj = Campaign(user_id=user_id)
    campaign_data = campaignObj.get_all_campaigns()
    print(campaign_data)

    for item in campaign_data['data']:
        item['from_date'] = datetime.datetime.strptime(item['from_date'],'%d-%b-%y').date().strftime('%Y-%m-%d')
        item['to_date'] = datetime.datetime.strptime(item['to_date'], '%d-%b-%y').date().strftime('%Y-%m-%d')
        if item['campaign_status'] == 'New':
           item.update({'color':'#393FDB'})
        elif item['campaign_status'] == 'Queued':
            item.update({'color': '#FE831A'})
        elif item['campaign_status'] == 'Active':
           item.update({'color':'#48E552'})
        elif item['campaign_status'] == 'Finished':
           item.update({'color':'#F30636'})
        elif item['campaign_status'] == 'InActive':
           item.update({'color':'#929292'})

    print(campaign_data)
    return render_template('campaign/calenderView.html',campaign_data=campaign_data)

@connecsiApp.route('/inbox/<string:message_id>',methods = ['GET'])
@is_logged_in
def inbox(message_id):
    message_id = str(message_id)
    inbox = ''
    full_conv=''
    conv_title=''
    length_conv=''
    user_id = session['user_id']
    print('user id=',user_id)
    type = session['type']
    print('user type = ',type)
    email_id = session['email_id']
    print('email id =', email_id)
    url = base_url + 'Messages/' + str(user_id) + '/' + type
    conv_url = base_url + 'Messages/conversations/' + str(email_id)
    try:
        response = requests.get(url=url)
        data = response.json()
        print('messages = ',data)
        conv_resposne = requests.get(url=conv_url)
        conv_data = conv_resposne.json()
        print('conv = ',conv_data)
        ###################### get inbox
        inboxList=[]
        message_id_list=[]
        for item in data['data']:
            if item['to_email_id'] == email_id:
               inboxList.append(item)
               message_id_list.append(item['message_id'])
        # print(mylist)
        for item in conv_data['data']:
            # if item['to_email_id'] == email_id and item['message_id'] not in message_id_list:
            if item['to_email_id'] == email_id :
               # message_id1 = item['message_id']
               # print(message_id1)
               # for message in data['data']:
               #     if message_id1 == message['message_id']:
               #        read = message['read']
               #        item.update({'read': read})
               inboxList.append(item)
        print('inboxList  =',inboxList)
        inboxSorted = sorted(inboxList, key=lambda k: k['message_id'])
        print('sorted inboxlist = ', inboxSorted)
        inbox = {}
        inbox.update({'data':inboxSorted})
        print('inbox = ',inbox)

        for item in inbox['data']:
            inbox_user_id = item['user_id']
            print(inbox_user_id)
            inbox_user_type = item['user_type']
            print('inbox user type',inbox_user_type)
            first_name = ''
            profile_pic = ''
            if inbox_user_type == 'brand':
                brand_details_url = base_url+'/Brand/'+str(inbox_user_id)
                brand_details_resposne = requests.get(url=brand_details_url)
                brand_details_json = brand_details_resposne.json()
                print('brand details = ',brand_details_json)
                first_name = brand_details_json['data']['first_name']
                profile_pic = brand_details_json['data']['profile_pic']
                print(first_name)
            elif inbox_user_type == 'influencer':
                inbox_email_id = item['from_email_id']
                influencer_details_url = base_url + '/Influencer/GetDetailsByEmailId/' + str(inbox_email_id)
                print(influencer_details_url)

                influencer_details_resposne = requests.get(url=influencer_details_url)
                influencer_details_json = influencer_details_resposne.json()
                print(influencer_details_json)
                first_name = influencer_details_json['data']['first_name']
                profile_pic = influencer_details_json['data']['channel_img']
                if first_name =='':
                    first_name=inbox_email_id
            item.update({'first_name': first_name})
            item.update({'profile_pic': profile_pic})
            # print(item)

        # #######################################

        from_email_id=''

        if message_id == "0":
            try:
                message_id = inbox['data'][-1]['message_id']
                from_email_id = inbox['data'][0]['from_email_id']
                print('default message id = ', message_id)
            except:pass
        else: print('new message id = ',message_id)
            # print(from_email_id)
        # ########################### get conversations

        getConv_url = base_url + 'Messages/conversations/' + str(message_id)+'/'+str(user_id)+'/'+str(type)
        print(getConv_url)
        full_conv_resposne = requests.get(url=getConv_url)
        full_conv_data = full_conv_resposne.json()
        print('full_conv_data = ',full_conv_data)
        #################################################
        convList = []
        for item in data['data']:
            if item['message_id'] == int(message_id):
                convList.append(item)
        # print(mylist)
        for item in full_conv_data['data']:
            if item['message_id'] == int(message_id):
                convList.append(item)
        full_conv = {}
        full_conv.update({'data': convList})
        print('full_conv = ', full_conv)
        length_conv = len(full_conv['data'])
        print('length = ',length_conv)
        collapse_id = 1
        for item in full_conv['data']:
            full_conv_user_id = item['user_id']
            # print(full_conv_user_id)
            full_conv_user_type = item['user_type']
            first_name = ''
            profile_pic = ''
            if full_conv_user_type == 'brand':
                brand_details_url = base_url+'/Brand/'+str(full_conv_user_id)
                brand_details_resposne = requests.get(url=brand_details_url)
                brand_details_json = brand_details_resposne.json()
                print('brand details for conv =',brand_details_json)
                first_name = brand_details_json['data']['first_name']
                profile_pic = brand_details_json['data']['profile_pic']
            elif full_conv_user_type == 'influencer':
                full_conv_email_id = item['from_email_id']
                influencer_details_url = base_url + '/Influencer/GetDetailsByEmailId/' + str(full_conv_email_id)
                influencer_details_resposne = requests.get(url=influencer_details_url)
                influencer_details_json = influencer_details_resposne.json()
                print('INF DETAILS=======',influencer_details_json)
                inf_channel_id = influencer_details_json['data']['channel_id']
                print('INF CHANNEL ID ======',inf_channel_id)
                item.update({'channel_id':inf_channel_id})
                first_name = influencer_details_json['data']['first_name']
                profile_pic = influencer_details_json['data']['channel_img']
                if first_name =='':
                    first_name=full_conv_email_id
            item.update({'first_name': first_name})
            item.update({'collapse_id':collapse_id})
            item.update({'profile_pic': profile_pic})
            # print(item)
            collapse_id+=1
################ remove deleted message from inbox and conv ##################
        removed_deleted_messages_from_inbox = []
        for item in inbox['data']:
            try:
                deleted_from_user_id_string = item['deleted_from_user_id']
                deleted_from_user_id_list = deleted_from_user_id_string.split(',')
                print('deleted user list from inbox',deleted_from_user_id_list)
                if str(user_id) not in deleted_from_user_id_list:
                    removed_deleted_messages_from_inbox.append(item)
            except:
                removed_deleted_messages_from_inbox.append(item)
                pass
        inbox.update({'data': removed_deleted_messages_from_inbox})
        print('removed deleted from inbox', inbox)

        inbox['data'] = inbox['data'][::-1]
        inbox.update({'data':inbox['data']})
        removed_deleted_messages_from_conv = []
        for item in full_conv['data']:
            try:
                deleted_from_user_id_string = item['deleted_from_user_id']
                deleted_from_user_id_list = deleted_from_user_id_string.split(',')
                print('deleted user list from full conv', deleted_from_user_id_list)
                if str(user_id) not in deleted_from_user_id_list:
                    removed_deleted_messages_from_conv.append(item)
            except:
                removed_deleted_messages_from_conv.append(item)
                pass
        full_conv.update({'data':removed_deleted_messages_from_conv})
        print('removed deleted from conv',full_conv)
############################################################
        # ####################################
        try:
            conv_title = full_conv['data'][0]['subject']
        except:pass

        from templates.campaign.campaign import Campaign
        campaignObj = Campaign(user_id=user_id)
        view_campaign_data = campaignObj.get_all_campaigns()
        for item in view_campaign_data['data']:
            if item['deleted'] == 'true':
                view_campaign_data['data'].remove(item)

        print('final conv = ',full_conv)
        for item in full_conv['data']:
            print(item)
        print('campaign data = ',view_campaign_data)
        print('final inbox =',inbox)
        ############## sort inbox according to date ################
        for item in inbox['data']:
            print('message inbox = ',item)

        inbox['data'].sort(key=lambda x: datetime.datetime.strptime(x['date'], '%A, %d. %B %Y %I:%M%p'),reverse=True)
        message_id_list1 = []
        for item in inbox['data']:
            if item['message_id'] not in message_id_list1:
                message_id_list1.append(item['message_id'])
            else:
                inbox['data'].remove(item)
                print('after sorting inbox = ',item)
        print(message_id_list1)
        ############## sort end ####################################
        return render_template('email/inbox.html', inbox = inbox, full_conv = full_conv, conv_title=conv_title,view_campaign_data=view_campaign_data)
    except Exception as e:
        print(e)
        pass

    from templates.campaign.campaign import Campaign
    campaignObj = Campaign(user_id=user_id)
    view_campaign_data = campaignObj.get_all_campaigns()

    print('final conv default = ', full_conv)

    return render_template('email/inbox.html',inbox=inbox, full_conv = full_conv,conv_title=conv_title,view_campaign_data=view_campaign_data)


@connecsiApp.route('/update_message_as_read/<string:message_id>',methods=['GET'])
@is_logged_in
def update_message_as_read(message_id):
    url = base_url+'Messages/update_message_as_read/'+str(message_id)
    try:
        requests.get(url=url)
        return 'read message'
    except Exception as e:
        print(e)
        return 'error while opening message'

@connecsiApp.route('/update_conversation_as_read/<string:conv_id>',methods=['GET'])
@is_logged_in
def update_conversation_as_read(conv_id):
    url = base_url+'Messages/update_conversation_as_read/'+str(conv_id)
    try:
        requests.get(url=url)
        return 'read'
    except Exception as e:
        print(e)
        return 'error while opening message'

@connecsiApp.route('/get_all_unread_messages',methods=['GET'])
@is_logged_in
def get_all_unread_messages():
    to_email_id = session['email_id']
    url = base_url+'Messages/getAllUnreadMessages/'+str(to_email_id)
    try:
        response = requests.get(url=url)
        return jsonify(results=response.json())
    except Exception as e:
        print(e)
        return 'error while getting unread messages'


@connecsiApp.route('/addCampaignsToMessage',methods=['POST','GET'])
@is_logged_in
def addCampaignsToMessage():
    if request.method=='POST':
        message_id=request.form.get('message_id')
        campaign_ids= request.form.getlist('campaign_id')
        channel_id = request.form.get('channel_id')
        print('message_id = ',message_id)
        print('campaign_ids = ',campaign_ids)
        print('channel_id = ',channel_id)
        # exit()
        if campaign_ids:
            for campaign_id in campaign_ids:
                url = base_url + 'Messages/addCampaignIdToMessageId/' + message_id + '/' + campaign_id+'/'+str(channel_id)
                print(url)
                response = requests.post(url=url)
                response_json = response.json()
                print(response_json)
            # flash('campaigns added to Conversation')
            return 'Campaigns Added To Conversation'
        else: return 'Your Campaign List is Empty'

@connecsiApp.route('/getCampaignsAddedToMessage/<string:message_id>',methods=['GET','POST'])
@is_logged_in
def getCampaignsAddedToMessage(message_id):
    print(message_id)
    url = base_url + 'Messages/getCampaignsAddedToMessage/' +message_id
    print(url)
    response = requests.get(url=url)
    response_json = response.json()
    for item in response_json['data']:
        print(item)
    return jsonify(results=response_json['data'])

@connecsiApp.route('/getCampaignsAddedToMessageByChannelId/<string:channel_id>',methods=['GET','POST'])
@is_logged_in
def getCampaignsAddedToMessageByChannelId(channel_id):
    url = base_url + 'Messages/getCampaignsAddedToMessageByChannelId/'+channel_id
    print(url)
    response = requests.get(url=url)
    response_json = response.json()
    for item in response_json['data']:
        print(item)
    return jsonify(results=response_json['data'])



@connecsiApp.route('/deleted',methods = ['GET'])
@is_logged_in
def deleted():
    deleted_dict=''
    user_id = session['user_id']
    type = session['type']
    email_id = session['email_id']
    # url = base_url + 'Messages/' + str(user_id) + '/'+ type
    conv_url = base_url + 'Messages/conversations/all/'+type
    url = base_url + 'Messages/' + str(user_id) + '/' + type
    # conv_url = base_url + 'Messages/conversations/' + str(email_id)
    print(conv_url)
    # conv_url = base_url + 'Messages/conversations/' + str(email_id)
    try:
        response = requests.get(url=url)
        messages = response.json()
        print('messages = ',messages)
        conv_resposne = requests.get(url=conv_url)
        conv_data = conv_resposne.json()
        print('conv = ',conv_data)
        # exit()
        ###################### get inbox
        deleted_list=[]
        for item in messages['data']:
            print('mess =',item)
            if item['deleted'] == 'true':
               deleted_list.append(item)
        print(deleted_list)
        for item in conv_data['data']:
            print('conv=',item)
            if item['deleted'] == 'true':
               deleted_list.append(item)
        deleted_dict = {}
        deleted_dict.update({'data':deleted_list})
        print('deleted dict 123 = ',deleted_dict)

        # ########################### get conversations
        collapse_id = 1
        for item in deleted_dict['data']:
            full_conv_user_id = item['user_id']
            print(full_conv_user_id)
            full_conv_user_type = item['user_type']
            print(full_conv_user_type)
            first_name = ''
            profile_pic = ''
            if full_conv_user_type == 'brand':
                brand_details_url = base_url+'/Brand/'+str(full_conv_user_id)
                brand_details_resposne = requests.get(url=brand_details_url)
                brand_details_json = brand_details_resposne.json()
                print(brand_details_json)
                first_name = brand_details_json['data']['first_name']
                profile_pic = brand_details_json['data']['profile_pic']
            elif full_conv_user_type == 'influencer':
                full_conv_email_id = item['from_email_id']
                influencer_details_url = base_url + '/Influencer/GetDetailsByEmailId/' + str(full_conv_email_id)
                influencer_details_resposne = requests.get(url=influencer_details_url)
                influencer_details_json = influencer_details_resposne.json()
                print('INF DETAILS=======', influencer_details_json)
                inf_channel_id = influencer_details_json['data']['channel_id']
                print('INF CHANNEL ID ======', inf_channel_id)
                item.update({'channel_id': inf_channel_id})
                first_name = influencer_details_json['data']['first_name']
                profile_pic = influencer_details_json['data']['channel_img']
                if first_name == '':
                    first_name = full_conv_email_id
            item.update({'first_name': first_name})
            item.update({'collapse_id': collapse_id})
            item.update({'profile_pic': profile_pic})
            # print(item)
            collapse_id+=1

################ remove deleted message from inbox and conv ##################
        print('hello')
        removed_deleted_messages_from_conv = []
        for item in deleted_dict['data']:
            try:
                deleted_from_user_id_string = item['deleted_from_user_id']
                print(deleted_from_user_id_string)
                try:
                    deleted_from_user_id_list = deleted_from_user_id_string.split(',')
                    print('deleted user list', deleted_from_user_id_list)
                    if str(user_id) in deleted_from_user_id_list:
                        removed_deleted_messages_from_conv.append(item)
                except Exception as e:
                    print(e)
            except Exception as e:
                print('i m in exception')
                removed_deleted_messages_from_conv.append(item)
                # pass
                print(e)
        deleted_dict.update({'data':removed_deleted_messages_from_conv})
        print('deleted messages',deleted_dict)
############################################################
        # ####################################
        return render_template('email/deleted.html', deleted_dict = deleted_dict)
    except Exception as e:
        print(e)
        return render_template('email/deleted.html',deleted_dict = deleted_dict)




@connecsiApp.route('/sent',methods = ['GET'])
@is_logged_in
def sent():
    sent = ''
    user_id = session['user_id']
    type = session['type']
    email_id = session['email_id']
    # url = base_url + 'Messages/' + str(user_id) + '/' + type
    url = base_url + 'Messages/getSentMessages/' + str(email_id)
    conv_url = base_url + 'Messages/conversations/sent/' + str(email_id)
    try:
        response = requests.get(url=url)
        data = response.json()
        for mess in data['data']:
            print('mess = ', mess)
        conv_resposne = requests.get(url=conv_url)
        conv_data = conv_resposne.json()
        for conv in conv_data['data']:
            print('conv = ', conv)
        ###################### get sent
        sentList = []
        for item in data['data']:
            if item['from_email_id'] == email_id:
                sentList.append(item)
        # print(mylist)
        for item in conv_data['data']:
            if item['from_email_id'] == email_id:
                sentList.append(item)

        sent = {}
        sent.update({'data': sentList})
        print('sent = ', sent)

        collapse_id = 1
        for item in sent['data']:
            sent_user_id = item['user_id']
            # print(sent_user_id)
            sent_user_type = item['user_type']
            senders_first_name = ''
            reciepents_first_name=''
            reciepents_profile_pic = ''
            if sent_user_type == 'brand':
                brand_details_url = base_url + '/Brand/' + str(sent_user_id)
                brand_details_resposne = requests.get(url=brand_details_url)
                brand_details_json = brand_details_resposne.json()
                # print(brand_details_json)
                senders_first_name = brand_details_json['data']['first_name']
                full_conv_to_email_id = item['to_email_id']
                influencer_details_url = base_url + '/Influencer/GetDetailsByEmailId/' + str(full_conv_to_email_id)
                influencer_details_resposne = requests.get(url=influencer_details_url)
                influencer_details_json = influencer_details_resposne.json()
                # print(influencer_details_json)
                reciepents_first_name = influencer_details_json['data']['first_name']
                reciepents_profile_pic = influencer_details_json['data']['channel_img']
            elif sent_user_type == 'influencer':
                full_conv_email_id = item['from_email_id']
                influencer_details_url = base_url + '/Influencer/GetDetailsByEmailId/' + str(full_conv_email_id)
                influencer_details_resposne = requests.get(url=influencer_details_url)
                influencer_details_json = influencer_details_resposne.json()
                # print(influencer_details_json)
                senders_first_name = influencer_details_json['data']['first_name']

                full_conv_to_email_id = item['to_email_id']
                brand_details_url = base_url + '/Brand/getDetailsByEmailId/' + str(full_conv_to_email_id)
                brand_details_resposne = requests.get(url=brand_details_url)
                brand_details_json = brand_details_resposne.json()
                # print(brand_details_json)
                reciepents_first_name = brand_details_json['data']['first_name']
                reciepents_profile_pic = brand_details_json['data']['profile_pic']
            item.update({'senders_first_name': senders_first_name})
            item.update({'reciepents_first_name': reciepents_first_name})
            item.update({'profile_pic': reciepents_profile_pic})
            item.update({'collapse_id': collapse_id})
            # print(item)
            collapse_id += 1

        removed_deleted_messages_from_sent = []
        for item in sent['data']:
            try:
                deleted_from_user_id_string = item['deleted_from_user_id']
                deleted_from_user_id_list = deleted_from_user_id_string.split(',')
                if str(user_id) not in deleted_from_user_id_list:
                    removed_deleted_messages_from_sent.append(item)
            except:
                pass
        sent.update({'data': removed_deleted_messages_from_sent})
        print('removed deleted', sent)
        sent['data'].sort(key=lambda x: datetime.datetime.strptime(x['date'], '%A, %d. %B %Y %I:%M%p'), reverse=True)


        return render_template('email/sent.html', sent=sent)
    except Exception as e:
        print(e)
        return render_template('email/sent.html', sent=sent)




@connecsiApp.route('/delete/<string:message_id>/<string:conv_id>/<string:user_id>', methods = ['GET'])
@is_logged_in
def delete(message_id,conv_id,user_id):
    print(message_id,conv_id)
    conv_id = int(conv_id)
    print(type(conv_id))
    print(user_id)
    try:
        if conv_id != 0:
            url_delete_msg_from_conv = base_url+'Messages/conversations/delete/'+str(message_id)+'/'+str(conv_id)+'/'+str(user_id)
            print(url_delete_msg_from_conv)
            response = requests.put(url=url_delete_msg_from_conv)
            print(response.json())
            flash('message moved to deleted', 'warning')
            return 'message from conversation deleted'
        else:
            url_delete_msg_from_messages = base_url+'Messages/delete/'+str(message_id)+'/'+str(user_id)
            print(url_delete_msg_from_messages)
            response = requests.put(url=url_delete_msg_from_messages)
            print(response.json())
            # flash('message moved to deleted', 'warning')
            return 'message deleted'
    except Exception as e:
        print(e)
        pass
        return 'unable to delete message'

@connecsiApp.route('/compose')
@is_logged_in
def compose():
    return render_template('email/compose.html')



@connecsiApp.route('/reply/<string:message_id>/<string:to_email_id>/<string:subject>',methods = ['GET'])
@is_logged_in
def reply(message_id,to_email_id,subject):
    return render_template('email/reply.html',to_email_id=to_email_id,subject=subject,message_id=message_id)


@connecsiApp.route('/sendEmail',methods = ['POST'])
@is_logged_in
def sendEmail():
    if request.method == 'POST':
       payload = request.form.to_dict()
       # print(payload)
       payload.update({'from_email_id': session['email_id']})
       # print(payload)
       date = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
       payload.update({'date':date})
       print(payload)
       user_id= session['user_id']
       type = session['type']
       url = base_url + 'Messages/' + str(user_id) +'/' + type
       try:
           response = requests.post(url=url, json=payload)
           data = response.json()
           print(data)
           flash('Your email has been sent', category='success')
           return render_template('email/inbox.html', data=data)
       except:
           pass
       return render_template('email/compose.html')



# @connecsiApp.route('/sendMessage',methods = ['POST'])
# @is_logged_in
# def sendMessage():
#     if request.method == 'POST':
#        payload = request.form.to_dict()
#        # print(payload)
#        payload.update({'from_email_id': session['email_id']})
#        # print(payload)
#        date = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
#        payload.update({'date':date})
#        if payload['to_email_id'] == '':
#           payload.update({'to_email_id':'kiran.padwal@connecsi.com'})
#        print(payload)
#        user_id= session['user_id']
#        type = session['type']
#        url = base_url + 'Messages/' + str(user_id) +'/' + type
#        try:
#            response = requests.post(url=url, json=payload)
#            data = response.json()
#            print(data)
#            # if data['resposne'] == 1:
#            return 'Your message has been sent'
#            # else: return "Failed to sent mail"
#        except:
#            pass
#            return  'Server Error'


@connecsiApp.route('/sendMessage',methods = ['POST'])
@is_logged_in
def sendMessage():
    if request.method == 'POST':
       payload = request.form.to_dict()
       # print(payload)
       payload.update({'from_email_id': session['email_id']})
       # print(payload)
       date = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
       payload.update({'date':date})
       if payload['to_email_id'] == '':
          payload.update({'to_email_id':'kiran.padwal@connecsi.com'})
       print(payload)
       user_id= session['user_id']
       type = session['type']
       url = base_url + 'Messages/' + str(user_id) +'/' + type
       try:
           response = requests.post(url=url, json=payload)
           data = response.json()
           print(data)
           # if data['resposne'] == 1:
           if(data['response']==1):
               check = subscriptionReduction("Messages")
               if (check['response'] == 1):
                   print("done subscription Messages")

           return 'Your message has been sent'
           # else: return "Failed to sent mail"
       except:
           pass
           return  'Server Error'


@connecsiApp.route('/show_youtube_channels_without_email_id',methods = ['POST','GET'])
@is_logged_in
def show_youtube_channels_without_email_id():
    to_email_id = 'kiran.padwal@connecsi.com'
    url = base_url+'Messages/getMessagesByToEmailId/'+to_email_id
    response = requests.get(url=url)
    print(response.json())

    data = []
    response_json = response.json()
    for item in response_json['data']:
        print(item)
        channel_name_list = item['channel_id'].split('@')
        print(channel_name_list)
        channel_name = channel_name_list[1]
        if channel_name == 'youtube':
           item['channel_id']=channel_name_list[0]
           data.append(item)
           channel_details_url = base_url+'Youtube/getChannelDetailsByChannelId/'+item['channel_id']
           print(channel_details_url)
           response_channel_details = requests.get(url=channel_details_url)
           resposne_channel_details_json = response_channel_details.json()
           print(resposne_channel_details_json)
           for channel_details in resposne_channel_details_json['data']:
               title = channel_details['title']
               item.update({'title':title})
           print('my item= ',item)
    print('data = ',data)
    return render_template('show_youtube_channels_without_email_id.html',data = data)


@connecsiApp.route('/list_brands',methods = ['POST','GET'])
@is_logged_in
def list_brands():
    url = base_url+'Brand/'
    response = requests.get(url=url)
    print(response.json())
    return render_template('list_brands.html',data = response.json())

@connecsiApp.route('/list_influencers',methods = ['POST','GET'])
@is_logged_in
def list_incluencers():
    url = base_url+'Brand/influencerList'
    response = requests.get(url=url)
    print(response.json())
    return render_template('list_influencers.html',data = response.json())


@connecsiApp.route('/update_and_send_email_youtube/<channel_id>/<message_id>/<email_id>/<subject>/<message>',methods = ['POST','GET'])
@is_logged_in
def update_and_send_email(channel_id,message_id,email_id,subject,message):
    print(channel_id)
    url = base_url+"Messages/update_and_send_email_youtube/"+channel_id+'/'+message_id+'/'+email_id+'/'+subject+'/'+message
    res = requests.get(url=url)
    print(res.json())
    response = res.json()
    if response['data']==1:
        return 'Updated and sent Email Successfully'
    else:
        return 'Server Error'



@connecsiApp.route('/sendProposal',methods = ['POST'])
@is_logged_in
def sendProposal():
    if request.method == 'POST':
       payload = request.form.to_dict()
       # payload.update({'from_email_id': session['email_id']})
       # date = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
       proposal_arrangements = request.form.getlist('proposal_arrangements')
       proposal_arrangements_string = ','.join(proposal_arrangements)
       print(proposal_arrangements_string)
       payload.update({'proposal_arrangements':proposal_arrangements_string})

       proposal_kpis = request.form.getlist('proposal_kpis')
       proposal_kpis_string = ','.join(proposal_kpis)
       print(proposal_kpis_string)
       payload.update({'proposal_kpis': proposal_kpis_string})

       proposal_channels = request.form.getlist('proposal_channels')
       proposal_channels_string = ','.join(proposal_channels)
       print(proposal_channels_string)
       payload.update({'proposal_channels': proposal_channels_string})

       print(payload)
       # exit()
       user_id= session['user_id']
       # type = session['type']
       url = base_url + 'Brand/Proposal/' + str(user_id)
       print(url)
       # exit()
       try:
           response = requests.post(url=url, json=payload)
           data = response.json()
           print(data)
           return 'Proposal Sent'
       except:
           pass
           return  'Server Error'


@connecsiApp.route('/updateProposal',methods = ['POST'])
@is_logged_in
def updateProposal():
    if request.method == 'POST':
       payload = request.form.to_dict()
       # payload.update({'from_email_id': session['email_id']})
       # date = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
       proposal_arrangements = request.form.getlist('edit_proposal_arrangements')
       proposal_arrangements_string = ','.join(proposal_arrangements)
       print(proposal_arrangements_string)
       payload.update({'edit_proposal_arrangements':proposal_arrangements_string})

       proposal_kpis = request.form.getlist('edit_proposal_kpis')
       proposal_kpis_string = ','.join(proposal_kpis)
       print(proposal_kpis_string)
       payload.update({'edit_proposal_kpis': proposal_kpis_string})

       proposal_channels = request.form.getlist('edit_proposal_channels')
       proposal_channels_string = ','.join(proposal_channels)
       print(proposal_channels_string)
       payload.update({'edit_proposal_channels': proposal_channels_string})

       print(payload)
       proposal_id = request.form.get('proposal_id')
       url = base_url + 'Brand/Proposal/get/' + str(proposal_id)
       print(url)
       # exit()
       try:
           response = requests.put(url=url, json=payload)
           data = response.json()
           print(data)
           return 'Proposal updated'
       except:
           pass
           return  'Server Error'

@connecsiApp.route('/getProposal/<string:message_id>/<string:campaign_id>',methods=['GET'])
@is_logged_in
def getProposal(message_id,campaign_id):
    url = base_url + 'Brand/Proposal/get/' + str(message_id)+'/'+str(campaign_id)
    try:
        response = requests.get(url=url)
        data = response.json()
        print('proposal data = ',data)
        return jsonify(results=data['data'])
    except:
        pass
        return 'Server Error'



@connecsiApp.route('/accept_decline_proposal/<string:message_id>/<string:campaign_id>/<string:status>',methods=['GET'])
@is_logged_in
def accept_decline_proposal(message_id,campaign_id,status):
    new_status=''
    if status == 'Accept':
        new_status = 'Current Partner'
    if status == 'Reject':
        new_status = 'Proposal Rejected'
    print(new_status)

    url = base_url + 'Campaign/update_channel_status_for_campaign/' + str(message_id)+'/'+str(campaign_id)+'/'+new_status
    try:
        response = requests.put(url=url)
        data = response.json()
        print(data)
        return 'Succesfully updated Status'
    except:
        pass
        return 'Server Error'

@connecsiApp.route('/uploadMessageFiles',methods=['POST'])
@is_logged_in
def uploadMessageFiles():
    if request.method == 'POST':
        payload = request.form.to_dict()
        user_id=session['user_id']
        payload.update({'user_id':user_id})
        files = request.files.getlist("message_files")
        print(files)
        # exit()

        filenames = []
        for file in files:
            filename = message_files.save(file)
            filenames.append(filename)
        filenames_string = ','.join(filenames)
        payload.update({'message_files': filenames_string})
        print(payload)
        # return 'uploaded files'
        # exit()
        message_id = request.form.get('message_id')
        url = base_url + 'Messages/uploadMessageFiles/'+message_id
        try:
            response = requests.post(url=url,json=payload)
            data = response.json()
            print(data)
            return 'Succesfully Uploaded Files'
        except:
            pass
            return 'Server Error'

@connecsiApp.route('/getMessageFiles/<string:message_id>',methods=['GET'])
@is_logged_in
def getMessageFiles(message_id):
    url = base_url + 'Messages/uploadMessageFiles/' + str(message_id)
    try:
        response = requests.get(url=url)
        data = response.json()
        print(data)
        return jsonify(results=data['data'])
    except:
        pass
        return 'Server Error'




@connecsiApp.route('/uploadMessageAgreements',methods=['POST'])
@is_logged_in
def uploadMessageAgreements():
    if request.method == 'POST':
        payload = request.form.to_dict()
        user_id=session['user_id']
        payload.update({'user_id':user_id})
        files = request.files.getlist("message_agreements")
        print(files)
        # exit()

        filenames = []
        try:
            for file in files:
                filename = message_agreements.save(file)
                filenames.append(filename)
        except Exception as e:
            print(e)
            return 'Only PDF and Docx Files are allowed as Agreements'
        filenames_string = ','.join(filenames)
        payload.update({'message_agreements': filenames_string})
        print(payload)
        # return 'uploaded agreement'
        # exit()
        message_id = request.form.get('message_id')
        url = base_url + 'Messages/uploadMessageAgreements/'+message_id
        try:
            response = requests.post(url=url,json=payload)
            data = response.json()
            print(data)
            return 'Succesfully Uploaded Agreement'
        except:
            pass
            return 'Server Error'


@connecsiApp.route('/getMessageAgreements/<string:message_id>',methods=['GET'])
@is_logged_in
def getMessageAgreements(message_id):
    url = base_url + 'Messages/uploadMessageAgreements/' + str(message_id)
    try:
        response = requests.get(url=url)
        data = response.json()
        print(data)
        return jsonify(results=data['data'])
    except:
        pass
        return 'Server Error'


@connecsiApp.route('/replyEmail/<string:message_id>', methods=['POST'])
@is_logged_in
def replyEmail(message_id):
    if request.method == 'POST':
        payload = request.form.to_dict()
        # print(payload)
        payload.update({'conv_from_email_id': session['email_id']})
        # print(payload)
        date = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
        payload.update({'date': date})
        print(payload)
        user_id = session['user_id']
        type = session['type']
        url = base_url + 'Messages/conversations/' +str(message_id)+'/'+ str(user_id) + '/' + type
        print(url)
        # exit()
        try:
            response = requests.post(url=url, json=payload)
            data = response.json()
            print(data)
            flash('Your email has been sent', category='success')
            return render_template('email/inbox.html', data=data)
        except:
            pass
        return render_template('email/compose.html')



@connecsiApp.route('/replyMessage', methods=['POST'])
@is_logged_in
def replyMessage():
    if request.method == 'POST':
        payload = request.form.to_dict()
        print('payload',payload)
        del payload['reply_message_first_name']
        print(payload)
        message_id = request.form.get('message_id')
        print('message id = ',message_id)
        payload.update({'conv_from_email_id': session['email_id']})
        # print(payload)
        date = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
        print(date,type(date))
        payload.update({'conv_date': date})
        print(payload)
        # exit()
        user_id = session['user_id']
        user_type = session['type']
        url = base_url + 'Messages/conversations/' + str(message_id)+'/'+ str(user_id) + '/' + str(user_type)
        print(url)

        # exit()
        try:
            response = requests.post(url=url, json=payload)
            data = response.json()
            print(data)

            return 'You Replied Successfully'
        except Exception as e:
            print(e)
            return 'Error in Reply!!!!!! Try Agin Later'




@connecsiApp.route('/addToFavInfList/<string:channel_id>/<string:channel_name>',methods=['GET'])
@is_logged_in
def addToFavInfList(channel_id,channel_name):
    try:
        print(channel_id)
        print(channel_name)
        user_id = session['user_id']
        url = base_url+'/Brand/addToFavList/'+channel_id+'/'+str(user_id)+'/'+channel_name
        response = requests.post(url=url)
        print(response)
        return channel_name+' Influencer Added To Your Favorite List'
        # flash("Added to Favorites List", 'success')
        # return searchInfluencers()
    except:
        return 'Server error'
        # flash("Could not be added to Favorites List", 'danger')
        # return influencerFavoritesList()

@connecsiApp.route('/getFavInfList',methods=['GET'])
@is_logged_in
def getFavInfList():
    user_id = session['user_id']
    url = base_url + '/Brand/getInfluencerFavList/' + str(user_id)
    response = requests.get(url=url)
    response_json=response.json()
    print(response_json)
    return jsonify(results=response_json['data'])


# @connecsiApp.route('/influencerFavoritesList/<string:channel_name>',methods=['GET','POST'])
# @is_logged_in
# def influencerFavoritesList(channel_name):
#     data=''
#     view_campaign_data=''
#     try:
#         user_id = session['user_id']
#         url = base_url+'/Brand/getInfluencerFavList_with_details/'+str(user_id)+'/'+channel_name
#         response = requests.get(url=url)
#         data = response.json()
#         print(data)
#         print(len(data))
#         linechart_id = 1
#         for item in data['data']:
#             item.update({'linechart_id': linechart_id})
#             item.update({'total_rows': len(data['data'])})
#             linechart_id += 1
#         from templates.campaign import campaign
#         campaignObj = campaign.Campaign(user_id=user_id)
#         view_campaign_data = campaignObj.get_all_campaigns()
#         for item in view_campaign_data['data']:
#             if item['deleted'] == 'true':
#                 view_campaign_data['data'].remove(item)
#         print('i m n search')
#         print('data=',data)
#         # print('fav list=',favInfList_data)
#         # exportCsv(data=data)
#         if channel_name == 'youtube':
#             for item in data['data']:
#                 total_videos_url = base_url + 'Youtube/totalVideos/' + str(item['channel_id'])
#                 try:
#                     response = requests.get(total_videos_url)
#                     total_videos = response.json()
#                     for item1 in total_videos['data']:
#                         item.update(item1)
#                     print(item)
#                 except:
#                     pass
#         if channel_name == 'twitter':
#             for item in data['data']:
#                 item.update({'total_videos': 100})
#         if channel_name == 'instagram':
#             for item in data['data']:
#                 item.update({'total_videos': 100})
#
#         return render_template('partnerships/influencerFavoritesList.html',data=data,view_campaign_data=view_campaign_data,channel_name=channel_name)
#     except Exception as e:
#         print(e)
#         pass
#         return render_template('partnerships/influencerFavoritesList.html',data=data,view_campaign_data=view_campaign_data,channel_name=channel_name)



@connecsiApp.route('/influencerFavoritesList/<string:channel_name>',methods=['GET','POST'])
@is_logged_in
def influencerFavoritesList(channel_name):
    data=''
    view_campaign_data=''
    subscriptionValue = getSubscriptionValues(str(session["user_id"]))
    export_count = 0
    feature_name = ''
    packageName=''
    countMessages=0
    countAddToFavorites=0
    countAlerts=0
    messageSubscription={
        'Export Lists':'',
        'Messages':'',
        'Add To Favorites':'',
        'Alerts':''
    }
    for i in subscriptionValue['data']:
        if (i['feature_name'].lower() == 'export lists'):
            export_count = i['units']
            feature_name = i['feature_name']
            packageName=i['package_name']
        if (i['feature_name'].lower() == 'messages'):
            countMessages = i['units']
            feature_name = i['feature_name']
            packageName=i['package_name']
        if (i['feature_name'].lower() == 'add to favorites'):
            countAddToFavorites = i['units']
            feature_name = i['feature_name']
            packageName = i['package_name']
        if (i['feature_name'].lower() == 'alerts'):
            countAlerts = i['units']
            feature_name = i['feature_name']
            packageName = i['package_name']
    messageSubscription['Export Lists'] = 'Your have less Export Lists units than the influencers in current export List. Add more in custom or upgrade your '+packageName+' package.'
    if (countAlerts == 0):
        messageSubscription['Alerts'] = "You ran out of Alerts Units of your " + subscriptionValue['data'][0][
            'package_name'] + " package. You can add more create campaigns in custom option or upgrade subscription."

    if (countAddToFavorites == 0):
        messageSubscription['Add to Favorites'] = "You ran out of Add to Favorites Units of your " + subscriptionValue['data'][0][
            'package_name'] + " package. You can add more create campaigns in custom option or upgrade subscription."

    if (export_count == 0):
        messageSubscription['Export Lists'] = "You ran out of Export List Units of your " + subscriptionValue['data'][0][
            'package_name'] + " package. You can add more create campaigns in custom option or upgrade subscription."
    if (export_count == -1):
        messageSubscription['Export Lists'] = "Your "+subscriptionValue['data'][0]['package_name']+" package doesn't have Export list feature. Please upgrade your package."

    if (countMessages == -1):
        messageSubscription[
            'Messages'] = "Your " + packageName + " package doesn't have this feature. Please Upgrade your subscription to use this feature."
    elif (countMessages == 0):
        messageSubscription[
            'Messages'] = "You ran out of Messages feature of " + packageName + " package. PLease add more in custom or upgrade your subscription."

    try:
        user_id = session['user_id']
        url = base_url+'/Brand/getInfluencerFavList_with_details/'+str(user_id)+'/'+channel_name
        response = requests.get(url=url)
        data = response.json()
        print(data)
        print(len(data))
        linechart_id = 1
        for item in data['data']:
            item.update({'linechart_id': linechart_id})
            item.update({'total_rows': len(data['data'])})
            linechart_id += 1
        from templates.campaign import campaign
        campaignObj = campaign.Campaign(user_id=user_id)
        view_campaign_data = campaignObj.get_all_campaigns()
        for item in view_campaign_data['data']:
            if item['deleted'] == 'true':
                view_campaign_data['data'].remove(item)
        print('i m n search')
        print('data=',data)
        # print('fav list=',favInfList_data)
        # exportCsv(data=data)
        if channel_name == 'youtube':
            for item in data['data']:
                total_videos_url = base_url + 'Youtube/totalVideos/' + str(item['channel_id'])
                try:
                    response = requests.get(total_videos_url)
                    total_videos = response.json()
                    for item1 in total_videos['data']:
                        item.update(item1)
                    print(item)
                except:
                    pass
        if channel_name == 'twitter':
            for item in data['data']:
                item.update({'total_videos': 100})
        if channel_name == 'instagram':
            for item in data['data']:
                item.update({'total_videos': 100})

        return render_template('partnerships/influencerFavoritesList.html',countAddToFavorites=countAddToFavorites,countAlerts=countAlerts,packageName=packageName,countMessages=countMessages,export_count=export_count,messageSubscription=messageSubscription,data=data,view_campaign_data=view_campaign_data,channel_name=channel_name)
    except Exception as e:
        print(e)
        pass
        return render_template('partnerships/influencerFavoritesList.html',countAddToFavorites=countAddToFavorites,countAlerts=countAlerts,packageName=packageName,countMessages=countMessages,export_count=export_count,messageSubscription=messageSubscription,data=data,view_campaign_data=view_campaign_data,channel_name=channel_name)




# @connecsiApp.route('/createAlerts', methods=['POST','GET'])
# @is_logged_in
# def createAlerts():
#     user_id=session['user_id']
#     if request.method == 'POST':
#         print("i m in post")
#         payload = request.form.to_dict()
#         print(payload)
#         try:
#             url = base_url + '/Brand/createInfluencerAlerts/'+str(user_id)
#             response = requests.put(url=url,json=payload)
#             # data = response.json()
#             return 'Created Alerts for Favorite Influencer'
#
#         except Exception as e:
#             print('i m in exception')
#             print(e)
#             return 'Server error'

@connecsiApp.route('/createAlerts', methods=['POST','GET'])
@is_logged_in
def createAlerts():
    print(' inside create alerts')
    user_id=session['user_id']
    if request.method == 'POST':
        print("i m in post")
        payload = request.form.to_dict()
        print(payload)
        try:
            url = base_url + '/Brand/createInfluencerAlerts/'+str(user_id)
            response = requests.put(url=url,json=payload)
            data = response.json()
            if(data['response']==1):
                check = subscriptionReduction("Alerts")
                if (check['response'] == 1):
                    print("done subscription ALERTS")
                    check1 = subscriptionReduction("Add to favorites")
                    if (check1['response'] == 1):
                        print("done subscription ADD TO FAVORITES")
            return 'Created Alerts for Favorite Influencer'

        except Exception as e:
            print('i m in exception')
            print(e)
            return 'Server error'



@connecsiApp.route('/createAlerts1', methods=['POST','GET'])
@is_logged_in
def createAlerts1():
    user_id=session['user_id']
    if request.method == 'POST':
        print("i m in post")
        payload = request.form.to_dict()
        print(payload)
        try:
            url = base_url + '/Brand/createInfluencerAlerts/'+str(user_id)
            response = requests.put(url=url,json=payload)
            data = response.json()
            return 'Created Alerts for Favorite Influencer'

        except Exception as e:
            print('i m in exception')
            print(e)
            return 'Server error'


# @connecsiApp.route('/addClassified')
# @is_logged_in
# def addClassified():
#     url_regionCodes = base_url + 'Youtube/regionCodes'
#     regionCodes_json = ''
#     try:
#         regionCodes_response = requests.get(url=url_regionCodes)
#         regionCodes_json = regionCodes_response.json()
#         print(regionCodes_json)
#     except:pass
#     url_videoCat = base_url + 'Youtube/videoCategories'
#     videoCat_json=''
#     try:
#         response_videoCat = requests.get(url=url_videoCat)
#         videoCat_json = response_videoCat.json()
#         print(videoCat_json)
#     except Exception as e:
#         print(e)
#     return render_template('classifiedAds/add_classifiedForm.html',regionCodes=regionCodes_json,videoCategories = videoCat_json)


@connecsiApp.route('/addClassified')
@is_logged_in
def addClassified():
    url_regionCodes = base_url + 'Youtube/regionCodes'
    regionCodes_json = ''
    subscriptionValue = getSubscriptionValues(str(session["user_id"]))
    classified_count = 0
    campaign_count=0
    feature_name = ''
    messageSubscription={
        'Create Campaign':'',
        'Classified Ads Posting':''
    }
    for i in subscriptionValue['data']:
        if (i['feature_name'].lower() == 'classified ads posting'):
            classified_count = i['units']
            feature_name = i['feature_name']
        elif(i['feature_name'].lower() == 'create campaign'):
            campaign_count=i['units']
    messageSubscription['Classified Ads Posting'] = "Your " + subscriptionValue['data'][0]['package_name'] + " package does not have Classified Ads Posting. You can upgrade subscription."
    if (campaign_count == 0):
        messageSubscription['Create Campaign'] = "You ran out of Create Campaign Units of your " + subscriptionValue['data'][0][
            'package_name'] + " package. Continue without posting it as a Campaign or just upgrade your subscription."

    if (classified_count == 0):
        messageSubscription['Classified Ads Posting'] = "You ran out of Classified Ads Posting Units of your " + subscriptionValue['data'][0]['package_name'] + " package. You can add more Classified Ads Posting in custom option or upgrade subscription."

    try:
        regionCodes_response = requests.get(url=url_regionCodes)
        regionCodes_json = regionCodes_response.json()
        print(regionCodes_json)
    except:pass
    url_videoCat = base_url + 'Youtube/videoCategories'
    videoCat_json=''
    try:
        response_videoCat = requests.get(url=url_videoCat)
        videoCat_json = response_videoCat.json()
        print(videoCat_json)
    except Exception as e:
        print(e)
    return render_template('classifiedAds/add_classifiedForm.html',campaign_count=campaign_count,classified_count=classified_count,messageSubscription=messageSubscription,regionCodes=regionCodes_json,videoCategories = videoCat_json)


# @connecsiApp.route('/saveClassified',methods=['POST'])
# @is_logged_in
# def saveClassified():
#     if request.method == 'POST':
#         payload = request.form.to_dict()
#
#         # post_as_campaign = 'post_as_campaign' in request.form
#         channels = request.form.getlist('channels')
#         channels_string = ','.join(channels)
#         payload.update({'channels':channels_string})
#
#         regions = request.form.getlist('country')
#         regions_string = ','.join(regions)
#         payload.update({'regions':regions_string})
#         # payload.update({"post_as_campaign": post_as_campaign})
#
#         arrangements = request.form.getlist('arrangements')
#         arrangements_string = ','.join(arrangements)
#         payload.update({'arrangements': arrangements_string})
#
#         kpis = request.form.getlist('kpis')
#         kpis_string = ','.join(kpis)
#         payload.update({'kpis': kpis_string})
#
#         convert_to_campaign = request.form.get('convert_to_campaign')
#         print('convert to campaign = ', convert_to_campaign)
#         try:
#             del payload['country']
#             del payload['convert_to_campaign']
#         except:
#             pass
#         print(payload)
#
#         files = request.files.getlist("campaign_files")
#         print(files)
#         # exit()
#         filenames = []
#         for file in files:
#             # filename = brands_classified_files.save(file)
#             filename = campaign_files.save(file)
#             print(filename)
#             filenames.append(filename)
#         filenames_string = ','.join(filenames)
#         payload.update({'files': filenames_string})
#         print(payload)
#
#         # exit()
#         if convert_to_campaign == 'on':
#             payload.update({'convert_to_campaign':'TRUE'})
#             print('payload inside if =',payload)
#             for file in files:
#                 campaign_files.save(file)
#             user_id = session['user_id']
#             campaign_url = base_url + 'Campaign/' + str(user_id)
#             print(campaign_url)
#             campaign_payload = copy.deepcopy(payload)
#             campaign_payload['campaign_name'] = campaign_payload.pop('classified_name')
#             campaign_payload['campaign_description'] = campaign_payload.pop('classified_description')
#             campaign_payload['is_classified_post'] = campaign_payload.pop('convert_to_campaign')
#             print('campaign_payload=',campaign_payload)
#             try:
#                 requests.post(url=campaign_url, json=campaign_payload)
#             except Exception as e:
#                 print(e)
#                 pass
#
#         else:
#             payload.update({'convert_to_campaign':'FALSE'})
#
#         user_id = session['user_id']
#         url = base_url + 'Classified/' + str(user_id)
#         print(url)
#         # return ''
#         try:
#             response = requests.post(url=url, json=payload)
#             result_json = response.json()
#             print(result_json)
#             flash('saved Classified', 'success')
#             return redirect(url_for("viewAllClassifiedAds"))
#             # return viewAllClassifiedAds()
#         except Exception as e:
#             print(e)
#             flash('Classified didnt saved Please try again later','danger')
#             return addClassified()
#
#     else:
#         flash('Unauthorized', 'danger')


@connecsiApp.route('/saveClassified',methods=['POST'])
@is_logged_in
def saveClassified():
    if request.method == 'POST':
        payload = request.form.to_dict()

        # post_as_campaign = 'post_as_campaign' in request.form
        channels = request.form.getlist('channels')
        channels_string = ','.join(channels)
        payload.update({'channels':channels_string})

        regions = request.form.getlist('country')
        regions_string = ','.join(regions)
        payload.update({'regions':regions_string})
        # payload.update({"post_as_campaign": post_as_campaign})

        arrangements = request.form.getlist('arrangements')
        arrangements_string = ','.join(arrangements)
        payload.update({'arrangements': arrangements_string})

        kpis = request.form.getlist('kpis')
        kpis_string = ','.join(kpis)
        payload.update({'kpis': kpis_string})

        convert_to_campaign = request.form.get('convert_to_campaign')
        print('convert to campaign = ', convert_to_campaign)
        try:
            del payload['country']
            del payload['convert_to_campaign']
        except:
            pass
        print(payload)

        files = request.files.getlist("campaign_files")
        print(files)
        # exit()
        filenames = []
        for file in files:
            if (file.filename):
                filename = campaign_files.save(file)
                filenames.append(filename)
        filenames_string = ','.join(filenames)
        payload.update({'files': filenames_string})
        print(payload)

        # exit()
        if convert_to_campaign == 'on':
            payload.update({'convert_to_campaign':'TRUE'})
            print('payload inside if =',payload)
            for file in files:
                if (file.filename):
                    campaign_files.save(file)
            user_id = session['user_id']
            campaign_url = base_url + 'Campaign/' + str(user_id)
            print(campaign_url)
            campaign_payload = copy.deepcopy(payload)
            campaign_payload['campaign_name'] = campaign_payload.pop('classified_name')
            campaign_payload['campaign_description'] = campaign_payload.pop('classified_description')
            campaign_payload['is_classified_post'] = campaign_payload.pop('convert_to_campaign')
            print('campaign_payload=',campaign_payload)
            try:
                requests.post(url=campaign_url, json=campaign_payload)
            except Exception as e:
                print(e)
                pass

        else:
            payload.update({'convert_to_campaign':'FALSE'})

        user_id = session['user_id']
        url = base_url + 'Classified/' + str(user_id)
        print(url)
        # return ''
        try:
            print('total classified ads values sent ',payload)
            response = requests.post(url=url, json=payload)
            result_json = response.json()
            print(result_json)
            check = subscriptionReduction("Classified Ads Posting")
            if (check['response'] == 1):
                print("done subscription classified ads posting")
                if (payload['convert_to_campaign'] == 'TRUE'):
                    check1 = subscriptionReduction("Create Campaign")
                    if (check1['response'] == 1):
                        print("done subscription classified ads posting with create campaign")
            flash('saved Classified', 'success')
            #return redirect(url_for("viewAllClassifiedAds"))
            return viewAllClassifiedAds()
        except Exception as e:
            print(e)
            flash('Classified didnt saved Please try again later','danger')
            return addClassified()

    else:
        flash('Unauthorized', 'danger')




@connecsiApp.route('/editClassified/<string:classified_id>',methods=['GET'])
@is_logged_in
def editClassified(classified_id):
    url_regionCodes = base_url + 'Youtube/regionCodes'
    regionCodes_json = ''
    try:
        regionCodes_response = requests.get(url=url_regionCodes)
        regionCodes_json = regionCodes_response.json()
        # print(regionCodes_json)
    except:
        pass
    url_videoCat = base_url + 'Youtube/videoCategories'
    videoCat_json = ''
    try:
        response_videoCat = requests.get(url=url_videoCat)
        videoCat_json = response_videoCat.json()
        # print(videoCat_json)
    except Exception as e:
        print(e)
    print(classified_id)
    user_id = session['user_id']
    from templates.classifiedAds.classified import Classified
    classifiedObj = Classified(user_id=user_id, classified_id=classified_id)
    classified_details = classifiedObj.get_classified_details()
    print(classified_details)
    try:
        for item in classified_details['data']:
            item['from_date'] = datetime.datetime.strptime(item['from_date'],'%d-%b-%y').date()
            item['to_date'] = datetime.datetime.strptime(item['to_date'], '%d-%b-%y').date()
            item['arrangements'] = item['arrangements'].replace('/', '')
            item['arrangements'] = item['arrangements'].replace(' ', '')
            item['kpis'] = item['kpis'].replace(' ', '')
    except Exception as e:
        print(e)
    return render_template('classifiedAds/edit_classifiedForm.html', view_classified_details_data=classified_details,
                           regionCodes=regionCodes_json, videoCategories=videoCat_json)



@connecsiApp.route('/updateClassified',methods=['POST'])
@is_logged_in
def updateClassified():
    if request.method == 'POST':
        payload = request.form.to_dict()
        # print('payload = ',payload)
        classified_id = request.form.get('classified_id')
        # exit
        del payload['classified_id']
        # print(payload)
        # print(campaign_id)
        # exit()
        channels = request.form.getlist('channels')
        channels_string = ','.join(channels)
        payload.update({'channels':channels_string})
        regions = request.form.getlist('country')
        regions_string = ','.join(regions)
        payload.update({'regions':regions_string})


        arrangements = request.form.getlist('arrangements')
        arrangements_string = ','.join(arrangements)
        payload.update({'arrangements': arrangements_string})

        kpis = request.form.getlist('kpis')
        kpis_string = ','.join(kpis)
        payload.update({'kpis': kpis_string})

        convert_to_campaign = request.form.get('convert_to_campaign')
        # print('is classified = ',is_classified_post)
        try:
            del payload['country']
            del payload['convert_to_campaign']
        except:pass
        if convert_to_campaign == 'on':
            payload.update({'convert_to_campaign':'TRUE'})
        else:
            payload.update({'convert_to_campaign':'FALSE'})
        files = request.files.getlist("campaign_files")
        # print(files)
        # exit()
        filenames=[]
        for file in files:
            # filename = brands_classified_files.save(file)
            filename = campaign_files.save(file)
            filenames.append(filename)


        user_id = session['user_id']
        url_classified = base_url + 'Classified/' + str(classified_id) + '/' + str(user_id)
        response_classified = requests.get(url=url_classified)
        result_json_classified = response_classified.json()
        # print('cam data',result_json_campaign)

        for item in result_json_classified['data']:
            files_string = item['files']
            print(files_string)
            if files_string:
               filenames.append(files_string)

        filenames_string = ','.join(filenames)
        print('file name string', filenames_string)
        payload.update({'files': filenames_string})

        print('last payload',payload)

        if convert_to_campaign == 'on':
            payload.update({'convert_to_campaign':'TRUE'})
            print('payload inside if =',payload)
            for file in files:
                campaign_files.save(file)
            user_id = session['user_id']
            campaign_url = base_url + 'Campaign/' + str(user_id)
            print(campaign_url)
            campaign_payload = copy.deepcopy(payload)
            campaign_payload['campaign_name'] = campaign_payload.pop('classified_name')
            campaign_payload['campaign_description'] = campaign_payload.pop('classified_description')
            campaign_payload['is_classified_post'] = campaign_payload.pop('convert_to_campaign')
            print('campaign_payload=',campaign_payload)
            try:
                requests.post(url=campaign_url, json=campaign_payload)
            except Exception as e:
                print(e)
                pass

        else:
            payload.update({'convert_to_campaign':'FALSE'})

        # exit()
        url = base_url + 'Classified/'+str(classified_id)+'/' + str(user_id)
        print(url)
        try:
            response = requests.put(url=url, json=payload)
            result_json = response.json()
            print(result_json)
            flash('Updated Classified', 'success')
            return viewAllClassifiedAds()
        except Exception as e:
            print(e)
            flash('campaign didnt saved Please try again later','danger')
            pass
    else:
        flash('Unauthorized', 'danger')


@connecsiApp.route('/deleteClassified/<string:classified_id>',methods=['GET'])
@is_logged_in
def deleteClassified(classified_id):
    print(classified_id)
    user_id= session['user_id']
    url = base_url + 'Classified/' + str(classified_id) + '/' + str(user_id)
    print(url)
    try:
        response = requests.delete(url=url)
        result_json = response.json()
        print(result_json)
        # res = requests.put(url=base_url + 'Campaign/update_campaign_status/' + str(campaign_id) + '/' + 'InActive')
        flash('Deleted Campaign', 'success')
        return viewAllClassifiedAds()
    except Exception as e:
        print(e)
        flash('Please try again later', 'danger')
        pass

@connecsiApp.route('/deletedClassifieds',methods=['GET','POST'])
@is_logged_in
def deletedClassifieds():
    user_id=session['user_id']
    # import templates
    from templates.classifiedAds.classified import Classified
    classifiedObj = Classified(user_id=user_id)
    all_classified_data = classifiedObj.get_all_classifieds()
    deleted_classified_list = []
    for item in all_classified_data['data']:
        if item['deleted'] =='true':
            deleted_classified_list.append(item)

    print(deleted_classified_list)
    return render_template('classifiedAds/deleted_classifieds.html',view_classified_data=deleted_classified_list)




def exportCsv(data):
    print('my data = ', data)
    print(os.getcwd())
    cwd = os.getcwd()
    with open(cwd+'/static/infList.csv', mode='w') as csv_file:
    # with open(cwd+'/infList.csv', mode='w') as csv_file:
        fieldnames = ['Channel Name', 'Total Followers', 'Avg Views/video','Avg Likes/video','Avg Comments/video']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # writer.writerow(myDict)
        for item in data['data']:
            # print(item['title'])
            writer.writerow({'Channel Name': item['title'], 'Total Followers': item['subscriberCount_gained'], 'Avg Views/video': item['total_100video_views']/100,'Avg Likes/video':item['total_100video_likes']/100,'Avg Comments/video':item['total_100video_comments']/100})

# @connecsiApp.route('/viewAllClassifiedAds',methods=['GET','POST'])
# @is_logged_in
# def viewAllClassifiedAds():
#     user_id=session['user_id']
#     from templates.classifiedAds.classified import Classified
#     classifiedObj = Classified(user_id=user_id)
#     all_classified_data = classifiedObj.get_all_classifieds()
#     view_classified_data_list = []
#     for item in all_classified_data['data']:
#         if item['deleted'] != 'true':
#             view_classified_data_list.append(item)
#     print(view_classified_data_list)
#
#     view_profile_url = base_url + 'Brand/' + str(user_id)
#     response = requests.get(view_profile_url)
#     profile_data_json = response.json()
#     print(profile_data_json)
#
#     return render_template('classifiedAds/view_all_classifiedAds.html',all_classified_data=view_classified_data_list,profile_data=profile_data_json)


@connecsiApp.route('/viewAllClassifiedAds',methods=['GET','POST'])
@is_logged_in
def viewAllClassifiedAds():
    user_id=session['user_id']
    from templates.classifiedAds.classified import Classified
    classifiedObj = Classified(user_id=user_id)
    subValues=getSubscriptionValues(str(user_id))
    countClassified=0
    messageSubscription = {
        'Classified Ads Posting': ''
    }
    for i in subValues['data']:
        print(i['feature_name'])
        if (i['feature_name'].lower() == 'classified ads posting'):
            countClassified = i['units']
            packageName = i['package_name']
            feature_name=i['feature_name']


    if (countClassified == -1):
        messageSubscription['Classified Ads Posting'] = "Your " + packageName + " package doesn't have this feature. Please Upgrade your subscription to use this feature."
    elif (countClassified == 0):
        messageSubscription['Classified Ads Posting'] = "You ran out of "+feature_name+" feature of " + packageName + " package. PLease add more in custom or upgrade your subscription."

    all_classified_data = classifiedObj.get_all_classifieds()
    view_classified_data_list = []
    for item in all_classified_data['data']:
        if item['deleted'] != 'true':
            view_classified_data_list.append(item)
    print(view_classified_data_list)

    view_profile_url = base_url + 'Brand/' + str(user_id)
    response = requests.get(view_profile_url)
    profile_data_json = response.json()
    print(profile_data_json)
    return render_template('classifiedAds/view_all_classifiedAds.html',countClassified=countClassified,messageSubscription=messageSubscription,all_classified_data=view_classified_data_list,profile_data=profile_data_json)

@connecsiApp.route('/viewClassifiedDetails/<string:classified_id>')
@is_logged_in
def viewClassifiedDetails(classified_id):
    user_id=session['user_id']
    # user_id = ''
    from templates.classifiedAds.classified import Classified
    classifiedObj = Classified(user_id=user_id,classified_id=classified_id)
    classified_details = classifiedObj.get_classified_details()
    print(classified_details)
    for item in classified_details['data']:
        print(item)
        user_id= item['user_id']
        print(user_id)
    view_profile_url = base_url + 'Brand/' + str(user_id)
    response = requests.get(view_profile_url)
    profile_data_json = response.json()
    print(profile_data_json)

    return render_template('classifiedAds/viewClassifiedDetails.html',classified_details=classified_details,profile_data=profile_data_json)

@connecsiApp.route('/addYoutubeInfToCampaignList',methods=['POST'])
@is_logged_in
def addYoutubeInfToCampaignList():
    if request.method == 'POST':
        campaign_ids = request.form.getlist('campaign_id')
        channel_id = request.form.get('channel_id')
        channel_name=request.form.get('channel_name')
        if campaign_ids:
            for campaign_id in campaign_ids:
                url = base_url+'Brand/addInfToCampaignList/'+ str(channel_id) + '/' + str(campaign_id)+'/'+channel_name
                response = requests.post(url=url)
                response = response.json()
                # flash('Youtube Influencer Added to Campaign','success')
            # return viewCampaigns()
            return channel_name+' Influencer Added to Campaign'
        else: return  'Your Campaign List is Empty'

@connecsiApp.route('/getChannelStatusForCampaign/<string:channel_id>',methods=['GET'])
@is_logged_in
def getChannelStatusForCampaign(channel_id):
    print(channel_id)
    url=base_url+'Campaign/channel_status_for_campaign/'+str(channel_id)
    print(url)
    try:
        channel_status_for_campaign = requests.get(url=url)
        response_json = channel_status_for_campaign.json()
        print(response_json)
        return jsonify(results=response_json['data'])
    except Exception as e:
        print(e)


@connecsiApp.route('/channel_status_for_campaign_by_channel_id_and_campaign_id/<string:channel_id>/<string:campaign_id>',methods=['GET'])
@is_logged_in
def channel_status_for_campaign_by_channel_id_and_campaign_id(channel_id,campaign_id):
    print(channel_id)
    print(campaign_id)
    url=base_url+'Campaign/channel_status_for_campaign_by_channel_id_and_campaign_id/'+str(channel_id)+'/'+str(campaign_id)
    print(url)
    try:
        channel_status_for_campaign = requests.get(url=url)
        response_json = channel_status_for_campaign.json()
        print(response_json)
        return jsonify(results=response_json['data'])
    except Exception as e:
        print(e)

@connecsiApp.route('/getChannelStatusForCampaignByCampaignId/<string:campaign_id>',methods=['GET'])
@is_logged_in
def getChannelStatusForCampaignByCampaignId(campaign_id):
    print(campaign_id)
    url=base_url+'Campaign/channel_status_for_campaign_by_campaign_id/'+str(campaign_id)
    print(url)
    try:
        channel_status_for_campaign = requests.get(url=url)
        response_json = channel_status_for_campaign.json()
        print(response_json)
        return jsonify(results=response_json['data'])
    except Exception as e:
        print(e)




@connecsiApp.route('/delFavInf/<string:channel_id>/<string:user_id>',methods=['GET'])
def delFavInf(channel_id,user_id):
        print(channel_id)
        url = base_url+'Brand/deleteFromFavList/'+ str(channel_id) + '/' + str(user_id)
        print(url)
        response = requests.post(url=url)
        response = response.json()
        print(response)
        if response['response']==1:
            return 'Influencer Removed From Favourite List'
        else: return 'Server Error'



@connecsiApp.route('/saveBrandReport',methods = ['POST'])
@is_logged_in
def saveBrandReport():
    if request.method == 'POST':

       user_id = session['user_id']
       campaign_id = request.form.get('campaign_id')
       channel_id_list = request.form.getlist('channel_id')
       revenue_list = request.form.getlist('revenue')
       new_users_list = request.form.getlist('new_users')
       currency_list = request.form.getlist('currency')
       zip_list = list(zip(revenue_list,new_users_list,currency_list,channel_id_list))
       print(zip_list)
       for item in zip_list:
           try:
                channels_list = item[3].split('@')
                payload = {'revenue_generated':item[0],'new_users':item[1],'currency':item[2],'channel_id':channels_list[1],'channel':channels_list[0]}
                url = base_url + 'Campaign/BrandCampaignReport/' + str(user_id) + '/' + str(campaign_id)
                print(payload)
                response = requests.post(url=url, json=payload)
                data = response.json()
           except Exception as e:
               print(e)
               pass
               return 'server error'
       return 'Added Report'


@connecsiApp.route('/updateBrandReport',methods = ['POST'])
@is_logged_in
def updateBrandReport():
    if request.method == 'POST':
       user_id = session['user_id']
       campaign_id = request.form.get('campaign_id')
       channel_id_list = request.form.getlist('channel_id')
       revenue_list = request.form.getlist('revenue')
       new_users_list = request.form.getlist('new_users')
       currency_list = request.form.getlist('currency')
       zip_list = list(zip(revenue_list,new_users_list,currency_list,channel_id_list))
       print(zip_list)
       # exit()
       #
       for item in zip_list:
           try:
                payload = {'revenue_generated':item[0],'new_users':item[1],'currency':item[2]}
                url = base_url + 'Campaign/BrandCampaignReport/Update/' + str(campaign_id) + '/' + str(item[3])
                print('payload = ',payload)
                print(url)
                response = requests.put(url=url, json=payload)
                data = response.json()
           except Exception as e:
               print(e)
               pass
               return 'server error'
       return 'Updated Report'

@connecsiApp.route('/getBrandReport/<string:campaign_id>',methods = ['GET'])
@is_logged_in
def getBrandReport(campaign_id):
    print('cam=',campaign_id)

    user_id = session['user_id']
    url = base_url+'Campaign/BrandCampaignReport/'+str(user_id)+'/'+str(campaign_id)
    print(url)
    try:
        bcr_data = requests.get(url=url)
        response_json = bcr_data.json()
        print(response_json)
        return jsonify(results=response_json['data'])
    except Exception as e:
        print(e)
        return 'server error'

@connecsiApp.route('/getBrandReportByCampaignIdAndChannelIds/<string:campaign_id>/<string:proposal_channels>',methods = ['GET'])
@is_logged_in
def getBrandReportByCampaignIdAndChannelIds(campaign_id,proposal_channels):
    print('cam=',campaign_id)
    print(proposal_channels)
    user_id = session['user_id']
    url = base_url + 'Campaign/BrandCampaignReport/' + str(user_id) + '/' + str(campaign_id)
    bcr_data = requests.get(url=url)
    bcr_response_json = bcr_data.json()
    print('bcr report = ',bcr_response_json)
    # exit()
    bcr_dict = {'data': ''}
    data=[]
    channel_id_list = proposal_channels.split(',')
    for channel in channel_id_list:
        channel_id_final = channel.split('@')
        for item in bcr_response_json['data']:
            if item['channel_id']==channel_id_final[1]:
                data.append(item)

    bcr_dict.update({'data':data})
    return jsonify(results=bcr_dict['data'])


@connecsiApp.route('/delBrandReport/<string:campaign_id>/<string:proposal_channels>',methods = ['GET'])
@is_logged_in
def delBrandReport(campaign_id,proposal_channels):
    print('campaign_id=',campaign_id)
    print(proposal_channels)
    channel_id_list= proposal_channels.split(',')
    for channel in channel_id_list:
        channel_id_final=channel.split('@')
        url = base_url+'Campaign/BrandCampaignReport/Delete/'+str(campaign_id)+'/'+str(channel_id_final[1])
        print(url)
        bcr_data = requests.delete(url=url)
    return 'Report deleted'




@connecsiApp.route('/reports')
@is_logged_in
def reports():
    return render_template('reports/reports.html')


############################################## influencer Section###########################################################
@connecsiApp.route('/getMappedChannels/<string:channel_id>', methods=['get'])
@is_logged_in
def getMappedChannels(channel_id):
    print(channel_id)
    # url = base_url + 'Influencer/' + str(channel_id)

    # print(url)
    try:
        # mappedChannel_ids = requests.get(url=url)
        mappedChannel_ids = requests.get(url=base_url + 'Influencer/getDetailsByUserId/' + str(channel_id))
        response_json = mappedChannel_ids.json()
        print(response_json)
        return jsonify(results=response_json['data'])
    except Exception as e:
        print(e)




from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
# os.environ['WERKZEUG_RUN_MAIN'] = 'true'


google_blueprint = make_google_blueprint(
    client_id = "493258682854-ubb1m8e59t5teebtj3lclllb04j4dn0t.apps.googleusercontent.com",
    client_secret="tFk1KLwBXpwaIJOUIYQwgpWZ",
    # client_id="413672402805-dvv0v7bft07iqhj2du2eqq59itbeqcv1.apps.googleusercontent.com",
    # client_secret="wNxRXqxGrz7inj2yE2nlgcyO",

    # scope=[
        # "https://www.googleapis.com/auth/plus.me",
        # "https://www.googleapis.com/auth/userinfo.email",
        # "https://www.googleapis.com/auth/youtube.readonly"
    # ],
scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/youtube.readonly",
        # "https://www.googleapis.com/auth/yt-analytics.readonly"
    ],
    offline=True,
    reprompt_consent=True,
    redirect_to='google_login',
)

twitter_blueprint = make_twitter_blueprint(
    api_key="lOhkeJRZhYXvkm0lYq1ZgTtYa",
    api_secret="TbMKSZBbcqhnedjjqG66JuStxunBdKLelfjgxTW4UNJndbatJa",
    redirect_to='twitter_login'
)
connecsiApp.register_blueprint(google_blueprint, url_prefix="/login")
connecsiApp.register_blueprint(twitter_blueprint, url_prefix="/login")


@connecsiApp.route("/google_login")
def google_login():
    print('i m here in google_login()')
    if not google.authorized:
        print('i m here always')
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    # resp = google.get("/oauth2/v2/youtube.readonly")
    url = 'https://www.googleapis.com/youtube/v3/channels?part=statistics,id,snippet,contentOwnerDetails,status&mine=true'
    channel_data = google.get(url).json()
    print('channel details = ',channel_data)
    print(resp.json())
    print(google.authorized)
    print(google_blueprint.backend)
    # exit()
    resp_json = resp.json()
    payload = {}
    channel_id=channel_data['items'][0]['id']
    title = channel_data['items'][0]['snippet']['title']
    description = channel_data['items'][0]['snippet']['description']
    # print(channel_id)
    payload.update({'channel_id':channel_id,'business_email':resp_json['email']})
    url = base_url+'Influencer/saveInfluencer'
    print(url)
    try:
        response = requests.post(url,json=payload)
        print(response.json())
        response_json = response.json()
        if response_json['response'] == 1:

            youtube_url = base_url + 'Youtube/addYoutubeChannel/' + channel_id + '/' + resp_json['email']
            try:
                requests.post(url=youtube_url)
            except Exception as e:
                print(e)
                pass

            email_content = welcomemail_inf()
            payload1 = {
                "from_email_id": "business@connecsi.com",
                "to_email_id": resp_json['email'],
                "date": datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"),
                "subject": "Welcome To Connecsi",
                "message": "'"+email_content+"'"
            }
            user_id = 1
            type = 'brand'
            url = base_url + 'Messages/sentWelcomeEmail/' + str(user_id) + '/' + type
            try:
                response = requests.post(url=url, json=payload1)
                data = response.json()
                print('email sent')
            except:
                pass

        ##### code for OAUTH channel updates ############
        else:
            print('indluencer already present in youtube channel details get OAUTH to update the details')
        #################################################
    except Exception as e:
        print(e)
        pass
    # assert resp.ok, resp.text
    if resp.ok:
        user_id = channel_id
        print(user_id)
        # exit()
        if user_id:
            flash("logged in", 'success')
            session['logged_in'] = True
            session['email_id'] = resp_json['email']
            session['type'] = 'influencer'
            session['user_id'] = user_id
            print(session['user_id'])
            return redirect(url_for('admin_inf'))
    else:return redirect(url_for('login'))


# from twitterAnalyticsOauthKiranLib import TwitterAnalyticsOauthKiranLib
# @connecsiApp.route('/twitter_oauth')
# def twitter_oauth():
#     CALLBACK_URL = request.url_root+'twitter_callback_url'
#     print(CALLBACK_URL)
    # twitter_kiran_lib = TwitterAnalyticsOauthKiranLib()
    # twitter_kiran_lib.get_bearer_token()
    # return 'i m here'

from birdy.twitter import UserClient
@connecsiApp.route('/twitter_oauth')
def twitter_oauth():
    # CALLBACK_URL = request.url_root+'twitter_callback_url'
    CONSUMER_KEY = 'lOhkeJRZhYXvkm0lYq1ZgTtYa'
    CONSUMER_SECRET = 'TbMKSZBbcqhnedjjqG66JuStxunBdKLelfjgxTW4UNJndbatJa'
    CALLBACK_URL = request.url_root + 'twitter_callback_url'
    client = UserClient(CONSUMER_KEY, CONSUMER_SECRET)
    token = client.get_authorize_token(CALLBACK_URL)
    print(token)
    OAUTH_TOKEN = token.oauth_token
    OAUTH_TOKEN_SECRET = token.oauth_token_secret
    AUTH_URL = token.auth_url
    print(OAUTH_TOKEN)
    print(OAUTH_TOKEN_SECRET)
    print(AUTH_URL)
    session['twitter_oauth_token']=OAUTH_TOKEN
    session['twitter_oauth_token_secret'] = OAUTH_TOKEN_SECRET
    return redirect(AUTH_URL)

@connecsiApp.route('/twitter_callback_url')
def twitter_callback_url():
    OAUTH_VERIFIER = request.args.get('oauth_verifier')
    print(OAUTH_VERIFIER)
    CONSUMER_KEY = 'lOhkeJRZhYXvkm0lYq1ZgTtYa'
    CONSUMER_SECRET = 'TbMKSZBbcqhnedjjqG66JuStxunBdKLelfjgxTW4UNJndbatJa'
    client = UserClient(CONSUMER_KEY, CONSUMER_SECRET,session['twitter_oauth_token'], session['twitter_oauth_token_secret'])

    token = client.get_access_token(OAUTH_VERIFIER)
    print(token)
    FINAL_ACCESS_TOKEN = token.oauth_token
    FINAL_ACCESS_TOKEN_SECRET = token.oauth_token_secret
    twitter_id = token.user_id
    screen_name = token.screen_name
    print(FINAL_ACCESS_TOKEN)
    print(FINAL_ACCESS_TOKEN_SECRET)

    add_credentials_url = base_url + 'Influencer/influencerTwitterAnalyticsCredentials/' + str(twitter_id)
    try:
        print('i m inside try')
        json_post_data = {
            'access_token': FINAL_ACCESS_TOKEN,
            'access_token_secret': FINAL_ACCESS_TOKEN_SECRET,
            'screen_name':screen_name
        }
        res = requests.post(url=add_credentials_url, json=json_post_data)
        print('added/updated credentials')
    except:
        print('error while adding or updating credentials')
        pass
    response = client.api.statuses.home_timeline.get()
    # print(response.data)
    return 'i m here'



@connecsiApp.route("/twitter_login")
def twitter_login():
    if not twitter.authorized:
        return redirect(url_for("twitter.login"))
    resp = twitter.get("account/verify_credentials.json?include_email=true")

    print(resp.json())
    # exit()
    resp_json = resp.json()
    # screen_name = resp_json['screen_name']
    # user_data = twitter.get('users/show.json?screen_name=' +screen_name)
    # assert resp.ok, resp.text
    # print(user_data.json())
    # payload = {}
    channel_id = resp_json['id_str']
    screen_name = resp_json['screen_name']
    # payload.update({'channel_id': channel_id, 'business_email': resp_json['email']})
    twitter_url = base_url+'Twitter/addTwitterChannel/'+screen_name+'/'+resp_json['email']+'/'+session['user_id']
    print(twitter_url)
    try:
        requests.post(url=twitter_url)
        return redirect(url_for("inf_editProfile"))
    except Exception as e:
        print(e)
        pass
        return redirect(url_for("inf_editProfile"))


@connecsiApp.route('/add_insta_channel',methods=['GET','POST'])
@is_logged_in
def add_insta_channel():
    if request.method == 'POST':
        payload = request.form.to_dict()
        insta_username = request.form.get('insta_username')
        email_id = request.form.get('email_id')
        user_id=session['user_id']
        print(insta_username)
        print(email_id)
        print(user_id)
        add_insta_channel_url = base_url + 'Insta/addInstagramChannel/' + insta_username + '/' + email_id + '/' + user_id
        print(add_insta_channel_url)
        try:
            requests.post(url=add_insta_channel_url)
            return 'Successfully Added Instagram Channel'
        except Exception as e:
            print(e)
            pass
            return 'Server error Please try again later'


@connecsiApp.route('/admin_inf')
@is_logged_in
def admin_inf():
    title='Influencer Dashboard'
    # url = 'https://www.googleapis.com/youtube/v3/channels?part=statistics,id,snippet,contentOwnerDetails,status&mine=true'
    # channel_data = google.get(url).json()

    # print('channel details = ', channel_data)
    return render_template('index_inf.html',title=title)

@connecsiApp.route('/inf_profile')
@is_logged_in
def inf_profile():
    user_id = session['user_id']
    response = requests.get(url=base_url+'Influencer/getDetailsByUserId/'+str(user_id))
    profile_data = response.json()
    print(profile_data)
    return render_template('user/inf_profile.html',data=profile_data)

@connecsiApp.route('/inf_editProfile')
@is_logged_in
def inf_editProfile():
    user_id = session['user_id']
    # regionCodes_json=''
    videoCat_json=''
    response = requests.get(url=base_url + 'Influencer/getDetailsByUserId/' + str(user_id))
    profile_data = response.json()
    print(profile_data)
    try:
        url_regionCodes = base_url + 'Youtube/regionCodes'
        response_regionCodes = requests.get(url=url_regionCodes)
        regionCodes_json = response_regionCodes.json()
        print(regionCodes_json['data'])
    except Exception as e:
        print(e)

    try:
        url_videoCat = base_url + 'Youtube/videoCategories'
        response_videoCat = requests.get(url=url_videoCat)
        videoCat_json = response_videoCat.json()
        print(videoCat_json)
    except Exception as e:
        print(e)

    return render_template('user/inf_editprofile.html',data=profile_data,videoCat=videoCat_json,regionCodes=regionCodes_json)

@connecsiApp.route('/updateProfile_inf',methods=['POST'])
@is_logged_in
def updateProfile_inf():
    user_id = session['user_id']
    if request.method == 'POST':
        url = base_url+ 'Influencer/'+str(user_id)
        payload = request.form.to_dict()
        youtube_video_categories = request.form.getlist('categories')

        categories_string = ','.join(youtube_video_categories)
        payload.update({'categories':categories_string})
        try:
            del payload['video_cat']
        except:pass
        print(payload)
        # return ''
        try:
            response = requests.put(url=url,json=payload)
            result_json = response.json()
            # res_mapped_channels = requests.get(url=base_url + 'Influencer/getMappedChannels/' + str(user_id))
            res_inf_details = requests.get(url=base_url + 'Influencer/getDetailsByUserId/' + str(user_id))
            res_inf_details_json = res_inf_details.json()
            print(res_inf_details_json)
            for item in youtube_video_categories:
                print(item)
                res = requests.get(url=base_url+'Influencer/addCategoriesToChannel/'+str(user_id)+'/'+str(item))
                for inf_dict in res_inf_details_json['data']:
                    # print(channel_id['twitter_channel_id'])
                    if 'mapped_twitter_channel_id' in inf_dict  :
                       print('inside twitter channel id')
                       res = requests.get(url=base_url + 'Influencer/addCategoriesToTwitterChannel/' + str(inf_dict['mapped_twitter_channel_id']) + '/' + str(item))
                    if 'mapped_insta_channel_id' in inf_dict:
                       print('inside insta channel id')
                       res = requests.get(url=base_url + 'Influencer/addCategoriesToInstaChannel/' + str(inf_dict['mapped_insta_channel_id']) + '/' + str(item))
                print(res.json())

            for inf_dict in res_inf_details_json['data']:
                country = ''
                if 'youtube_country' in inf_dict:
                    country = inf_dict['youtube_country']
                if 'mapped_twitter_channel_id' in inf_dict:
                    print('inside twitter channel id')
                    res = requests.get(url=base_url + 'Influencer/updateCountryToTwitterChannel/' + str(inf_dict['mapped_twitter_channel_id']) + '/' + str(country))
                if 'mapped_insta_channel_id' in inf_dict:
                    print('inside insta channel id')
                    res = requests.get(url=base_url + 'Influencer/updateCountryToInstaChannel/' + str(inf_dict['mapped_insta_channel_id']) + '/' + str(country))
            return redirect(url_for("inf_editProfile"))
        except Exception as e:
            print(e)
            pass
            # return ''
            return redirect(url_for("inf_editProfile"))

@connecsiApp.route('/addOffer')
@is_logged_in
def addOffer():
    url_regionCodes = base_url + 'Youtube/regionCodes'
    regionCodes_json = ''
    try:
        regionCodes_response = requests.get(url=url_regionCodes)
        regionCodes_json = regionCodes_response.json()
        print(regionCodes_json)
    except:
        pass
    url_videoCat = base_url + 'Youtube/videoCategories'
    videoCat_json = ''
    try:
        response_videoCat = requests.get(url=url_videoCat)
        videoCat_json = response_videoCat.json()
        print(videoCat_json)
    except Exception as e:
        print(e)
    return render_template('offers/add_offerForm.html', regionCodes=regionCodes_json,
                           videoCategories=videoCat_json)

@connecsiApp.route('/saveOffer', methods=['POST'])
@is_logged_in
def saveOffer():
    if request.method == 'POST':
        payload = request.form.to_dict()
        channels = request.form.getlist('channels')
        channels_string = ','.join(channels)
        payload.update({'channels': channels_string})

        regions = request.form.getlist('country')
        regions_string = ','.join(regions)
        payload.update({'regions': regions_string})

        arrangements = request.form.getlist('arrangements')
        arrangements_string = ','.join(arrangements)
        payload.update({'arrangements': arrangements_string})

        kpis = request.form.getlist('kpis')
        kpis_string = ','.join(kpis)
        payload.update({'kpis': kpis_string})

        try:
            del payload['country']
        except:
            pass
        # print(payload)

        files = request.files.getlist("campaign_files")
        print(files)
        # exit()
        filenames = []
        for file in files:
            filename = offer_files.save(file)
            print(filename)
            filenames.append(filename)
        filenames_string = ','.join(filenames)
        payload.update({'files': filenames_string})
        print('final offer payload = ',payload)

        user_id = session['user_id']
        url = base_url + 'Offer/' + str(user_id)
        print(url)
        # exit()
        # return ''
        try:
            response = requests.post(url=url, json=payload)
            result_json = response.json()
            print(result_json)
            flash('saved Offer', 'success')
            return viewAllOffers()
            # return 'offer added'
        except Exception as e:
            print(e)
            flash('Offer didnt saved Please try again later', 'danger')
            return addOffer()
            # return 'offer not added'

    else:
        flash('Unauthorized', 'danger')

@connecsiApp.route('/viewAllOffers', methods=['GET', 'POST'])
@is_logged_in
def viewAllOffers():
    user_id = session['user_id']
    from templates.offers.offer import Offer
    offerObj = Offer(user_id=user_id)
    all_offer_data = offerObj.get_all_offers()
    print('all off data = ',all_offer_data)
    view_offer_data_list = []
    for item in all_offer_data['data']:
        if item['deleted'] != 'true':
            view_offer_data_list.append(item)
    print('list = ',view_offer_data_list)

    view_profile_url = base_url + 'Influencer/getDetailsByUserId/' + str(user_id)
    response = requests.get(view_profile_url)
    profile_data_json = response.json()
    print(profile_data_json)

    return render_template('offers/view_all_offer.html',
                           all_offer_data=view_offer_data_list, profile_data=profile_data_json)

# @connecsiApp.route('/viewOfferDetails/<string:offer_id>')
# @is_logged_in
# def viewOfferDetails(offer_id):
#     user_id = session['user_id']
#     print(user_id)
#     channel_id=''
#     from templates.offers.offer import Offer
#     offerObj = Offer(user_id=user_id, offer_id=offer_id)
#     offer_details = offerObj.get_offer_details()
#     print(offer_details)
#     for item in offer_details['data']:
#         channel_id=item['channel_id']
#     view_profile_url = base_url + 'Influencer/getDetailsByUserId/' + str(channel_id)
#     response = requests.get(view_profile_url)
#     profile_data_json = response.json()
#     print(profile_data_json)
#
#     return render_template('offers/viewOfferDetails.html', offer_details=offer_details,
#                            profile_data=profile_data_json)


@connecsiApp.route('/viewOfferDetails/<string:offer_id>')
@is_logged_in
def viewOfferDetails(offer_id):
    user_id = session['user_id']
    subscriptionValue = getSubscriptionValues(str(session["user_id"]))
    custom_offers_reply_count = 0
    feature_name = ''
    messageSubscription = {
        'Custom Offers Reply':''
    }
    for i in subscriptionValue['data']:
        if (i['feature_name'].lower() == 'custom offers reply'):
            custom_offers_reply_count = i['units']
            feature_name = i['feature_name']
    if (custom_offers_reply_count == 0):
        messageSubscription['Custom Offer Reply'] = "You ran out of " + feature_name + " Units of your " + subscriptionValue['data'][0][
            'package_name'] + " package. Add more units in custom or upgrade your package."
    print(user_id)
    channel_id=''
    from templates.offers.offer import Offer
    offerObj = Offer(user_id=user_id, offer_id=offer_id)
    offer_details = offerObj.get_offer_details()
    print(offer_details)
    for item in offer_details['data']:
        channel_id=item['channel_id']
    view_profile_url = base_url + 'Influencer/getDetailsByUserId/' + str(channel_id)
    response = requests.get(view_profile_url)
    profile_data_json = response.json()
    print(profile_data_json)

    return render_template('offers/viewOfferDetails.html', custom_offers_reply_count=custom_offers_reply_count,messageSubscription=messageSubscription,offer_details=offer_details,
                           profile_data=profile_data_json)


@connecsiApp.route('/deleteOffer/<string:offer_id>', methods=['GET'])
@is_logged_in
def deleteOffer(offer_id):
    print(offer_id)
    user_id = session['user_id']
    url = base_url + 'Offer/' + str(offer_id) + '/' + str(user_id)
    print(url)
    try:
        response = requests.delete(url=url)
        result_json = response.json()
        print(result_json)
        # res = requests.put(url=base_url + 'Campaign/update_campaign_status/' + str(campaign_id) + '/' + 'InActive')
        flash('Deleted Offer', 'success')
        return viewAllOffers()
    except Exception as e:
        print(e)
        flash('Please try again later', 'danger')
        pass

@connecsiApp.route('/deletedOffers', methods=['GET', 'POST'])
@is_logged_in
def deletedOffers():
    user_id = session['user_id']
    # import templates
    from templates.offers.offer import Offer
    offerObj = Offer(user_id=user_id)
    all_offer_data = offerObj.get_all_offers()
    deleted_offer_list = []
    for item in all_offer_data['data']:
        if item['deleted'] == 'true':
            deleted_offer_list.append(item)

    print(deleted_offer_list)
    return render_template('offers/deleted_offers.html', view_offer_data=deleted_offer_list)

@connecsiApp.route('/editOffer/<string:offer_id>', methods=['GET'])
@is_logged_in
def editOffer(offer_id):
    url_regionCodes = base_url + 'Youtube/regionCodes'
    regionCodes_json = ''
    try:
        regionCodes_response = requests.get(url=url_regionCodes)
        regionCodes_json = regionCodes_response.json()
        # print(regionCodes_json)
    except:
        pass
    url_videoCat = base_url + 'Youtube/videoCategories'
    videoCat_json = ''
    try:
        response_videoCat = requests.get(url=url_videoCat)
        videoCat_json = response_videoCat.json()
        # print(videoCat_json)
    except Exception as e:
        print(e)
    print(offer_id)
    user_id = session['user_id']
    from templates.offers.offer import Offer
    offerObj = Offer(user_id=user_id, offer_id=offer_id)
    offer_details = offerObj.get_offer_details()
    print(offer_details)
    try:
        for item in offer_details['data']:
            item['from_date'] = datetime.datetime.strptime(item['from_date'], '%d-%b-%y').date()
            item['to_date'] = datetime.datetime.strptime(item['to_date'], '%d-%b-%y').date()
            item['arrangements'] = item['arrangements'].replace('/', '')
            item['arrangements'] = item['arrangements'].replace(' ', '')
            item['kpis'] = item['kpis'].replace(' ', '')
    except Exception as e:
        print(e)
    return render_template('offers/edit_offerForm.html',
                           view_offer_details_data=offer_details,
                           regionCodes=regionCodes_json, videoCategories=videoCat_json)

@connecsiApp.route('/updateOffer', methods=['POST'])
@is_logged_in
def updateOffer():
    if request.method == 'POST':
        payload = request.form.to_dict()
        # print('payload = ',payload)
        offer_id = request.form.get('offer_id')
        # exit
        del payload['offer_id']
        # print(payload)
        # print(campaign_id)
        # exit()
        channels = request.form.getlist('channels')
        channels_string = ','.join(channels)
        payload.update({'channels': channels_string})
        regions = request.form.getlist('country')
        regions_string = ','.join(regions)
        payload.update({'regions': regions_string})

        arrangements = request.form.getlist('arrangements')
        arrangements_string = ','.join(arrangements)
        payload.update({'arrangements': arrangements_string})

        kpis = request.form.getlist('kpis')
        kpis_string = ','.join(kpis)
        payload.update({'kpis': kpis_string})

        # convert_to_campaign = request.form.get('convert_to_campaign')
        # print('is classified = ',is_classified_post)
        try:
            del payload['country']
            # del payload['convert_to_campaign']
        except:
            pass

        files = request.files.getlist("campaign_files")
        # print(files)
        # exit()
        filenames = []
        for file in files:
            filename = offer_files.save(file)
            filenames.append(filename)

        user_id = session['user_id']
        url_offer = base_url + 'Offer/' + str(offer_id) + '/' + str(user_id)
        response_offer = requests.get(url=url_offer)
        result_json_offer = response_offer.json()
        # print('cam data',result_json_campaign)

        for item in result_json_offer['data']:
            files_string = item['files']
            print(files_string)
            if files_string:
                filenames.append(files_string)

        filenames_string = ','.join(filenames)
        print('file name string', filenames_string)
        payload.update({'files': filenames_string})

        print('last payload', payload)

        url = base_url + 'Offer/' + str(offer_id) + '/' + str(user_id)
        print(url)
        try:
            response = requests.put(url=url, json=payload)
            result_json = response.json()
            print(result_json)
            flash('Updated Offer', 'success')
            return viewAllOffers()
        except Exception as e:
            print(e)
            flash('Offer didnt saved Please try again later', 'danger')
            pass
    else:
        flash('Unauthorized', 'danger')


# @connecsiApp.route('/searchOffers',methods=['GET','POST'])
# @is_logged_in
# def searchOffers():
#     url_regionCodes = base_url + 'Youtube/regionCodes'
#     regionCodes_json = ''
#     try:
#         regionCodes_response = requests.get(url=url_regionCodes)
#         regionCodes_json = regionCodes_response.json()
#         # print(regionCodes_json)
#     except:
#         pass
#     url_videoCat = base_url + 'Youtube/videoCategories'
#     videoCat_json = ''
#     try:
#         response_videoCat = requests.get(url=url_videoCat)
#         videoCat_json = response_videoCat.json()
#         # print(videoCat_json)
#     except Exception as e:
#         print(e)
#     return render_template('offers/search_offers.html',videoCategories=videoCat_json,
#                            regionCodes=regionCodes_json)


@connecsiApp.route('/searchOffers',methods=['GET','POST'])
@is_logged_in
def searchOffers():
    url_regionCodes = base_url + 'Youtube/regionCodes'
    regionCodes_json = ''
    subscriptionValue = getSubscriptionValues(str(session["user_id"]))
    custom_offers_reply_count = 0
    feature_name = ''
    package_name=''
    messageSubscription = {
        'Custom Offers Reply':''
    }
    for i in subscriptionValue['data']:
        if (i['feature_name'].lower() == 'custom offers reply'):
            custom_offers_reply_count = i['units']
            feature_name = i['feature_name']
            package_name=i['package_name']
    if (custom_offers_reply_count == 0):
        messageSubscription['Custom Offers Reply'] = "You ran out of "+feature_name+" Units of your " + subscriptionValue['data'][0][
            'package_name'] + " package. Add more units in custom or upgrade your package."
    try:
        regionCodes_response = requests.get(url=url_regionCodes)
        regionCodes_json = regionCodes_response.json()
        # print(regionCodes_json)
    except:
        pass
    url_videoCat = base_url + 'Youtube/videoCategories'
    videoCat_json = ''
    try:
        response_videoCat = requests.get(url=url_videoCat)
        videoCat_json = response_videoCat.json()
        # print(videoCat_json)
    except Exception as e:
        print(e)
    return render_template('offers/search_offers.html',package_name=package_name,messageSubscription=messageSubscription,custom_offers_reply_count=custom_offers_reply_count,videoCategories=videoCat_json,
                           regionCodes=regionCodes_json)

@connecsiApp.route('/sendCustomReply',methods = ['POST'])
@is_logged_in
def sendCustomReply():
    if request.method == 'POST':
       payload = request.form.to_dict()
       # print(payload)
       payload.update({'from_email_id': session['email_id']})
       # print(payload)
       date = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
       payload.update({'date':date})
       if payload['to_email_id'] == '':
          payload.update({'to_email_id':'kiran.padwal@connecsi.com'})
       print(payload)
       user_id= session['user_id']
       type = session['type']
       url = base_url + 'Messages/' + str(user_id) +'/' + type
       try:
           response = requests.post(url=url, json=payload)
           data = response.json()
           print(data)
           # if data['resposne'] == 1:
           if(data['response']==1):
               check = subscriptionReduction("Custom Offers Reply")
               if (check['response'] == 1):
                   print("done subscription Custom offer Reply")

           return 'Your message has been sent'
           # else: return "Failed to sent mail"
       except:
           pass
           return  'Server Error'




@connecsiApp.route('/getOffers',methods=['GET','POST'])
@is_logged_in
def getOffers():
    if request.method=='POST':
        payload = request.form.to_dict()
        print(payload)
        url = base_url+'Offer/searchOffers'
        response = requests.post(url=url,json=payload)
        print(response.json())
        response_json = response.json()
        for item in response_json['data']:
            channel_id = item['channel_id']
            user_inf_data = requests.get(url=base_url + 'Influencer/getDetailsByUserId/' + str(channel_id))
            user_inf_data_json = user_inf_data.json()
            print(user_inf_data_json)
            channel_img=''
            for item1 in user_inf_data_json['data']:
                channel_img = item1['channel_img']
            item.update({'channel_img':channel_img})
            print(item)
        return jsonify(results=response_json['data'])
        # return 'ajax working'



@connecsiApp.route('/searchClassifieds', methods=['GET', 'POST'])
@is_logged_in
def searchClassifieds():
    url_regionCodes = base_url + 'Youtube/regionCodes'
    regionCodes_json = ''
    try:
        regionCodes_response = requests.get(url=url_regionCodes)
        regionCodes_json = regionCodes_response.json()
        # print(regionCodes_json)
    except:
        pass
    url_videoCat = base_url + 'Youtube/videoCategories'
    videoCat_json = ''
    try:
        response_videoCat = requests.get(url=url_videoCat)
        videoCat_json = response_videoCat.json()
        # print(videoCat_json)
    except Exception as e:
        print(e)
    return render_template('classifiedAds/search_classifieds.html', videoCategories=videoCat_json,
                           regionCodes=regionCodes_json)

@connecsiApp.route('/getClassifieds', methods=['GET', 'POST'])
@is_logged_in
def getClassifieds():
    if request.method == 'POST':
        payload = request.form.to_dict()
        print(payload)
        url = base_url + 'Classified/searchClassifieds'
        response = requests.post(url=url, json=payload)
        print(response.json())
        response_json = response.json()
        return jsonify(results=response_json['data'])
        # return 'ajax working'



                # @connecsiApp.route('/login/authorized')
# def authorized():
#     resp = linkedin.authorized_response()
#     if resp is None:
#         return 'Access denied: reason=%s error=%s' % (
#             request.args['error_reason'],
#             request.args['error_description']
#         )
#     session['linkedin_token'] = (resp['access_token'], '')

    # me = linkedin.get('people/~')
    # email_linkedin = linkedin.get('people/~:(email-address)')
    # print(jsonify(email_linkedin.data))

    # email_id = email_linkedin.data['emailAddress']
    # data=[me.data['id'],me.data['firstName'],me.data['lastName'],email_id,'',me.data['headline'],'Admin']
    # print(me.data)
    # session['logged_in'] = True
    # session['type'] = 'brand'
    # session['user_id'] = me.data['id']
    # session['first_name']=me.data['firstName']
    # print(data)
    # return render_template('index.html',data=data)

# @linkedin.tokengetter
# def get_linkedin_oauth_token():
#     return session.get('linkedin_token')


# def change_linkedin_query(uri, headers, body):
#     auth = headers.pop('Authorization')
#     headers['x-li-format'] = 'json'
#     if auth:
#         auth = auth.replace('Bearer', '').strip()
#         if '?' in uri:
#             uri += '&oauth2_access_token=' + auth
#         else:
#             uri += '?oauth2_access_token=' + auth
#     return uri, headers, body
#
# linkedin.pre_request = change_linkedin_query

#  google Analytics for brands section #################################
from googleAnalyticsKiranLib import GoogleAnalyticsKiranLib
@connecsiApp.route('/google_analytics',methods=['GET'])
@is_logged_in
def google_analytics():
    google_analytics_kiran_lib = GoogleAnalyticsKiranLib()
    auth_url = google_analytics_kiran_lib.get_auth_url()
    print(auth_url)
    return redirect(auth_url)

@connecsiApp.route('/google_analytics_call_back_url',methods=['GET'])
@is_logged_in
def google_analytics_call_back_url():
    user_id=session['user_id']
    call_back_url = request.url
    add_credentials_url = base_url + 'Brand/brandsGoogleAnalyticsCredentials/' + str(user_id)
    print(call_back_url)
    google_analytics_kiran_lib = GoogleAnalyticsKiranLib()
    access_token,refresh_token = google_analytics_kiran_lib.get_access_token(call_back_url=call_back_url,user_id=user_id,add_credentials_url=add_credentials_url)
    if access_token:
        session['google_analytics_acess_token']=access_token
        session['google_analytics_refresh_token'] = refresh_token
        print('session acess_token= ',session['google_analytics_acess_token'])
        print('session refresh_token= ', session['google_analytics_refresh_token'])
        view_ids = google_analytics_kiran_lib.get_view_ids(access_token=access_token)
        for viewId in view_ids:
            data = google_analytics_kiran_lib.get_google_analytics_data(access_token=access_token,viewId=viewId)
            print(data)
        return 'data retrived'
    else: return 'no access token'



#  google Analytics for brands section  ends #################################


#  youtube Analytics for influencers section #################################
from youtubeAnalyticsKiranLib import YoutubeAnalyticsKiranLib
@connecsiApp.route('/youtube_analytics',methods=['GET'])
@is_logged_in
def youtube_analytics():
    youtube_analytics_kiran_lib = YoutubeAnalyticsKiranLib()
    auth_url = youtube_analytics_kiran_lib.get_auth_url()
    print(auth_url)
    return redirect(auth_url)

@connecsiApp.route('/youtube_analytics_call_back_url',methods=['GET'])
@is_logged_in
def youtube_analytics_call_back_url():
    user_id=session['user_id']
    print(user_id)
    call_back_url = request.url
    add_credentials_url = base_url + 'Influencer/influencerYoutubeAnalyticsCredentials/' + str(user_id)
    print(call_back_url)
    youtube_analytics_kiran_lib = YoutubeAnalyticsKiranLib()
    access_token = youtube_analytics_kiran_lib.get_access_token(call_back_url=call_back_url,user_id=user_id,add_credentials_url=add_credentials_url)
    if access_token:
        print(access_token)
        # view_ids = youtube_analytics_kiran_lib.get_view_ids(access_token=access_token)
        # for viewId in view_ids:
        #     data = youtube_analytics_kiran_lib.get_google_analytics_data(access_token=access_token,viewId=viewId)
        #     print(data)
        return 'data retrived'
    else: return 'no access token'


#  youtube Analytics for influencers section  ends #################################
#----------------instagram route for landing page-------------------------------------------
@connecsiApp.route('/getInstgramUserFromInstagramApi/<string:instagram_username>', methods=['GET'])
#@is_logged_in
def getInstgramUserFromInstagramApi(instagram_username):
    try:
        url = base_url + 'Insta/getInstagramChannel/' + instagram_username
        response = requests.get(url=url)
        response_json = response.json()
        return jsonify(results=response_json)
    except Exception as e:
        print(e)
        return e

#------------------------------------------------------------------------------------------
#----------------youtube routes for landing page-------------------------------------------


# @connecsiApp.route('/getYoutubeUserFromYoutubeApi/<string:youtube_username>', methods=['GET'])
# #@is_logged_in
# def getYoutubeUserFromYoutubeApi(youtube_username):
#     try:
#         url = base_url + 'Youtube/getYoutubeChannelDetailsFromYoutubeApi/' + youtube_username
#         response = requests.get(url=url)
#         response_json = response.json()
#         return jsonify(results=response_json)
#     except Exception as e:
#         print(e)
#         return e


@connecsiApp.route('/getYoutubeUserFromYoutubeApi/<string:youtube_username>', methods=['GET'])
#@is_logged_in
def getYoutubeUserFromYoutubeApi(youtube_username):
    try:
        url = base_url + 'Youtube/getYoutubeChannelDetailsFromYoutubeApi/' + youtube_username
        response = requests.get(url=url)
        response_json = response.json()
        url2 = base_url + 'Youtube/totalVideos/' + youtube_username
        response2 = requests.get(url=url2)
        response_json2=response2.json()
        wholeData={}
        wholeData["results"]=response_json
        wholeData["totalVideos"]=response_json2
        return jsonify(wholeData)
    except Exception as e:
        print(e)
        return e


@connecsiApp.route('/getYoutubeSearchDropDownResults/<string:youtube_searchChannel>', methods=['GET'])
# @is_logged_in
def getYoutubeSearchDropDownResults(youtube_searchChannel):
    try:
        print (youtube_searchChannel)
        url = base_url + '/Youtube/getYoutubeChannelSnippetFromYoutubeSearchApi/' + youtube_searchChannel
        response = requests.get(url=url)
        response_json = response.json()
        print ("data ji",response_json)
        return jsonify(results=response_json)
    except Exception as e:
        print(e)
        return e

@connecsiApp.route('/getYoutubeVideoCategory/<string:youtube_ChannelID>', methods=['GET'])
# @is_logged_in
def getYoutubeVideoCategory(youtube_ChannelID):
    try:
        print (youtube_ChannelID)
        url = base_url + '/Youtube/getVideoCategoriesByChannelId/' + youtube_ChannelID
        response = requests.get(url=url)
        response_json = response.json()
        print ("data ji",response_json)
        return jsonify(results=response_json)
    except Exception as e:
        print(e)
        return e


#-------------------------------------------------------------------------------------------

#------------------------------- twitter landing page routes--------------------------------

@connecsiApp.route('/getTwitterUserFromTwitterApi/<string:twitter_username>', methods=['GET'])
#@is_logged_in
def getTwitterUserFromTwitterApi(twitter_username):
    try:
        url = base_url + '/Twitter/getTwitterChannelsDetailsFromConnecsi/' + twitter_username
        response = requests.get(url=url)
        response_json = response.json()
        return jsonify(results=response_json)
    except Exception as e:
        print(e)
        return e


@connecsiApp.route('/getTwitterSearchDropDownResults/<string:twitter_searchChannel>', methods=['GET'])
# @is_logged_in
def getTwitterSearchDropDownResults(twitter_searchChannel):
    try:
        print(twitter_searchChannel)
        url = base_url + '/Twitter/getTwitterChannelsFromTwitterSearchApi/' + twitter_searchChannel
        response = requests.get(url=url)
        response_json = response.json()
        print("data ji", response_json)
        return jsonify(results=response_json)
    except Exception as e:
        print(e)
        return e

# landing page route
@connecsiApp.route('/influencer-scanner/influencer')
# @is_logged_in
def influencerScanner():
    title='Influencer Scanner'
    data=[]
    dataList= {
        'title':'Influencer Scanner'
    }
    data.append(dataList)
    return render_template('user/influencerScanner.html',data=data,title='Influencer Scanner')


@connecsiApp.route('/influencer-scanner/advertiser')
# @is_logged_in
def influencerScannerAdvertiser():
    title='Influencer Scanner'
    data=[]
    dataList= {
        'title':'Influencer Scanner'
    }
    data.append(dataList)
    return render_template('user/influencerScannerBrand.html',data=data,title='Brand Influencer Scanner')



@connecsiApp.route('/getChannelGraphData/<string:channel_name>/<string:channel_id>',methods=['GET'])
@is_logged_in
def getChannelGraphData(channel_name,channel_id):
       try:
           url = base_url + '/GraphHistory/getNoOfFollowersHistory/' + channel_name+'/'+channel_id

           response = requests.get(url=url)

           response_json = response.json()

           return jsonify(results=response_json['data'])
       except Exception as e:
           print(e)
           return e



#-----------subscription levels with its feautes-------------------------------------------------

@connecsiApp.route('/upgrade')
@is_logged_in
def upgrade():

    return render_template('user/upgrade.html')

def levelsWithFeatures(package_name):
    package_features={}
    if(package_name=='Free'):
        package_features = {
            "data":[
            {
                "feature_name":"Create Campaign",
                "units":2,
                "price":2,
                "customized_feature":"No",
                "added_units":0,
                "base_units":2
            },
            {
                "feature_name": "Export Lists",
                "units": -1,
                "price": 0,
                "customized_feature": "No",
                "added_units":0,
                "base_units":-1
            },
            {
                "feature_name": "Add to favorites",
                "units": 5,
                "price": 1,
                "customized_feature": "No",
                "added_units":0,
                "base_units":5
            },
            {
                "feature_name": "Classified Ads Posting",
                "units": -1,
                "price": 0,
                "customized_feature": "No",
                "added_units":0,
                "base_units":-1
            },
            {
                "feature_name": "Custom Offers Reply",
                "units": 5,
                "price": 5,
                "customized_feature": "No",
                "added_units":0,
                "base_units":5
            },
            {
                "feature_name": "Alerts",
                "units": 5,
                "price": 1,
                "customized_feature": "No",
                "added_units":0,
                "base_units":5
            },
            {
                "feature_name": "Messages",
                "units": -1,
                "price": 0,
                "customized_feature": "No",
                "added_units":0,
                "base_units":-1
            },
            {
                "feature_name": "Autofill Proposal",
                "units": 1,
                "price": 2,
                "customized_feature": "No",
                "added_units":0,
                "base_units":1
            }
            ]
        }
    elif(package_name=='Basic'):
        package_features = {
            "data":[
            {
                "feature_name": "Create Campaign",
                "units": 10,
                "price": 10,
                "customized_feature": "No",
                "added_units":0,
                "base_units":10
            },
            {
                "feature_name": "Export Lists",
                "units": -1,
                "price": 0,
                "customized_feature": "No",
                "added_units":0,
                "base_units":-1
            },
            {
                "feature_name": "Add to favorites",
                "units": 25,
                "price": 6,
                "customized_feature": "No",
                "added_units":0,
                "base_units":25
            },
            {
                "feature_name": "Classified Ads Posting",
                "units": 10,
                "price": 20,
                "customized_feature": "No",
                "added_units":0,
                "base_units":10
            },
            {
                "feature_name": "Custom Offers Reply",
                "units": 20,
                "price": 20,
                "customized_feature": "No",
                "added_units":0,
                "base_units":20
            },
            {
                "feature_name": "Alerts",
                "units": 25,
                "price": 6,
                "customized_feature": "No",
                "added_units":0,
                "base_units":25
            },
            {
                "feature_name": "Messages",
                "units": 15,
                "price": 7,
                "customized_feature": "No",
                "added_units":0,
                "base_units":15
            },
            {
                "feature_name": "Autofill Proposal",
                "units": 5,
                "price": 10,
                "customized_feature": "No",
                "added_units":0,
                "base_units":5
            }
            ]
        }
    elif (package_name == 'Professional'):
        package_features = {
            "data":[
            {
                "feature_name": "Create Campaign",
                "units": 20,
                "price": 20,
                "customized_feature": "No",
                "added_units":0,
                "base_units":20
            },
            {
                "feature_name": "Export Lists",
                "units": 100,
                "price": 40,
                "customized_feature": "No",
                "added_units":0,
                "base_units":100
            },
            {
                "feature_name": "Add to favorites",
                "units": 50,
                "price": 12,
                "customized_feature": "No",
                "added_units":0,
                "base_units":12
            },
            {
                "feature_name": "Classified Ads Posting",
                "units": 20,
                "price": 40,
                "customized_feature": "No",
                "added_units":0,
                "base_units":20
            },
            {
                "feature_name": "Custom Offers Reply",
                "units": 50,
                "price": 50,
                "customized_feature": "No",
                "added_units":0,
                "base_units":50
            },
            {
                "feature_name": "Alerts",
                "units": 50,
                "price": 12,
                "customized_feature": "No",
                "added_units":0,
                "base_units":50
            },
            {
                "feature_name": "Messages",
                "units": 30,
                "price": 15,
                "customized_feature": "No",
                "added_units":0,
                "base_units":30
            },
            {
                "feature_name": "Autofill Proposal",
                "units": 20,
                "price": 40,
                "customized_feature": "No",
                "added_units":0,
                "base_units":20
            }
            ]
        }
    elif (package_name == 'Enterprise'):
        package_features = {
            "data":[
            {
                "feature_name": "Create Campaign",
                "units": 1000000,
                "price": 0,
                "customized_feature": "No",
                "added_units":0,
                "base_units":1000000
            },
            {
                "feature_name": "Export Lists",
                "units": 500,
                "price": 200,
                "customized_feature": "No",
                "added_units":0,
                "base_units":500
            },
            {
                "feature_name": "Add to favorites",
                "units": 1000000,
                "price": 0,
                "customized_feature": "No",
                "added_units":0,
                "base_units":1000000
            },
            {
                "feature_name": "Classified Ads Posting",
                "units": 1000000,
                "price": 0,
                "customized_feature": "No",
                "added_units":0,
                "base_units":1000000
            },
            {
                "feature_name": "Custom Offers Reply",
                "units": 1000000,
                "price": 0,
                "customized_feature": "No",
                "added_units":0,
                "base_units":1000000
            },
            {
                "feature_name": "Alerts",
                "units": 1000000,
                "price": 0,
                "customized_feature": "No",
                "added_units":0,
                "base_units":1000000
            },
            {
                "feature_name": "Messages",
                "units": 1000000,
                "price": 0,
                "customized_feature": "No",
                "added_units":0,
                "base_units":1000000
            },
            {
                "feature_name": "Autofill Proposal",
                "units": 1000000,
                "price": 0,
                "customized_feature": "No",
                "added_units":0,
                "base_units":1000000
            }
            ]
        }
    return package_features
#----------------------subscription methods-------------------------------------------------------


def getSubscriptionValues(u_id):
    print("get value")
    url2 = base_url + 'Brand/subscriptionPackageDetails/' + u_id
    response1 = requests.get(url2)
    print('hello i m here',response1.json())
    value=response1.json()
    if value['data']:
        print('hello')
        expiryDate=value['data'][0]['p_expiry_date']
        readable = datetime.datetime.fromtimestamp(expiryDate)
        if(datetime.datetime.now()>readable):
            print("ending current subscription")
            check=freeSubscription(u_id)
            if(check['response']==1):
                print("subscription reverted to free version")
    return value

def freeSubscription(u_id):
    print("free")
    startTime = str(int(time.time()))
    newDate = datetime.datetime.now() + datetime.timedelta(30)
    endTime = str(int(time.mktime(newDate.timetuple())))
    url3 = base_url + 'Brand/updatePackageDetails/' + u_id
    payload3 = {}
    payload3["package_name"] = "Free"
    payload3["p_created_date"] = startTime
    payload3["p_expiry_date"] = endTime
    payload3["base_package"] = "Free"
    response3 = requests.post(url3, json=payload3)

    check=response3.json()
    response4=None
    print(check)
    if(check['response']==1):
        url4 = base_url + 'Brand/subscriptionFeatureDetails/' + u_id
        allFeatures=levelsWithFeatures("Free")
        response4=0
        print(allFeatures['data'])
        for i in allFeatures["data"]:
            print('inside for',i)
            payload4 = {}
            payload4["feature_name"] = i["feature_name"]
            payload4["units"] = i["units"]
            payload4["price"] = i["price"]
            payload4["customized_feature"] = i["customized_feature"]
            payload4["added_units"] = i["added_units"]
            payload4["base_units"] = i["base_units"]
            response4 = requests.post(url4, json=payload4)
    return response4.json()

def customSubscription(features, u_id):
    print("custom",features)
    url4 = base_url + 'Brand/subscriptionFeatureDetails/' + u_id
    response4=None
    for i in features:
        print(i)
        payload4 = {}
        payload4["feature_name"] = i['feature_name']
        payload4["units"] = i['units']
        payload4["price"] = i['price']
        payload4["customized_feature"] = i['customized_feature']
        payload4["added_units"] = i["added_units"]
        payload4["base_units"] = i["base_units"]
        response4 = requests.post(url4, json=payload4)
        check=response4.json()
        print("res",check)
        if(check['response']==1):
            print("feature added")
    return response4.json()

def basicSubscription(u_id):
    print("basic")
    startTime = str(int(time.time()))
    newDate = datetime.datetime.now() + datetime.timedelta(30)
    endTime = str(int(time.mktime(newDate.timetuple())))
    url3 = base_url + 'Brand/updatePackageDetails/' + u_id
    payload3 = {}
    payload3["package_name"] = "Basic"
    payload3["p_created_date"] = startTime
    payload3["p_expiry_date"] = endTime
    payload3["base_package"] = "Basic"
    response3 = requests.post(url3, json=payload3)
    check = response3.json()
    response4=None
    if(check['response']==1):
        url4 = base_url + 'Brand/subscriptionFeatureDetails/' + u_id
        allFeatures = levelsWithFeatures("Basic")
        for i in allFeatures["data"]:
            payload4 = {}
            payload4["feature_name"] = i['feature_name']
            payload4["units"] = i['units']
            payload4["price"] = i['price']
            payload4["customized_feature"] = i['customized_feature']
            payload4["added_units"] = i["added_units"]
            payload4["base_units"] = i["base_units"]
            response4 = requests.post(url4, json=payload4)
    return response4.json()


def professionalSubscription(u_id):
    print("professional")
    startTime = str(int(time.time()))
    newDate = datetime.datetime.now() + datetime.timedelta(30)
    endTime = str(int(time.mktime(newDate.timetuple())))
    url3 = base_url + 'Brand/updatePackageDetails/' + u_id
    payload3 = {}
    payload3["package_name"] = "Professional"
    payload3["p_created_date"] = startTime
    payload3["p_expiry_date"] = endTime
    payload3["base_package"] = "Professional"
    response3 = requests.post(url3, json=payload3)
    check = response3.json()
    response4=None
    if (check['response']==1):
        url4 = base_url + 'Brand/subscriptionFeatureDetails/' + u_id
        allFeatures = levelsWithFeatures("Professional")
        for i in allFeatures['data']:
            payload4 = {}
            payload4["feature_name"] = i['feature_name']
            payload4["units"] = i['units']
            payload4["price"] = i['price']
            payload4["customized_feature"] = i['customized_feature']
            payload4["added_units"] = i["added_units"]
            payload4["base_units"] = i["base_units"]
            response4 = requests.post(url4, json=payload4)
    return response4.json()

def enterpriseSubscription(u_id):
    print("enterprise")
    startTime = str(int(time.time()))
    newDate = datetime.datetime.now() + datetime.timedelta(30)
    endTime = str(int(time.mktime(newDate.timetuple())))
    url3 = base_url + 'Brand/updatePackageDetails/' + u_id
    payload3 = {}
    payload3["package_name"] = "Enterprise"
    payload3["p_created_date"] = startTime
    payload3["p_expiry_date"] = endTime
    payload3["base_package"] = "Enterprise"
    response3 = requests.post(url3, json=payload3)
    check = response3.json()
    response4=None
    if (check['response']==1):
        url4 = base_url + 'Brand/subscriptionFeatureDetails/' + u_id
        allFeatures = levelsWithFeatures("Enterprise")
        response4 = 0
        for i in allFeatures["data"]:
            payload4 = {}
            payload4["feature_name"] = i["feature_name"]
            payload4["units"] = i["units"]
            payload4["price"] = i["price"]
            payload4["customized_feature"] = i["customized_feature"]
            payload4["added_units"] = i["added_units"]
            payload4["base_units"] = i["base_units"]
            response4 = requests.post(url4, json=payload4)
    return response4.json()
# -------ashish----------------subscription routes------------------------------------------------

@connecsiApp.route('/updateBrandSubscriptionPackageDetails',methods=['POST'])
@is_logged_in
def updateBrandSubscriptionPackageDetails():
       try:
           url = base_url + 'Brand/updatePackageDetails/' + str(session["user_id"])
           payload = request.form.to_dict()
           payloadNew={}
           startTime = str(int(time.time()))
           newDate = datetime.datetime.now() + datetime.timedelta(30)
           endTime = str(int(time.mktime(newDate.timetuple())))
           payloadNew["package_name"]=payload["package_name"]
           payloadNew["p_created_date"]=startTime
           payloadNew["p_expiry_date"]=endTime


           if(payload["package_name"]=="Custom"):
               print("inside custom")
               allValue=getSubscriptionValues(str(session["user_id"]))
               features=[]
               valueLen=(len(payload)-1)/2
               value=int(valueLen)+1

               for j in range(1,value):
                   print(j)
                   for i in allValue['data']:
                       payloadNew['base_package'] =i['base_package']
                       if(i['feature_name']==payload['feature'+str(j)]):
                           print("match",i)
                           units=i['units']+int(payload['count'+str(j)])
                           #enter price value here for each module
                           price=i['price']+(int(payload['count'+str(j)])*1)
                           added=i['added_units']+int(payload['count'+str(j)])
                           dat = {
                               'feature_name': payload['feature' + str(j)],
                               'units': units,
                               'price':price,
                               'customized_feature':"Yes",
                               'added_units':added,
                               'base_units':i['base_units']
                           }
                           features.append(dat)
                           print("yo", features)
               check = customSubscription(features, str(session["user_id"]))

               response1 = requests.post(url=url, json=payloadNew)
               print("check value", check)

           elif(payload["package_name"]=="Basic"):
               print("inside basic")
               check=basicSubscription(str(session["user_id"]))
               if(check['response']==1):
                   print("basic plan ADDED")

               else:
                   print("basic plan NOT added")

           elif (payload["package_name"] == "Professional"):
               print("inside Professional")
               check = professionalSubscription(str(session["user_id"]))
               if (check['response'] == 1):
                   print("professional plan ADDED")

               else:
                   print("professional plan NOT added")


           elif (payload["package_name"] == "Enterprise"):
               print("inside Enterprise")
               check = enterpriseSubscription(str(session["user_id"]))
               if (check['response'] == 1):
                   print("enterprise plan ADDED")

               else:
                   print("enterprise plan NOT added")

           return redirect('/profileView')
       except Exception as e:
           print(e)
           return e
#---------- route for subtraction values on click and all----------------------------------------


@connecsiApp.route('/updatingFeatureValue/<string:feature_name>',methods=['POST'])
@is_logged_in
def updatingFeatureValue(feature_name):
       try:
           subscriptionReduction(feature_name)
           return jsonify({"response":1})
       except Exception as e:
           print(e)
           return e

#------- route for adding back value --------------------------------------------------------
@connecsiApp.route('/addingBackFeatureValue/<string:feature_name>',methods=['POST'])
@is_logged_in
def addingBackFeatureValue(feature_name):
       try:
           subscriptionAddition(feature_name)
           return jsonify({"response":1})
       except Exception as e:
           print(e)
           return e
#-------- subtraction method for units in subscription-------------------------------------------

def subscriptionReduction(feature):
    feature_name=feature.split('_')

    subValues = getSubscriptionValues(str(session["user_id"]))
    for i in subValues['data']:
        if(i['feature_name']==feature_name[0]):
            if(len(feature_name)==1):
                i['units'] = i['units'] - 1
            else:
                i['units'] = i['units'] - int(feature_name[1])
            #update call for feature details
            check=updateFeatureSubscription(str(session["user_id"]),i)
            if(check['response']==1):
                print("feature value updated")
                return check


def subscriptionAddition(feature):
    feature_name=feature.split('_')

    subValues = getSubscriptionValues(str(session["user_id"]))
    for i in subValues['data']:
        if(i['feature_name']==feature_name[0]):
            if(len(feature_name)==1):
                i['units'] = i['units'] + 1
            else:
                i['units'] = i['units'] + int(feature_name[1])
            #update call for feature details
            check=updateFeatureSubscription(str(session["user_id"]),i)
            if(check['response']==1):
                print("feature value updated")



# ----------------updating single feature one by one------------------------------------------------------------
def updateFeatureSubscription(u_id,feature):
    url4 = base_url + 'Brand/subscriptionFeatureDetails/' + u_id
    payload4 = {}
    payload4["feature_name"] = feature['feature_name']
    payload4["units"] = feature['units']
    payload4["price"] = feature['price']
    payload4["customized_feature"] = feature['customized_feature']
    payload4["added_units"] = feature['added_units']
    payload4["base_units"] = feature['base_units']
    response4 = requests.post(url4, json=payload4)
    return response4.json()

#-------------- getting classified values-------------------------------------------------------

@connecsiApp.route('/getClassified/<string:classified_id>',methods=['GET'])
@is_logged_in
def getClassified(classified_id):
    url = base_url + 'Classified/'+classified_id+'/'+str(session['user_id'])
    response=requests.get(url)
    response_json = response.json()
    return jsonify(response_json)
    # return response.json()

#----------------saving classified ads---------------------------------------------------------
@connecsiApp.route('/saveClassifiedAds',methods=['POST'])
@is_logged_in
def saveClassifiedAds():
    data=request.form.to_dict()
    print(session['user_id'])
    print(data)
    url = base_url + 'Classified/'+str(session['user_id'])
    response=requests.post(url=url,json=data)
    check=response.json()
    if(check['response']==1):
        check2 = subscriptionReduction("Classified Ads Posting")
        if (check2['response'] == 1):
            print("done subscription Classified Ads Posting")
    response_json = response.json()
    return jsonify(response_json)

#################################################################################################################



if __name__ == '__main__':
    # connecsiApp.secret_key = 'connecsiSecretKey'
    connecsiApp.run(debug=True,host='127.0.0.1',port=8090,threaded=True)
