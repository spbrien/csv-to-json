"""
Simple, one-off actions that can be applied
regardless of schema
"""

from functions import *

actions = {
    'infer_types': infer_types,
    'convert_to_ascii_with_html': convert_to_ascii_with_html,
    'convert_to_ascii_with_ignore': convert_to_ascii_with_ignore,
    'remove_quotes': remove_quotes,
    'split_by_comma': split_by_comma
}
