from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello world!"


@app.route('/info/<username>')
def test_list(username):
    return 'User %s' % username


@app.route('/projects/')
def projects():
    return "Project list"


@app.route('/about')
def about():
    return "The about page"


if __name__ == "__main__":
    app.run(debug=True)
