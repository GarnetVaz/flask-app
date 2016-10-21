from flask import Flask
from flask import url_for
from flask import request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello world!"


@app.route('/info/<username>')
def test_list(username):
    return 'User %s' % username


@app.route('/projects/')
def projects():
    if request.method == "GET":
        return "You used the GET method. Project list"
    else:
        return "You did not use the GET method."


@app.route('/about')
def about():
    return "About page."


@app.route('/multiply')
def multiply():
    params = request.args.get('key', '')
    return "You added param: %s" % params

if __name__ == "__main__":
    app.run(debug=True)
