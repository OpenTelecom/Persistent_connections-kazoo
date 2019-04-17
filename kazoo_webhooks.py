from flask import Flask
from flask import request
from flask import json


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
        TEST CASE
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
        TEMPLATE
        """

        assert request.path == '/kazoo'
        assert request.method == 'POST'
        print('assertions passed')

    print(request.form)
    return 'ok'


if __name__ == '__main__':
    app.run(debug=True)
