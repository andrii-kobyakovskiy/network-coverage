import argparse
import dataclasses
import pathlib
import io
import pyproj
from typing import Iterable
from get_coverage import read_coverage, Coverage
from get_operators import read_operators, Operator


@dataclasses.dataclass
class Location:
    type: str
    coordinates: list[int]

    @classmethod
    def Point(cls, x: int, y: int):
        return cls(type="Point", coordinates=[x, y])


@dataclasses.dataclass
class CoverageGeoRecord:
    location: Location
    operator: str
    has_2g: bool
    has_3g: bool
    has_4g: bool


def build_args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--coverage-path",
        default="./data-coverage/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv",
        help="Filepath to the table with coverage data"
    )
    parser.add_argument(
        "--operators-path",
        default="./data-coverage/operators_table_wiki.md",
        help="Filepath to the table with operators data in wikitable format"
    )
    return parser


def merge_coverage_data(operators: list[Operator], coverage: Iterable[Coverage]) -> Iterable[CoverageGeoRecord]:
    lambert = pyproj.Proj('+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs')
    wgs84 = pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
    coordinates_transformer = pyproj.Transformer.from_proj(proj_from=lambert, proj_to=wgs84)
    operators_index = {o.MCC + o.MNC: o for o in operators}
    for c in coverage:
        operator_repr = c.operator
        if operator_repr in operators_index:
            operator_obj = operators_index[operator_repr]
            operator_repr = operator_obj.name or operator_obj.operator
        x, y = coordinates_transformer.transform(c.x, c.y)
        yield CoverageGeoRecord(
            operator=operator_repr,
            location=Location.Point(x, y),
            has_2g=c.has_2g,
            has_3g=c.has_3g,
            has_4g=c.has_4g,
        )


def read_coverage_and_operators(operators: io.TextIOWrapper, coverage: io.TextIOWrapper) -> Iterable[CoverageGeoRecord]:
    return merge_coverage_data(
        read_operators(operators),
        read_coverage(coverage),
    )

def print_head(coverage_path: pathlib.Path | None = None, operators_path: pathlib.Path | None = None):
    if coverage_path is None or operators_path is None:
        parser = build_args_parser()
        args = parser.parse_args()
        coverage_path = pathlib.Path(args.coverage_path)
        operators_path = pathlib.Path(args.operators_path)
    with operators_path.open(encoding="utf-8") as o, coverage_path.open() as c:
        records = list(read_coverage_and_operators(o,c))
        print(records[:10])


if __name__ == "__main__":
    print_head()
