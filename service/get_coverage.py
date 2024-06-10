import csv
import argparse
import pathlib
import dataclasses
import io
from typing import Iterable


@dataclasses.dataclass(frozen=False)
class Coverage:
    operator: str
    x: int
    y: int
    has_2g: bool
    has_3g: bool
    has_4g: bool


def build_args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        default="./data-coverage/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv",
        help="Filepath to the table with coverage data"
    )
    return parser


def read_coverage(f: io.TextIOWrapper) -> Iterable[Coverage]:
    reader = csv.DictReader(
        f,
        fieldnames=dataclasses.fields(Coverage),
        delimiter=";",
    )
    for record in reader:
        yield Coverage(**{
            # values provided by the DictReader are raw strings
            # at the same time all values in provided CSV file are stored as integers
            f.name: f.type(int(v))  # cast a value to annotated type
            for f, v in record.items()
        })


def print_head(table_path: pathlib.Path | None = None):
    if table_path is None:
        parser = build_args_parser()
        args = parser.parse_args()
        table_path = pathlib.Path(args.path)
    with table_path.open(encoding="utf-8") as f:
        records = read_coverage(f)
        print(list(records[:10]))


if __name__ == "__main__":
    print_head()
