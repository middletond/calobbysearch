"""Helper for parsing correct bill names from text.

"""
import re

from utils.arrays import flatten

DELIMITERS = (",", ";", " ",)
PREFIXES = ("AB", "ABX1", "ACA", "ACR", "AJR", "HR", "SB", "SBX1", "SCA", "SCR", "SJR", "SR",)
BILL_NAME_FORMAT = "{} {}"

# The simplest pattern to parse -- it was
# what they are *supposed* to use as a format.
SINGLE_BILL_PATTERN = r"AB\s?\d{1,4}" # "AB 1001", "SB 2"
BILL_NUMBER_PATTERN = r"(?<=[^\d])\d{1,4}\b"
BILL_TYPE_PATTERN = r"({})".format("|".join(prefix for prefix in PREFIXES))

# However, most common lobby activity submission format is:
# AB 23, 345, 1, 34; ACA 34, 34, 2, 445; SB 34, 8778, etc
PREFIX_BLOCK_PATTERN = r"(?:{prefix})s?\-?[\s\,[0-9\;\:]+(?=(?:[A-Za-z\-]|\.|$))"

def clean(text):
    TO_SINGLE_SPACE = (
        r"\n",
        r"\:",
        r"\-",
        r"\/",
        r"\s+",
    )
    TO_REMOVE = (
        r"(?<=\d)(\s+)?\-(\s+)?(?=\d)", # "AB 33 - 10" is actually "AB 3310"
    )
    if text is None:
        text = ""
    for pattern in TO_REMOVE:
        text = re.sub(pattern, "", text)
    for pattern in TO_SINGLE_SPACE:
        text = re.sub(pattern, " ", text)
    return text.strip()

def parse(text, unique=True):
    """Parse list of bill names from text."""
    text = clean(text)

    def bills_from(prefix):
        bills = []
        PREFIX_BLOCKS = re.compile(
            pattern=PREFIX_BLOCK_PATTERN.format(prefix=prefix),
            flags=re.IGNORECASE
        )
         # Now look for just the numbers within each block.
        for block in PREFIX_BLOCKS.findall(text):
            bill_nums = re.findall(BILL_NUMBER_PATTERN, block)
            bills.extend([BILL_NAME_FORMAT.format(prefix, num) for num in bill_nums])
        return bills

    bills = flatten(bills_from(prefix) for prefix in PREFIXES)
    if unique:
        bills = list(set(bills))
    return sorted(bills)

def parse_one(text):
    bill_names = parse(text)
    return bill_names[0] if bill_names else ""

def parse_number(text):
    bill_nums = re.findall(BILL_NUMBER_PATTERN, parse_one(text))
    return int(bill_nums[0]) if bill_nums else None

def parse_type(text):
    bill_types = re.findall(BILL_TYPE_PATTERN, parse_one(text))
    return bill_types[0] if bill_types else ""
