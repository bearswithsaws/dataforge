"""DataForge Exceptions
"""


class DFRangeException(Exception):
    """DFRangeException

    Args:
        Exception: Out of range
    """

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class DFEndianException(Exception):
    """DFEndianException

    Args:
        Exception: DFEndianException
    """

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class DFTypeException(Exception):
    """DFTypeException

    Args:
        Exception: DFTypeException
    """

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
