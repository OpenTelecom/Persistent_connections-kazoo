from flask import Flask
from flask import request
from flask import json
from kazoo_put import get_items, get_auth_token
import insert_data as db

app = Flask(__name__)


def parse_request(req):
    """
    Parses application/json request body data into a Python dictionary
    """
    return json.dumps(req.json)


@app.route('/')
def api_root():
    return 'Welcome guys'


@app.route('/test')
def test():
    return "hello this is a test"


@app.route('/github', methods=['POST', 'GET'])
def api_gh_message():
    with app.test_request_context('/github', method='POST'):
        """
        now you can do something with the request until the
        end of the with block, such as basic assertions:
        """

        assert request.path == '/github'
        assert request.method == 'POST'
        print('assertions passed')

    payload = parse_request(request)
    if payload == 'null':
        return "Welcome to GitHub."
    else:
        if request.headers['Content-Type'] == 'application/json':
            get_info = json.dumps(request.json)
            print(get_info)
            return get_info


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

    response = get_items(item_type, account_id, item_id, get_auth_token())

    print('this is my response', response)

    user_name = response['data']['caller_id']['internal']['name']
    print(user_name)
    # response = json.loads(response)

    var = db.insert_user(user_name, response, item_id)
    print('this is var', var)

    print(request.form)
    return 'ok'

    # print(request.form)
    # type_t = request.args.get('type')
    # id_t = request.args.get('id')
    # account_id = request.args.get('account_id')
    # print(account_id, type_t, action, id_t)


if __name__ == '__main__':
    app.run(debug=True)
