#! /usr/bin/env python3
# -*- coding: utf-8 -*-

""" Errors and exceptions?
"""

from .enums import ErrorCode

class J2534Exception(Exception):
    pass

class PassThruInterfaceException(ErrorCode, Exception):
    """ PassThru Exception
    """

    def __init__(self, code: object) -> None:
        """Generates an exception and converts ``code`` to error message if integer, otherwise assumes
        it is the message.

        Args:
            self (PassThruInterfaceException): the ``PassThruInterfaceException`` instance
            code (object): message or error code

        Returns:
            ``None``
        """
        message = code
        self.code = None

        if isinstance(code, int):
            message = self.to_string(code)
            self.code = code

        super(PassThruInterfaceException, self).__init__(message)
        self.message = message

class PassThruApiNotSupportedException(Exception):
    pass

class PassThruApiConcurrentCallException(Exception):
    pass

class PassThruLibraryException(Exception):
    pass