from flask import Flask
import logging

app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def main_page():
    return "<h1>Test</h1>"


if __name__ == '__main__':
    app.run(debug=True)
