class FileEmpty(Exception):
    pass

class PathEmpty(Exception):
    def __init__(self, message):
        super().__init__(message)