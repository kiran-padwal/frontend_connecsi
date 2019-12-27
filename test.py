mydict = [{
    "proposal_id": 7,
    "campaign_id": 8,
    "inf_first_name": "kiran",
    "inf_last_name": "padwal influencer",
      "inf_categories": "1,2,10,15,17,18,20,21",
      "inf_country": "PL",
      "proposal_price": 123,
      "proposal_from_date": "2019-12-20",
      "proposal_to_date": "2019-12-24",
      "regions": "DZ,AR,AU",
      "video_cat_id": "1",
      "campaign_status": "Queued",
    "channel_id": "UCgdZZWMmLNT9xPaQjgDEXgg",
    "revenue_generated": 7766,
    "new_users": 1212,
    "inf_report_date_posted": "2019-12-21",
    "inf_report_link_posted": "https://www.codeproject.com/Questions/665",
    "channel": "youtube",
    "youtube_title": "Kiran Padwal",
    "insta_username": 'null',
    "twitter_screen_name": 'null'
},
    {
        "proposal_id": 7,
        "campaign_id": 8,
        "inf_first_name": "kiran",
"inf_last_name": "padwal influencer",
      "inf_categories": "1,2,10,15,17,18,20,21",
      "inf_country": "PL",
      "proposal_price": 123,
      "proposal_from_date": "2019-12-20",
      "proposal_to_date": "2019-12-24",
      "regions": "DZ,AR,AU",
      "video_cat_id": "1",
      "campaign_status": "Queued",
        "channel_id": "UCgdZZWMmLNT9xPaQjgDEXgg",
        "revenue_generated": 7766,
        "new_users": 1212,
        "inf_report_date_posted": "2019-12-23",
        "inf_report_link_posted": "https://www.codeproject.com/Questions/665hdkahdjshhd",
        "channel": "youtube",
        "youtube_title": "Kiran Padwal",
        "insta_username": 'null',
        "twitter_screen_name": 'null'
    },
    {
        "proposal_id": 7,
        "campaign_id": 8,
        "inf_first_name": 'null',
"inf_last_name": "null",
      "inf_categories": "null",
      "inf_country": "null",
      "proposal_price": 123,
      "proposal_from_date": "2019-12-20",
      "proposal_to_date": "2019-12-24",
      "regions": "DZ,AR,AU",
      "video_cat_id": "1",
      "campaign_status": "Queued",
        "channel_id": "962771351193948162",
        "revenue_generated": 46464,
        "new_users": 3435,
        "inf_report_date_posted": "2019-12-22",
        "inf_report_link_posted": "https://www.codeproject.com/Questions/665",
        "channel": "twitter",
        "youtube_title": 'null',
        "insta_username": 'null',
        "twitter_screen_name": "kiran_padwal786"
    },
{
        "proposal_id": 9,
        "campaign_id": 8,
        "inf_first_name": 'sachin',
"inf_last_name": "tedulkar",
      "inf_categories": "1,2,10,15,17,18,20,21",
      "inf_country": "PL",
      "proposal_price": 123,
      "proposal_from_date": "2019-12-20",
      "proposal_to_date": "2019-12-24",
      "regions": "DZ,AR,AU",
      "video_cat_id": "1",
      "campaign_status": "Queued",
        "channel_id": "962771351193948162",
        "revenue_generated": 46464,
        "new_users": 3435,
        "inf_report_date_posted": "2019-12-22",
        "inf_report_link_posted": "https://www.codeproject.com/Questions/665",
        "channel": "twitter",
        "youtube_title": 'null',
        "insta_username": 'null',
        "twitter_screen_name": "kiran_padwal786"
    }
]

import itertools
from operator import itemgetter

# Sort proposals data by `proposal_id` key.
proposals = sorted(mydict, key=itemgetter('proposal_id'))
# for key,value in enumerate(mydict):
#     print(key,':',value)
data = []

# Display data grouped by `proposals`
for key, value in itertools.groupby(proposals, key=itemgetter('proposal_id')):
    proposal_dict = {}
    proposal_channels = []
    channel_details = {}
    inf_reports = []
    for i in value:
        none_value = 'null'
        temp_dict = {}
        temp_dict_inf_report = {}

        #common variables
        proposal_dict.update({'proposal_id':i.get('proposal_id')})
        proposal_dict.update({'campaign_id': i.get('campaign_id')})
        if i.get('inf_first_name')!=none_value:
            proposal_dict.update({'inf_first_name': i.get('inf_first_name')})
        if i.get('inf_last_name')!=none_value:
            proposal_dict.update({'inf_last_name': i.get('inf_last_name')})
        if i.get('inf_categories')!=none_value:
            proposal_dict.update({'inf_categories': i.get('inf_categories')})
        if i.get('inf_country')!=none_value:
            proposal_dict.update({'inf_country': i.get('inf_country')})
        if i.get('proposal_price')!=none_value:
            proposal_dict.update({'proposal_price': i.get('proposal_price')})
        if i.get('proposal_from_date')!=none_value:
            proposal_dict.update({'proposal_from_date': i.get('proposal_from_date')})
        if i.get('proposal_to_date')!=none_value:
            proposal_dict.update({'proposal_to_date': i.get('proposal_to_date')})
        if i.get('regions')!=none_value:
            proposal_dict.update({'regions': i.get('regions')})
        if i.get('video_cat_id')!=none_value:
            proposal_dict.update({'video_cat_id': i.get('video_cat_id')})
        if i.get('campaign_status')!=none_value:
            proposal_dict.update({'campaign_status': i.get('campaign_status')})
        #add more common variables here

        temp_dict.update({'channel_name':i.get('channel')})
        temp_dict.update({'channel_id': i.get('channel_id')})
        if i.get('youtube_title') != none_value:
            temp_dict.update({'youtube_title': i.get('youtube_title')})
        if i.get('insta_username') != none_value:
            temp_dict.update({'insta_username': i.get('insta_username')})
        if i.get('twitter_screen_name') != none_value:
            temp_dict.update({'twitter_screen_name': i.get('twitter_screen_name')})

        temp_dict.update({'revenue_generated': i.get('revenue_generated')})
        temp_dict.update({'new_users': i.get('new_users')})

        #inf reports
        temp_dict_inf_report.update({'channel_name': i.get('channel')})
        temp_dict_inf_report.update({'channel_id': i.get('channel_id')})
        temp_dict_inf_report.update({'inf_report_date_posted': i.get('inf_report_date_posted')})
        temp_dict_inf_report.update({'inf_report_link_posted': i.get('inf_report_link_posted')})
        # add more variables to inf reports here
        inf_reports.append(temp_dict_inf_report)

        if temp_dict not in proposal_channels:
            proposal_channels.append(temp_dict)

        proposal_dict.update({'proposal_channels': proposal_channels})

        proposal_dict.update({'inf_reports': inf_reports})

    data.append(proposal_dict)
    # print(inf_reports)
for item in data:
    # print(item)
    for k,v in item.items():
        print(k,':',v)
