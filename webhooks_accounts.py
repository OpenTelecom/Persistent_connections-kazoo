from flask import Flask
from flask import request
from flask import json
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
    item_id = request.form.get('id')
    item_type = request.form.get('type')
    account_id = request.form.get('account_id')

    print('this are the items: ', item_type, item_id, account_id)
    insert_data(item_type, account_id, item_id, get_auth_token())

    # print(request.form)
    return 'ok'

    # print(request.form)
    # type_t = request.args.get('type')
    # id_t = request.args.get('id')
    # account_id = request.args.get('account_id')
    # print(account_id, type_t, action, id_t)


if __name__ == '__main__':
    app.run(debug=True)
