import requests
import click
from os import environ
from flask import Flask, request
from merge_coverage_data import read_coverage_and_operators
from mongo_client import MongoClient


ADDOK_URL = environ.get("ADDOK_URL")


app = Flask(__name__)


@app.route("/search")
def search_handler():
    if "q" not in request.args:
        return ("Argument `q` is required", 400)
    query = request.args["q"]
    r = requests.get(ADDOK_URL + "/search/", params={"q": query})
    if r.ok:
        points = r.json()["features"]
        if not points:
            return ("Cannot find provided address", 404)
        x, y = points[0]["geometry"]["coordinates"]
        mongo = MongoClient.get_instance()
        coverage = mongo.get_coverage(x, y)
        return coverage if coverage else ("Cannot find coverage for provided address", 404)
    else:
        app.logger.error(r.content)
        return ("Got error from addok service", 500)


@app.cli.command("init-coverage-collection")
@click.argument("operators", type=click.File("r"))
@click.argument("coverage", type=click.File("r"))
def init_mongo(operators, coverage):
    records = read_coverage_and_operators(operators, coverage)
    mongo = MongoClient.get_instance()
    mongo.drop_collection()
    mongo.init_index()
    mongo.bulk_add(records)

app.cli.add_command(init_mongo)
