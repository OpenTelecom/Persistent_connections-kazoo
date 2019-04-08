from kazoo_put import get_users
import json
from kazoo_put import get_acc_id, get_auth_token

from data_alchemy import insert_data


def insert_users():
    print('hello from kazoo_cron.py')
    response = get_users()
    parsed = response.json()
    users = json.dumps(parsed, indent=2, sort_keys=True)
    users_dict = json.loads(users)

    for customer in users_dict['data']:
        item_type = 'user'
        item_id = customer.get('id')
        acc_id = get_acc_id()
        insert_data(item_type, acc_id, item_id, get_auth_token())


if __name__ == '__main__':
    insert_users()


