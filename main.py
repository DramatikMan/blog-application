import flask

from config import DevConfig


app = flask.Flask(__name__)
app.config.from_object(DevConfig)
app.url_map.strict_slashes = False


@app.route('/')
def hello():
    return '<h1>hello world!</h1>'


if __name__ == '__main__':
    app.run()
