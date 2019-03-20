# How to Connect Websockets to Kazoo - PYHTHON

**What are Websockets?**

Websockets are an upgrade to HTTP, they allow bi-directional communication between a server and a client. The client sends a request to the server to UPGRADE connection, and if the server agrees, a 200 ok message sent back and a persistent connection is established. This reduces the latency in server-client communication, as only one tcp connection is needed for messages to both ways.

### Background

To get a quick understanding of how websockets are implemented by kazoo, take a look at [https://github.com/2600hz/kazoo/blob/master/applications/crossbar/doc/websockets.md]

Kazoo’s backend implementation of websockets is implemented by the `blackhole` application. The documentation above shows what the UPGRADE http request should look like and how to subscribe to certain events.

`blackhole` listens on port 5555, and on port 7777 if it is a secure connection(wss). This is important because the communications happen through this port. 



*Let’s get started.*
If you have troubles with setting up kazoo, Check out my guide on how to set up a kazoo instance using AWS Centos server.

Import these libraries

***The "credential" field is MD5/SHA1 hash of your {username:Password}***

```
import requests
import json
import websockets

# Using RESTful API get the auth_token to use while sending an upgrade 
HTTP request to blackhole

def get_token():
    headers = {
    ‘Content-Type’: ‘application/json’,
    }

    data = ‘{‘data’: {“credentials”: “{MD5 hash of username: Password}”, “account_name”:”master”}}’
    Response = requests.put(‘{SERVER}://8000/v2/user_auth’, headers=headers, data=data)

    Return response.
```
Now we can parse the response to get the `auth_token`

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
Using the `get[]`, method avoids KeyNotFound errors caused if the response does not have the auth_token key.

Now you can bind to any available sockets on blackhole, example : User_created event : 

***'Request_id' field is optional, you can use your account_id if you want***

```
def user_created():
    message = {
    ‘Action’: ‘subscribe’,
    ‘Auth_token’: auth_token,
    ‘Request_id’: {anything},
    ‘Data’: { 
    ‘Account_id’: acc_id,
    ‘Binding’: ‘object.doc_created.user’
}
}
    async def subscribe():
        sync with w.connect(f’ws://{HOST}:5555’) as ws:
                await ws.send(j.dumps(message))
                try:
                    response = await ws.recv()
                    print(response)
                    except: ConnectionClosed:
                    print(‘connection closed’)
        
     async for message in ws:
              await consumer(message)
```
** the consumer method is anything you want to do with the message returned by the socket.

```
def consumer(message):
        print(message)
```
Now run the program and you are all connected.

