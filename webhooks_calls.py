from flask import Flask
from flask import request
from flask import json
from datetime import datetime
from account import Account
from kazoo_put import get_auth_token, get_items
from data_alchemy import insert_data
from call import Call

app = Flask(__name__)

directory = {}


@app.route('/')
def api_root():
    return 'Welcome guys'


def parse_request(req):
    """
    Parses application/json request body data into a Python dictionary
    """
    return json.dumps(req.json)


@app.route('/kazoo', methods=['POST'])
def api_kz_hook():
    with app.test_request_context('/kazoo', method='POST'):
        """
        now you can do something with the request until the
        end of the with block, such as basic assertions:
        """

        assert request.path == '/kazoo'
        assert request.method == 'POST'
        print('assertions passed')

    callee_id = request.form.get('callee_id_name')
    caller_id = request.form.get('caller_id_name')
    account_id = request.form.get('account_id')
    user_id = request.form.get('owner_id')
    date_time = int(request.form.get('timestamp'))
    date_time_obj = datetime.fromtimestamp(date_time)
    call_id = request.form.get('call_id')
    duration_seconds = request.form.get('duration_seconds')

    user = get_items('user', account_id, user_id, get_auth_token())
    print('this is user:{}'.format(user))
    data = user['data']
    user_id1 = data.get('id')

    if request.form.get('call_direction') == 'outbound':
        directory['outbound'] = user_id1
    if request.form.get('call_direction') == 'inbound':
        directory['inbound'] = user_id1

    print('"this are the items : :from webhooks_calls "', caller_id, callee_id, account_id, date_time_obj)

    # print(request.form)
    print(directory)
    dir_len = len(directory)
    if dir_len == 2:
        print(dir_len)
        print('inserting data')
        insert_data('call', account_id, call_id, get_auth_token(), inbound=directory['inbound'], outbound=directory['outbound'], callee=callee_id, caller=caller_id, duration=duration_seconds)
    return 'ok'


if __name__ == '__main__':
    app.run(debug=True)
