# How to create a kazoo hook - PYTHON

Commonly referred to as reverse API's, webhooks are outbound http posts sents asynchronously from one server to another. 
A website implementing webhooks will send a notification to a registered URL,
when an event happens. So instead of polling, the server registers a URL and gets notified, in realtime if an event occurs.

**To Start, import the `requests` library and get a lists of all available hooks from kazoo**

```
import requests
import json
```

First get your `auth_token` from kazoo

***The "credential" field is MD5/SHA1 hash of your {username:Password}***

```
def get_token():
    headers = {
    ‘Content-Type’: ‘application/json’,
    }
    
    data = ‘{‘data’: {“credentials”: “{MD5 hash of username: Password}”, “account_name”:”master”}}’
   
    Response = requests.put(‘{SERVER}://8000/v2/user_auth’, headers=headers, data=data)

    Return response.
```

***The response should look something like this if successful:***

```
{'page_size': 1, 'data': {'owner_id': '915c65317ceef0c7d8998117b68d2e15', 'account_id': 'c8c75d13eccbf803ca789e2ef83c0e11', 'reseller_id': 'c8c75d13eccbf803ca789e2ef83c0e11', 'is_reseller': True, 'account_name': 'master', 'language': 'en-US', 'apps': 
[{'id': '43b5a09e9000fbfc9fd16b78c98b1057', 'name': 'accounts', 'api_url': 'http://18.218.219.1:8000/v2', 'label': 'Accounts'},
{'id': 'd28cfe734a714c2390f53821e7543f89', 'name': 'voip', 'api_url': 'http://18.218.219.1:8000/v2', 'label': 'SmartPBX'}, 
{'id': 'f7a7b18bda3b60418fd6381fe904d6f8', 'name': 'webhooks', 'api_url': 'http://18.218.219.1:8000/v2', 'label': 'Webhooks'}]},
'revision': 'automatic', 'timestamp': '2019-03-19T17:02:09Z', 'version': '4.3.23', 'node': 'SQQOm6kA-oMWqoSqEEr_kw', 'request_id': '8a6b612ca22aa16c57c0b89920dec383',
'status': 'success', 
'auth_token': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRiMGFiMzRhNmU4NjUyZDAzNTNjODU1NDZjNjgxODQwIn0.eyJpc3MiOiJrYXpvbyIsImlkZW50aXR5X3NpZyI6ImN0MHJsdnZTUEVjRlptc01fZmlxd3dpYnBuaWM4OGowNmtBX2tpQVhxU28iLCJhY2NvdW50X2lkIjoiYzhjNzVkMTNlY2NiZjgwM2NhNzg5ZTJlZjgzYzBlMTEiLCJvd25lcl9pZCI6IjkxNWM2NTMxN2NlZWYwYzdkODk5ODExN2I2OGQyZTE1IiwibWV0aG9kIjoiY2JfdXNlcl9hdXRoIiwiZXhwIjoxNTUzMDE4NTI5fQ.eh6wtThWWtvUEGIckzy1tWPeyQDxI9QhiXf7EhyIvrX4Dj--xTV-efs7EMkTyPIioLp-T4QPJZfwubSBsBgGYDWRkJDW8a1_YlN1XhtwhBlCtS01982jwMV7nuzGo1ED6E5ca5Lz1s6XDOjVwV3ogr97Nicg6cIriCI-s5_fpCAU20RNwjB5aPAz0NoMVeu6dOqm0DCCobJrmrby0rDgDM_KXvYqwOB8f8ACr9ZRuNKmPnINDUtt_nLUFmskORuvy-bmbZZL8jxHvjj-td-f3yrCxrKymoI5XFjLx61ygnXkUQIBQoHPN9nK_Nhcemd-}
```
The auth_token changes with every request, so make sure to request this every time you want to PUT,GET.

```
def get_auth_token():
        parse = get_response()
        parse = get.json()
        auth_token = parse.get[‘auth_token’]
        return auth_token
```

Take a look at the kazoo/webhooks documentation [https://github.com/2600hz/kazoo/blob/master/applications/crossbar/doc/webhooks.md](Kazoo/webhooks)

**For this guide we will create a webhook for user_deleted event**

For `my_server` put the URL kazoo should use to send you notifications
```
# This will be used in the `data` field of the request sent to kazoo

message = {"data": {
        "name": "Destroy2",
        "uri": {my_server},
        "http_verb": "post",
        "hook": "object",
        "action": "doc_deleted",
        "type": "account",
        "retries": 3,
        "custom_data": {
            "type": "user",
            "action": "doc_deleted"
        }
    }
```

Turn `message` into json
```
def  jsonify(d):
        jsonfied = j.dumps(d)
        return jsonfied
``` 

```

def create_webhook():
	headers = {‘Content Type’: ‘application/json’,
	            ‘X-auth-token’: {auth_token},
               }

response = requests.put({SERVER}:8000/v2/accounts/'account_id'/webhooks', headers=headers, data=jsonify(message))

Return response

```
you have now successfully connected to kazoo webhooks and should get notifications as soon as the events occure.

**NOTE****
The request sent by kazoo is in the format `x-www-form-urlencoded` and not `JSON`
Most webservers that implement webhooks like `twilio` and  `Stripe` all use `form` for `POST` requests.

