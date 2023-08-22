#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import ctypes
import logging

from . import util
from . import api

@util.setup_logging
class VectorPassThruXLLibrary(object):
    """Wrapper to to load/unload the Vector PassThruXL Library DLL
    
    The :load: and :unload: methods shall be automatically called when an
    instance is created or destroyed.

    The class automatically searches for a PassThru DLL registered in the 
    Windows registry unless a dll path is passed as kwargs.

    Attributes:
        dll: A ``ctypes.DLL`` for invoking exported functions
        name: The name ``str`` of the loaded DLL
    """

    VENDOR = 'Vector'

    def __init__(self, **kwargs):
        """ Create instance and load the DLL. 

        Keyword Args:
            loglevel (int): logging level for the logger instance
            apiversion (str): version of the PassThru API
            dll (str): path to the DLL
        """
        api = kwargs.get('apiversion', api.V4)
        dll = kwargs.get('dll', None)
        self.__dll = None
        self.__log.setLevel(kwargs.get('loglevel', logging.WARN))
        self.__load(api, dll)

    def __load(self, version: str, path: str = None):
        """ Load the J2534 PassThru DLL.

        Args:
            version: the API version
            path (optional): path to a DLL (to skip searching the registry)
        """
        self.path = path

        if self.path is None:
            self.__log.info(f'Looking for installed DLLs with API version={version}')
            key = util.find_installed_dlls(version, self.VENDOR)
            self.path = util.get_dll_path(version, key)

        self.__log.info(f'Load: {self.path}')
        self.__dll = ctypes.cdll.LoadLibrary(self.path)

    def __unload(self):
        """ Free the J2534 PassThru DLL. """
        if self.__dll is not None:
            self.__log.info(f'FreeLibrary: {self.path}')
            ctypes.windll.kernel32.FreeLibrary.argtypes = (ctypes.c_void_p, )
            ctypes.windll.kernel32.FreeLibrary(self.__dll._handle)
            self.__dll = None

    @property
    def dll(self) -> ctypes.CDLL | None:
        """ Returns the loaded DLL which can be used to call the exported functions

        Returns:
            ``None`` if the DLL was not loaded successfully or unloaded already
            ``ctypes.DLL`` otherwise
        """
        return self.__dll

    @property
    def name(self) -> str:
        """ Returns the name of the DLL loaded. """
        return self.path.split('\\')[-1]

    def __del__(self):
        """ Unload the DLL when the class instance is destroyed. """
        self.__unload()
