# define Python user-defined exceptions

class Error(Exception):
    pass

class ValueIsNotPresent(Error):
    """ Raise error if the value field is NAN in the table of Yahoo Finance """
    pass