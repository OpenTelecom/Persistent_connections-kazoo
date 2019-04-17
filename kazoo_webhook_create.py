import json as j
import requests
import kazoo_websocket as ws
from config import KAZOO_SERVER, CHANNEL_DESTROY_WEBHOOKS, ACC_ID, HEADERS


# get the webhooks available
def get_webhooks():
    """
    get the webhooks available
    :return: a list of all available webhooks

    """
    response = requests.get(f'{KAZOO_SERVER}:8000/v2/webhooks', headers=HEADERS)

    return response


def create_webhook():
    """
    create a hook to a specific event, uses message above as the data sent
    :return:
    """

    response = requests.put(KAZOO_SERVER + ':8000/v2/accounts/' + ACC_ID + '/webhooks', headers=HEADERS, data=ws.jsonify(CHANNEL_DESTROY_WEBHOOKS))

    return response


if __name__ == '__main__':
    get = create_webhook().text

    parsed = j.loads(get)

    print(j.dumps(parsed, indent=2, sort_keys=True))
