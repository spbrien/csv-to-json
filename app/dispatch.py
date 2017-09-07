from actions import actions

def map_action(fname, data, columns=None):
    """
    Applies an action to every item in the requested columns, or every item
    in all columns
    """
    a = actions.get(fname, None)
    if a:
        data = a(data, columns=columns)
        return data, True
    return data, False

def map_analysis(fname, data, columns=None):
    """
    Applies an analysis to every item in the requested columns, or every item
    in all columns
    """
    a = actions.get(fname, None)
    if a:
        evaluation = a(data, columns=columns)
        return data, evaluation
    return data, None
