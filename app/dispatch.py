from actions import actions
from analysis import analysis

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

def map_analysis(fname, data, column):
    """
    Applies an analysis to every item in the requested columns, or every item
    in all columns
    """
    a = analysis.get(fname, None)
    if a:
        evaluation = a(data, column)
        return fname, evaluation
    return fname, None
