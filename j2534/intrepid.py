#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import ctypes
import logging
import winreg

from . import util
from . import api

class IntrepidCsPassthruLibrary(object):
    """Wrapper to load the Intrepid J2534 DLL

    The :load: and :unload: methods shall be automatically called when an
    instance is created or destroyed. 

    This class automatically searches for a PassThru DLL registered in the
    Windows registry unless a dll path is passed as kwargs.

    Attributes:
        dll: A ``ctypes.DLL`` for invoking exported functions
        name: The name ``str`` of the loaded DLL
    """

    OBD2PRO = 'neoOBD2Pro'
    FIRERED = 'neoVI Fire/Red'
    FIRE2 = 'neoVI Fire2'
    PLASMAION = 'neoVI Plasma/ION'
    PLASMAVNET8 = 'neoVI Plasma-VNET8'
    RADMARS = 'neoVI RAD-Mars'
    RED2 = 'neoVI Red2'
    RADA2B = 'RAD-A2B'
    RADGALAXY = 'RAD-Galaxy'
    RADGIGASTAR = 'RAD-Gigastar'
    RADJUPITER = 'RAD-Jupiter'
    RADPLUTO = 'RAD-Pluto'
    RADSTAR2 = 'RADStar2'
    VALUECAN3 = 'ValueCAN3'
    VALUECAN41 = 'ValueCAN41'
    VALUECAN42 = 'ValueCAN42'
    VALUECAN42EL = 'ValueCAN42EL'
    VALUECAN44 = 'ValueCAN44'

    def __init__(self, **kwargs):
        """ Create instance and load the DLL. 

        Keyword Args:
            hardware (str): Intrepid hardware
            loglevel (int): logging level for the logger instance
            apiversion (str): version of the PassThru API
            dll (str): path to the DLL
        """
        hw = kwargs.get('hardware', IntrepidCsPassthruLibrary.FIRERED)
        api = kwargs.get('apiversion', api.V4)
        dll = kwargs.get('dll', None)
        self.__dll = None
        self.__log.setLevel(kwargs.get('loglevel', logging.WARN))
        self.__load(hw, api, dll)

    def __load(self, name: str, version: str, path: str = None):
        """ Load the J2534 PassThru DLL.

        Args:
            name: Intrepid hardware
            version: the API version
            path: path to a DLL (to skip searching the registry)
        """
        self.path = path

        if self.path is None:
            self.__log.info(f'Looking for installed DLLs with API version={version}')
            key = util.find_installed_dlls(version, name)
            self.path = util.get_dll_path(version, key)

        self.__log.info(f'Load: {self.path}')
        self.__dll = ctypes.cdll.LoadLibrary(self.path)

    def __unload(self):
        """ Free the J2534 PassThru DLL. """
        if self.__dll is not None:
            self.__log.info(f'FreeLibrary: {self._path}')
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