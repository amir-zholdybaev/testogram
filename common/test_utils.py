import json
from django.core.serializers.json import DjangoJSONEncoder


def convert_response_data_to_dict(data):
    """
    # Convert the response data into a dictionary including nested structures.

    This method differs from the built-in `dict()` function **by** doing a deep conversion.
    For example, it converts a nested `OrderedDict` into a dictionary without skipping it.
    This is useful for converting data to JSON format.

    ## Arguments:
    - `data`: any data structure that can be converted into a json.

    ## Returns:
    - Any python structure that can be obtained from json.

    ## Example:
    >>> from collections import OrderedDict
    >>> data = OrderedDict([("a", 1), ("b", OrderedDict([("c", 2), ("d", 3)]))])
    >>> convert_response_data_to_dict(data)
    {'a': 1, 'b': {'c': 2, 'd': 3}}
    """

    return json.loads(
        json.dumps(
            data,
            cls=DjangoJSONEncoder,
        )
    )
