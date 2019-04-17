from configparser import ConfigParser
from kazoo_put import get_headers, get_auth_token, get_acc_id


KAZOO_HOST = '18.218.219.1'
KAZOO_SERVER = 'http://18.218.219.1'
WEBHOOKS_SERVER = ''
AUTH_TOKEN = get_auth_token()
HEADERS = get_headers(AUTH_TOKEN)
ACC_ID = get_acc_id()

DOC_CREATE_WEBHOOKS = {"data": {
        "name": "Destroy2",
        "uri": WEBHOOKS_SERVER,
        "http_verb": "post",
        "hook": "object",
        "action": "doc_created",
        "type": "account",
        "retries": 3,
        "custom_data": {
            "type": "user",
            "action": "doc_created"
        }
    }
}

DOC_CREATED_WEBHOOKS = {"data": {
        "name": "account3",
        "uri": WEBHOOKS_SERVER,
        "http_verb": "post",
        "hook": "object",
        "action": "doc_created",
        "type": "account",
        "include_subaccounts": "true",
        "retries": 3,
        "custom_data": {
            "type": "account",
            "action": "doc_created"
        }
    }
}

CHANNEL_CREATE_WEBHOOKS = {"data": {
        "name": "Get_Calls",
        "uri": WEBHOOKS_SERVER,
        "http_verb": "post",
        "hook": "channel_create",
        "retries": 3,
    }
}

CHANNEL_DESTROY_WEBHOOKS = {"data": {
        "name": "End_Calls",
        "uri": WEBHOOKS_SERVER,
        "http_verb": "post",
        "hook": "channel_destroy",
        "retries": 3,
    }
}


WEBSOCKET_CreateUser = {
    'action': 'subscribe',
    'auth_token': AUTH_TOKEN,
    'request_id': ACC_ID,
    'data': {
        'account_id': ACC_ID,
        'binding': 'object.doc_created.user'
    }
}

WEBSOCKET_CreateDevice = {
    'action': 'subscribe',
    'auth_token': AUTH_TOKEN,
    'request_id': ACC_ID,
    'data': {
        'account_id': ACC_ID,
        'binding': 'object.doc_created.device'
    }
}

WEBSOCKET_Channel_Create = {
    'action': 'subscribe',
    'auth_token': AUTH_TOKEN,
    'request_id': ACC_ID,
    'data': {
        'account_id': ACC_ID,
        'binding': 'call.CHANNEL_CREATE.*'
    }
}

WEBSOCKET_Channel_Destroy = {
    'action': 'subscribe',
    'auth_token': AUTH_TOKEN,
    'request_id': ACC_ID,
    'data': {
        'account_id': ACC_ID,
        'binding': 'call.CHANNEL_DESTROY.*'
    }
}


def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def config1(filename='database1.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db
