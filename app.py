from flask import Flask
from flask import render_template
from flask import request
from flask import abort
from flask import redirect, url_for

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello world!"


@app.route('/info/<username>')
def test_list(username):
    return 'User %s' % username


@app.route('/signin')
def signin():
    return render_template('login.html')



@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/projects/')
def projects():
    if request.method == "GET":

        return "You used the xxx  GET method. Project list"
    else:
        return "You did not use the GET method."


@app.route('/about')
def about():
    return "About page."


@app.route('/abort')
def aborter():
    abort(401)


@app.route('/multiply')
def multiply():
    params = request.args.get('key', '')
    return "You added param: %s" % params


@app.errorhandler(401)
def not_authorised(error):
    return "Not authorised"


@app.route('/login', methods=["POST"])
def login():
    if request.method == "POST":
        name = request.form['username']
        password = request.form['password']
        print(name)
        if name == "edna" and password == "test":
            return "SignIn successful"
        else:
            abort(401)

if __name__ == "__main__":
    app.run(debug=True)
