from collections import defaultdict
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


def check_indices(rows: list[list[str]]) -> int:
    max_index = 0
    for line, row in enumerate(rows, start=1):
        try:
            new_index = int(row[0])
            if new_index > max_index:
                max_index = new_index
        except ValueError as err:
            err_console.print(
                f"Row {line}: Could not convert '{row[0]}' to an integer."
            )
            raise Exit(1) from err
    return max_index


def check_for_duplicates(rows: list[list[str]]):
    # console.print(rows.sort(key=func))

    count_dict = defaultdict(list)
    indices = [row[0] for row in rows]
    for i, item in enumerate(indices, start=1):
        count_dict[item].append(i)
    dupes_only = {k: v for k, v in count_dict.items() if len(v) > 1}
    if len(dupes_only.keys()) != 0:
        err_console.print_json(data={"duplicates": dupes_only})
        raise Exit(1)


def expand_csv(file_name: PathLike, backup: bool):
    # Truncate all whitespace and empty rows
    with uopen(file_name) as rdr, uopen(file_name, "r+") as wrtr:
        for line in rdr:
            if line.strip():
                wrtr.write(line)
        wrtr.truncate()

    with uopen(file_name, "r") as file:
        lst = list(reader(file))
        # Error out if duplicates are found
        check_for_duplicates(lst)

        # Check all indices can be cast to int
        max_index = check_indices(lst)

        # Sort
        lst.sort(key=lambda x: int(x[0]))

        # Add empty rows to missing gaps
        expand_rows(lst, max_index)

    if backup:
        backup_file(file_name)

    with uopen(file_name, "w", newline="") as csvfile:
        csv_writer = writer(csvfile, quoting=QUOTE_MINIMAL)
        csv_writer.writerows(lst)


def expand_rows(lst: list[list[str]], max_index: int):
    for i in range(max_index):
        index_matches = int(lst[i][0]) == i + 1
        if not index_matches:
            blank_row = [str(i + 1)] + ([""] * (len(lst[i]) - 1))
            lst.insert(i, blank_row)
        if i == max_index - 1:
            break
