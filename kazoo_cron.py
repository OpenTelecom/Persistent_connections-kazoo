from kazoo_put import get_users
import json
from config import ACC_ID, AUTH_TOKEN

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
        acc_id = ACC_ID
        insert_data(item_type, acc_id, item_id, AUTH_TOKEN)


if __name__ == '__main__':
    insert_users()

