import psycopg2
import yaml
from flask import Flask, g

app = Flask(__name__)
CONFIG_PATH = "config.yml"


def get_db_cursor():
    if 'db_conn' not in g:
        with open(CONFIG_PATH, "r") as config_file:
            config = yaml.load(config_file)
        g.db_conn = psycopg2.connect(**config["sql"])
    if 'db_cur' not in g:
        g.db_cur = g.db_conn.cursor()
    return g.db_cur


@app.teardown_appcontext
def on_teardown(_):
    db_cur = g.pop("db_cur", None)
    if db_cur is not None:
        db_cur.close()
    db_conn = g.pop("db_conn", None)
    if db_conn is not None:
        db_conn.commit()
        db_conn.close()


@app.route('/')
def index():
    return "Hello World"
