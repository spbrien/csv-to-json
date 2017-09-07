from app.utils import map_dataframe, apply_to_column


# Check if we have homogeneous types in a column
@apply_to_column
def has_homogeneous_types(column):
    iseq = iter(column)
    first_type = type(next(iseq))
    return first_type if all( (type(x) is first_type) for x in iseq ) else False
