""" "Structures oriented to the transmission of custom errors"""


class RecordAlreadyExists(Exception):
    pass


class FileAlreadyUsed(Exception):
    pass


class RecordNotFound(Exception):
    pass


class RecordNotValid(Exception):
    pass
