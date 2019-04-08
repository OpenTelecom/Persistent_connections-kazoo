import requests
import json as j

server = 'http://18.218.219.1'


def get_items(item_type, account_id, item_id, auth):
    """
    get more information on data from websocket by requesting for more details

    """
    response = requests.get(
        f'{server}:8000/v2/accounts/{account_id}/{item_type}s/{item_id}', headers=get_headers(auth))
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


def get_response1():
    """
    Get the auth_token from crossbar
    :return: returns the http response from crossbar with auth_token
    """
    headers = {
        'Content-Type': 'application/json',
    }
    data = '{"data":{"credentials":"92b5841ef89f79c5b359226f24d194a4","account_name":"Farah Alaa"}}'

    _response = requests.put(
        server + ':8000/v2/user_auth', headers=headers, data=data)

    return _response


# Parse json file to get auth_token
def get_auth_token():
    """
    Parse json file to get auth_token

    :return: returns the auth_token parsed from the http response
    """
    key = get_response1()
    key = key.json()
    auth_token_og = key['auth_token']

    return auth_token_og


def get_api():

    var = 'yes'

    return var


def get_acc_id():
    """
    Parse json file for account id

    :return: returns acc id
    """
    _key = get_response1()
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


if __name__ == '__main__':
    # auth_token = get_auth_token()

    get = get_api()
    # parsed = get.json()

    # parsed = j.loads(get.json())

    print(get)
    # print(j.dumps(parsed, indent=2, sort_keys=True))
    # print(j.dumps(get, indent=2, sort_keys=True))
