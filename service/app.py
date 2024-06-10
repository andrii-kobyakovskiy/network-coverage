import requests
from os import environ
from flask import Flask, request


ADDOK_URL = environ.get("ADDOK_URL")


app = Flask(__name__)


@app.route("/search")
def search_handler():
    if "q" not in request.args:
        return ("Argument `q` is required", 404)
    query = request.args["q"]
    r = requests.get(ADDOK_URL + "/search/", params={"q": query})
    if r.ok:
        return r.json()
    else:
        app.logger.error(r.content)
        return ("Got error from addok service", 500)
