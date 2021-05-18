class NodeNotFoundException(Exception):
    def __init__(self, value):
        self.value = value


class EmptyTreeException(Exception):
    def __init__(self, value):
        self.value = value


class ZeroTreeSizeException(Exception):
    def __init__(self, value):
        self.value = value
