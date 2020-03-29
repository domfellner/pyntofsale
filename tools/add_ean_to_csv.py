import pandas as pd
from argparse import ArgumentParser
from pathlib import Path
import hashlib
import math
from typing import Any
import random
import numpy as np
from PIL import Image
import os


def create_ean_13(seed: Any = None) -> str:
    """Generate EAN13 code depending on hash of seed.

    The generated EAN13 code will seem random due to hashing.

    Keyword Arguments:
        seed {Any} -- seed for hash. If None is given, the created EAN13 will be random (default: {None})

    Returns:
        str -- Generated EAN13 code
    """
    if seed is None:
        seed = random.randrange(2 ** 64)
    hash = hashlib.sha1(str(seed).encode("utf8")).hexdigest()
    raw_ean = "{:012d}".format(int(hash, 16) % 10 ** 12)
    result = append_checkdigit(raw_ean)
    return result


def append_checkdigit(raw_ean: str) -> str:
    """Append checkdigit to EAN code with missing checkdigit.

    Arguments:
        raw_ean {str} -- EAN code. Can be EAN8 or EAN13.

    Returns:
        str -- completed EAN code
    """
    sum1 = sum([3 * int(i) for i in raw_ean[-1::-2]])
    sum2 = sum([int(i) for i in raw_ean[-2::-2]])
    sum_ = sum1 + sum2
    checkdigit = 10 * math.ceil(sum_ / 10) - sum_
    result = raw_ean + str(checkdigit)
    return result


def main():
    # args = init_args()
    df = pd.read_csv(
        Path(__file__).parent.parent / "data/inventory.csv",
        decimal=",",
        delimiter=";",
        encoding="latin_1",
        index_col=0,
        dtype={"ean": str},
    )
    df = prepare_df(df)
    df = fill_eans(df)
    df.to_csv(Path(__file__).parent.parent / "data/filled_inventory.csv")
    eans = extract_print_ean_csv(df)
    eans.to_csv(
        Path(__file__).parent.parent / "data/eans_to_be_printed.csv",
        header=False,
        index=False,
    )


def extract_print_ean_csv(df):
    eans = df.loc[(df["labelable"] == 1) & (df["is_labeled"] == 0), ("amount", "ean")]
    eans = eans.loc[eans.index.repeat(eans.amount)]["ean"]
    return eans


def fill_eans(df):
    df["ean"] = df.apply(
        lambda row: create_ean_13(row.name)
        if pd.isna(row["fixed_ean"])
        else row["ean"],
        axis=1,
    )
    assert not any(df["ean"].duplicated())
    return df


def prepare_df(df):
    df["labelable"] = df["labelable"].fillna(0).astype(bool)
    df["is_labeled"] = df["is_labeled"].fillna(0).astype(bool)
    return df


def init_args():
    parser = ArgumentParser("Read inventory from csv and add EAN-13 to it")
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path(__file__).parent.parent / "data" / "inventory.csv",
        help="Path to the inventory csv file",
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
