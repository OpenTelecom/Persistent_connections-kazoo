import json as j
import kazoo_put as kp
import requests
import kazoo_websocket as ws

my_server = 'http://cc036d94.ngrok.io/kazoo'
my_server1 = 'https://webhook.site/31b5f964-b43e-48c8-8073-a2e3b2934620'

HOST = '18.218.219.1'
auth_token = kp.get_auth_token()
acc_id = kp.get_acc_id()
server = kp.server
headers = kp.get_headers(auth=auth_token)

message = {"data": {
        "name": "Destroy",
        "uri": my_server,
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
}


message1 = {"data": {
        "name": "Destroy",
        "uri": my_server1,
        "http_verb": "post",
        "hook": "channel_destroy",
        "retries": 3,
    }
}


# get the webhooks available
def get_webhooks():
    """
    get the webhooks available
    :return: a list of all available webhooks

    """
    response = requests.get(f'{server}:8000/v2/webhooks', headers=headers)

    return response


def create_webhook():
    """
    create a hook to a specific event, uses message above as the data sent
    :return:
    """

    response = requests.put(kp.server + ':8000/v2/accounts/' + kp.get_acc_id() + '/webhooks', headers=headers, data=ws.jsonify(message))

    return response


if __name__ == '__main__':
    get = create_webhook().text

    parsed = j.loads(get)

    # #print(parsed)
    print(j.dumps(parsed, indent=2, sort_keys=True))
