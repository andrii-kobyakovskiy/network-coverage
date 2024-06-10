import requests
import click
import pathlib
from os import environ
from flask import Flask, request
from merge_coverage_data import read_coverage_and_operators


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


@app.cli.command("read-coverage")
@click.argument("operators", type=click.File("r"))
@click.argument("coverage", type=click.File("r"))
def read_operators_cmd(operators, coverage):
    records = read_coverage_and_operators(operators, coverage)
    print(list(records)[:10])

app.cli.add_command(read_operators_cmd)
