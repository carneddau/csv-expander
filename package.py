#!/usr/bin/env python
import PyInstaller.__main__

from csv_expander.utils import package

PyInstaller.__main__.run(
    [
        "main.py",
        "--hidden-import",
        "dotenv",
        "--onefile",
        "--copy-metadata",
        f"{package()}",
    ]
)
