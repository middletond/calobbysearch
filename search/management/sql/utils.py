"""Simple helpers for SQL queries.

"""

def inserted_rows(cursor):
    """Get number of inserted rows from `cursor` object.

    """
    status = cursor.statusmessage

    if not status:
        return 0
    if "INSERT" not in status:
        return 0
    tokens = status.split() # ['INSERT', 0, 1000,]
    return int(tokens[-1]) if len(tokens) == 3 else 0
