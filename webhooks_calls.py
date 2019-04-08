from flask import Flask
from flask import request
from flask import json
from datetime import datetime
from kazoo_put import get_auth_token
from data_alchemy import insert_data

app = Flask(__name__)


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

    # if request.headers['Content-Type'] == 'x-www-form-urlencoded':
    callee_id = request.form.get('callee_id_name')
    caller_id = request.form.get('caller_id_name')
    account_id = request.form.get('account_id')
    date_time = int(request.form.get('timestamp'))
    date_time_obj = datetime.fromtimestamp(date_time)

    print('this are the items: ', caller_id, callee_id, account_id, date_time_obj)

    print(request.form)
    return 'ok'

    # print(request.form)
    # type_t = request.args.get('type')
    # id_t = request.args.get('id')
    # account_id = request.args.get('account_id')
    # print(account_id, type_t, action, id_t)


if __name__ == '__main__':
    app.run(debug=True)
