"""Helpers for arrays / iterables."""

def flatten(list_of_lists):
    """
    Flattens a list of lists (or lists mixed w scalars) to one list.

    >>> flatten([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> flatten([1, 2, 3, [4, 5, 6], 7, 8, 9])
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    flattened = []
    for nested in list_of_lists:
        if isinstance(nested, (list, tuple)):
            flattened.extend(nested)
        else:
            flattened.append(nested)
    return flattened

def chunks(array, chunk_size):
    """
    Returns a list of sized chunks from array.

	>>> chunks([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
	[[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [array[i:i + chunk_size] for i in range(0, len(array), chunk_size)]
