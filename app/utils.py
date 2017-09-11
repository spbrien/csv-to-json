# ---------------------
# Utilities
# ---------------------

def map_dataframe(f):
    """
    Decorator to apply a function to every item in a pandas
    DataFrame, or optionally to every item in certain columns
    of the DataFrame.
    """
    def wrapper(data, columns=None):
        for item in data.columns:
            if columns:
                if item in columns:
                    data[item] = data[item].apply(f)
            else:
                data[item] = data[item].apply(f)
        return data
    return wrapper


def apply_to_column(f):
    """
    Decorator to apply a function to a pandas
    DataFrame column.
    """
    def wrapper(data, columns=None):
        return f(data[columns])

    return wrapper
