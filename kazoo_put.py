import requests
import json as j


server = 'http://18.218.219.1'
interaction_id = '63722564695-04eab61e'


def get_items(item_type, account_id, item_id, auth):
    """
    get more information on data from websocket by requesting for more details

    """
    response = requests.get(
        '{}:8000/v2/accounts/{}/{}s/{}'.format(server, account_id, item_type, item_id), headers=get_headers(auth))
    return response.json()


def get_headers(auth):
    """
    custom headers for requests

    :param auth: authentication key
    :return: returns the default header
    """
    return {
        'X-Auth-Token': auth,
        'Content-Type': 'application/json',
    }


def get_response():
    """
    Get the auth_token from crossbar
    :return: returns the http response from crossbar with auth_token
    """
    headers = {
        'Content-Type': 'application/json',
    }
    data = '{"data":{"credentials":"92b5841ef89f79c5b359226f24d194a4","account_name":"master"}}'

    _response = requests.put(
        server + ':8000/v2/user_auth', headers=headers, data=data)

    return _response


# Parse json file to get auth_token
def get_auth_token():
    """
    Parse json file to get auth_token

    :return: returns the auth_token parsed from the http response
    """
    key = get_response()
    key = key.json()
    auth_token_og = key['auth_token']

    return auth_token_og


def get_acc_id():
    """
    Parse json file for account id

    :return: returns acc id
    """
    _key = get_response()
    _key = _key.json()
    y = _key['data']['account_id']

    return y


def get_socket_id(auth):
    """
    Request available socket ids

    """
    acc_id = get_acc_id()
    headers = {'X-Auth-Token': auth,
               }
    ids = requests.get(server + ':8000/v2/accounts/' +
                       acc_id + '/websockets', headers=headers)

    return ids


def get_web_sockets():

    """
    Get all available websocket bindings
    :return: returns a list of available websocket bindings available

    """

    wesockets = requests.get(server + ':8000/v2/websockets')

    return wesockets


def get_users():
    # GET /v2/accounts/{ACCOUNT_ID}/users
    auth = get_auth_token()
    acc_id = get_acc_id()

    headers = get_headers(auth)

    _response = requests.get(
        server + ':8000/v2/accounts/{}/users'.format(acc_id), headers=headers)
    return _response
# curl -v -X GET \
#     -H "X-Auth-Token: {AUTH_TOKEN}" \
#     http://{SERVER}:8000/v2/accounts/{ACCOUNT_ID}/cdrs/interaction


def get_cdr():
    auth = get_auth_token()
    acc_id = get_acc_id()

    headers = get_headers(auth)
    response = requests.get(f'{server}:8000/v2/accounts/{acc_id}/cdrs/interaction', headers=headers)

    return response
# curl -v -X GET \
#     -H "X-Auth-Token: {AUTH_TOKEN}" \
#     http://{SERVER}:8000/v2/accounts/{ACCOUNT_ID}/cdrs/legs/{INTERACTION_ID}


def get_cdr_specific():
    auth = get_auth_token()
    acc_id = get_acc_id()

    headers = get_headers(auth)
    response = requests.get(f'{server}:8000/v2/accounts/{acc_id}/cdrs/legs/{interaction_id}', headers=headers)

    return response


if __name__ == '__main__':
    auth_token = get_auth_token()

    get = get_cdr_specific()
    parsed = get.json()

    print(j.dumps(parsed, indent=2, sort_keys=True))
