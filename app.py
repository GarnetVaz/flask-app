from flask import Flask
from flask import render_template
from flask import request
from flask import abort
from flask import g
import psycopg2 as pg

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE='Website',
    SECRET_KEY='secretkey',
    USERNAME='Garnet',
    PASSWORD='edna1986'
))


def connect_db():
    """Connect to the local db"""
    conn = pg.connect(
        database=app.config['DATABASE'],
        user=app.config['USERNAME'],
        password=app.config['PASSWORD'],
        host='localhost')
    return conn


def get_db():
    if not hasattr(g, 'conn'):
        g.conn = connect_db()
    return g.conn


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'conn'):
        g.conn.close()


def init_db():
    conn = connect_db()
    cur = conn.cursor()
    with app.open_resource('schema.sql', mode='r') as f:
        cur.execute(f.read())
    conn.commit()
    cur.close()


@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database')


def run_db_user_search():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('select * from users limit 1')
    res = cur.fetchone()
    return res


@app.route('/db')
def db(name=None):
    uuid, uname, passw = run_db_user_search()
    return "User {0} Password {1} uuid {2}".format(uname, passw, uuid)


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
    init_db()
    app.run(debug=True)
