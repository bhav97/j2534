#! /usr/bin/env python3
# -*- coding: utf-8 -*-

""" Utility functions and decorators for registry lookups and class setups

Available Functions:
    find_installed_dlls: get DLL from vendor string
    get_dll_path: get path of the DLL from the registry key

Available Decorators:
    setup_logging: add ``__log`` to the decorated class
    set_supported_baudrates: add ``__rates`` to the decorated class
    set_supported_pins: add ``__pins`` to the decorated class
"""

import winreg
import logging

def find_installed_dlls(api_version: str, vendor: str) -> str:
    """ Returns all the installed J2534 DLLs from a specific vendor of a specific API version.
    An empty string will return results from all vendors.

    Args:
        api_version (str): Valid J2534 API API version string
        vendor (str): DLL vendor; entries are usually named VENDORxx...

    Returns:
        the first available installation under the input ``api_version``

    Raises:
        OsError: if registry lookup fails
    """
    hkey = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE')
    hkey = winreg.OpenKeyEx(hkey, f'PassThruSupport.{api_version}')
    available = [winreg.EnumKey(hkey, x) for x in range(0, winreg.QueryInfoKey(hkey)[0])]
    return list(filter(lambda x: x.lower().startswith(vendor.lower()), available))[0]

def get_dll_path(api_version: str, key: str) -> str:
    """ Returns path to the DLL matching the key implementing the api_version

    Args:
        api_version (str): Valid J2534 API version string
        key (str): Registry key to query the DLL path

    Returns:
        path to the DLL

    Raises:
        OsError: if registry lookup fails
    """
    hkey = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE')
    hkey = winreg.OpenKeyEx(hkey, f'PassThruSupport.{api_version}\\{key}')
    return winreg.QueryValueEx(hkey, 'FunctionLibrary')[0]

def setup_logging(cls: type):
    """ Decorator to setup logging for a class

    Args:
        cls (type): the class type
    """
    setattr(cls, f'_{cls.__name__}__log', logging.getLogger(cls.__name__))
    return cls

def set_supported_baudrates(*args):
    """ Decorator to add supported baudrates a class. """
    def _set_supported_baudrates(cls: type):
        """ Add a ``__rates`` attribute to the class

        Args:
            cls: the class type
        """
        setattr(cls, f'_{cls.__name__}__rates', list(args))
        return cls
    return _set_supported_baudrates

def set_supported_pins(*args):
    """ Decorator to add supported pins to class. """
    def _set_supported_pins(cls: type):
        """ Add a ``__pins`` attribute to the class

        Args:
            cls: the class type
        """
        setattr(cls, f'_{cls.__name__}__pins', list(args))
        return cls
    return _set_supported_pins
