import strconv

from app.utils import map_dataframe

# ---------------------
# Functions
# ---------------------

@map_dataframe
def infer_types(item):
    return strconv.convert(str(item))


@map_dataframe
def convert_to_ascii_with_html(item):
    if hasattr(item, 'encode'):
        return item.encode('ascii', 'xmlcharrefreplace')
    return item

@map_dataframe
def convert_to_ascii_with_ignore(item):
    if hasattr(item, 'encode'):
        return item.encode('ascii', 'ignore')
    return item

@map_dataframe
def split_by_comma(item):
    return item.split(',')

@map_dataframe
def remove_quotes(item):
    item = item.replace('"', '')
    item = item.replace("'", "" )
    return item

@map_dataframe
def to_lowercase(item):
    if isinstance(item, basestring):
        return item.lower()
    return item

@map_dataframe
def to_uppercase(item):
    if isinstance(item, basestring):
        return item.upper()
    return item
