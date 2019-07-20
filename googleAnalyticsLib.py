import googleanalytics as ga
client_id = '886588013230-dc0iqr4usoddcs7ngjg0gbp90dkh569d.apps.googleusercontent.com'
client_secret = 'JdNe4oaXXOUcTkXFdBvBAqII'
accounts = ga.authenticate(client_id=client_id,client_secret=client_secret)
profile = accounts[0].webproperties[0].profile
pageviews = profile.core.query.metrics('pageviews').range('yesterday').value
print(pageviews)