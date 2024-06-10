import argparse
import pathlib
import dataclasses
import io


@dataclasses.dataclass(frozen=False)
class Operator:
    MCC: str = None
    MNC: str = None
    name: str = None
    operator: str = None

    @property
    def is_initialized(self):
        return self.MCC is not None \
            and self.MNC is not None \
            and (self.name is not None or self.operator is not None)
    

TABLE_FIELDS = (
    "MCC",
    "MNC",
    "name",
    "operator",
    "status",
    "bands",
    "notes",
)


def build_args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        default="./data-coverage/operators_table_wiki.md",
        help="Filepath to the table with operators data in wikitable format"
    )
    return parser


def read_operators(f: io.TextIOWrapper) -> list[Operator]:
    fields_to_set = set(f.name for f in dataclasses.fields(Operator))
    result = list[Operator]()
    current_record = Operator()
    current_field_iterator = iter(TABLE_FIELDS)
    for line in f.readlines():
        line = line.strip()
        if line.strip() == "|-":
            if current_record.is_initialized:
                result.append(current_record)
            current_record = Operator()
            current_field_iterator = iter(TABLE_FIELDS)
        else:
            line = line.lstrip("| ")
            values = line.split("||")
            for value in values:
                if value:
                    value = value.split("<ref")[0]  # remove HTML link
                    value = value.replace("[[", "").replace("]]", "")  # remove wiki link
                    if "|" in value:
                        value = value.split("|")[1]  # use wiki link alias
                    value = value.strip()
                    current_field = next(current_field_iterator)
                    if current_field in fields_to_set:
                        setattr(current_record, current_field, value)

    return result


def print_head(table_path: pathlib.Path | None = None):
    if table_path is None:
        parser = build_args_parser()
        args = parser.parse_args()
        table_path = pathlib.Path(args.path)
    with table_path.open(encoding="utf-8") as f:
        records = read_operators(f)
        print(records)


if __name__ == "__main__":
    print_head()
