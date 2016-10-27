from flask import render_template
from flask import g
from flask import request
from flask import abort
from flask import redirect, url_for
from flask.json import jsonify
import psycopg2 as pg
from flask import Flask
from flask.ext.cache import Cache
import requests
import configparser

app = Flask(__name__)
app.config.from_object(__name__)

config = configparser.ConfigParser()
_ = config.read('config.ini')

app.config.update(dict(
    DATABASE=config.get('Database', 'database'),
    SECRET_KEY=config.get('Application', 'secretkey'),
    USERNAME=config.get('Database', 'username'),
    PASSWORD=config.get('Database', 'password'),
    HOST=config.get('Database', 'host'),
    OPENWEATHERMAPKEY=config.get('ApiKeys', 'openweathermap')
))

cache = Cache(app, config={'CACHE_TYPE': 'simple'})


def connect_db():
    """Connect to the local db"""
    conn = pg.connect(
        database=app.config['DATABASE'],
        user=app.config['USERNAME'],
        password=app.config['PASSWORD'],
        host=app.config['HOST'])
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
    cur.execute('select * from users limit 100')
    res = cur.fetchall()
    return res


def add_db_user(name, password):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute('insert into users (username, password) values (%s, %s)', (name, password))
    except Exception as e:
        print(e)
    cur.close()
    conn.commit()


@app.route('/db')
def db():
    res = run_db_user_search()
    return jsonify(res)


@app.route('/')
def hello_world():
    return "Hello world!"


@app.route('/signin')
def signin():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/weather')
@cache.cached(timeout=60*10)
def get_weather():
    url = 'http://api.openweathermap.org/data/2.5/forecast/city?id=5786882&APPID=' + \
          app.config['OPENWEATHERMAPKEY']
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    else:
        return "API call failed."


@app.route('/signupuser', methods=["POST"])
def signupuser():
    name = request.form['username']
    password = request.form['password']
    add_db_user(name, password)
    return redirect(url_for('db'))


@app.route('/login', methods=["POST"])
def login():
    if request.method == "POST":
        name = request.form['username']
        password = request.form['password']
        if name == "edna" and password == "test":
            return "SignIn successful"
        else:
            abort(401)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
