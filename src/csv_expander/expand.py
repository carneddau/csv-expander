from csv import QUOTE_MINIMAL, reader, writer
from os import PathLike
from pathlib import Path
from shutil import copy2

from typer import Exit

from .utils import err_console, uopen


def backup_file(file: PathLike):
    path = Path(file).resolve()
    suffixes = path.suffixes
    suffixes.append(".old")
    new_suffix = "".join(suffixes)

    backup = path.with_suffix(new_suffix)

    copy2(path, backup)


def check_rows(rows: list[list[str]]):
    previous_index = 0
    for line, row in enumerate(rows, start=1):
        if int(row[0]) <= previous_index:
            err_console.print(
                f"Index on line {line} is not greater than the pevious index."
            )
            raise Exit(1)
        previous_index = int(row[0])


def expand_csv(file_name: PathLike, backup: bool):
    with uopen(file_name, "r") as file:
        lst = list(reader(file))
        max_index = int(lst[-1][0])
        check_rows(lst)

        for i in range(max_index):
            index_matches = int(lst[i][0]) == i + 1
            if not index_matches:
                blank_row = [str(i + 1)] + ([""] * (len(lst[i]) - 1))
                lst.insert(i, blank_row)
            if i == max_index - 1:
                break

    if backup:
        backup_file(file_name)

    with uopen(file_name, "w", newline="") as csvfile:
        csv_writer = writer(csvfile, quoting=QUOTE_MINIMAL)
        csv_writer.writerows(lst)
