@connecsiApp.route('/searchInfluencers', methods=['POST', 'GET'])
@is_logged_in
def searchInfluencers():
    user_id = session['user_id']
    url_regionCodes = base_url + 'Youtube/regionCodes'
    url_videoCat = base_url + 'Youtube/videoCategories'
    regionCodes_json = ''
    videoCat_json = ''
    form_filters = ''
    country_name = ''
    view_campaign_data = ''
    data = ''
    favInfList_data = ''
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
    lookup_string = lookup_string.replace('&', 'and')

    print('before getting campaigns')
    from templates.campaign import campaign
    campaignObj = campaign.Campaign(user_id=user_id)
    view_campaign_data = campaignObj.get_all_campaigns()
    print('after getting campaigns')

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
    print('before POST METHOD')
    if request.method == 'POST':
        print('i m inside POST METHOD')
        if 'search_inf' in request.form:
            string_word = request.form.get('string_word')
            print('string word =', string_word)
            # exit()
            category = string_word.replace('and', '&')
            print(category)
            category_id = ''
            for cat in videoCat_json['data']:
                # print(cat['video_cat_name'])
                if cat['video_cat_name'] == category:
                    print("category id = ", cat['video_cat_id'])
                    category_id = cat['video_cat_id']
            form_filters = request.form.to_dict()
            print('post form filters =', form_filters)
            # exit()
            if form_filters['country']:
                url_country_name = base_url + 'Youtube/regionCode/' + form_filters['country']
                try:
                    response_country_name = requests.get(url=url_country_name)
                    country_name_json = response_country_name.json()
                    print(country_name_json['data'][0][1])
                    country_name = country_name_json['data'][0][1]
                except Exception as e:
                    print(e)
                form_filters.update({'country_name': country_name})
            print('last filters = ', form_filters)
            payload = request.form.to_dict()

            # del payload['string_word']
            del payload['search_inf']
            # del payload['channel']
            payload.update({'category_id': str(category_id)})
            payload.update({'min_lower': payload.get('min_lower')})
            payload.update({'max_upper': payload.get('max_upper')})
            # payload.update({'sort_order': "High To Low"})
            try:
                payload.update({'offset': form_filters['offset']})
            except:
                payload.update({'offset': 0})
                pass

            print('payload  form filter = ', payload)

            try:
                channel = request.form.get('channel')
                url = base_url + 'Youtube/searchChannels/' + channel
                print(url)

                response = requests.post(url, json=payload)
                print(response.json())
                data = response.json()
                linechart_id = 1
                for item in data['data']:
                    item.update({'linechart_id': linechart_id})
                    # print(item)
                    linechart_id += 1

                return render_template('search/searchInfluencers.html', regionCodes=regionCodes_json,
                                       lookup_string=lookup_string, form_filters=form_filters, data=data,
                                       view_campaign_data=view_campaign_data
                                       , favInfList_data=favInfList_data, payload_form_filter=payload)
            except Exception as e:
                print(e)
                print('i m hee')
                return render_template('search/searchInfluencers.html', regionCodes=regionCodes_json,
                                       lookup_string=lookup_string, form_filters=form_filters, data='', pagination='',
                                       view_campaign_data=view_campaign_data
                                       , favInfList_data=favInfList_data)
        else:
            print('i m disguise')
            try:
                payload = {
                    "category_id": "",
                    "country": "PL",
                    "min_lower": 0,
                    "max_upper": 21200,
                    "sort_order": "High To Low"
                }
                url = base_url + 'Youtube/searchChannels/Youtube'
                response = requests.post(url, json=payload)
                print(response.json())
                data = response.json()
                linechart_id = 1
                for item in data['data']:
                    item.update({'linechart_id': linechart_id})
                    # print(item)
                    linechart_id += 1
                form_filters = {'channel': 'Youtube', 'string_word': '', 'country': 'PL', 'min_lower': '0',
                                'max_upper': '21200', 'search_inf': '', 'sort_order': 'High To Low',
                                'country_name': 'Poland'}
            except:
                pass

            return render_template('search/searchInfluencers.html', regionCodes=regionCodes_json,
                                   lookup_string=lookup_string, form_filters=form_filters, data=data, pagination='',
                                   view_campaign_data=view_campaign_data,
                                   favInfList_data=favInfList_data)

    else:
        print('i m here last')
        try:
            payload = {
                "category_id": "",
                "country": "PL",
                "min_lower": 0,
                "max_upper": 21200,
                "sort_order": "High To Low",
                "offset": 0
            }

            url = base_url + '/Youtube/searchChannels/youtube'
            response = requests.post(url, json=payload)
            print(response.json())
            data = response.json()
            linechart_id = 1
            for item in data['data']:
                item.update({'linechart_id': linechart_id})
                # print(item)
                linechart_id += 1
            form_filters = {'channel': 'Youtube', 'string_word': '', 'country': 'PL', 'min_lower': '0',
                            'max_upper': '21200', 'search_inf': '', 'sort_order': 'High To Low',
                            'country_name': 'Poland'}
        except:
            pass
        exportCsv(data=data)
        return render_template('search/searchInfluencers.html', regionCodes=regionCodes_json,
                               lookup_string=lookup_string, form_filters=form_filters, data=data, pagination='',
                               view_campaign_data=view_campaign_data,
                               favInfList_data=favInfList_data, payload_form_filter=form_filters)
