#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .errors import PassThruInterfaceException, PassThruApiNotSupportedException, PassThruApiConcurrentCallException
from .enums import ErrorCode, ProtocolId
from .vector import VectorPassThruXLLibrary
from .intrepid import IntrepidCsPassthruLibrary
from .structs import SDEVICE, PASSTHRU_MSG4, PASSTHRU_MSG5
from .filter import BlockFilter, PassFilter, FlowCtrlFilter, Filter
from .protocols import Protocol

from . import api
from . import util
from . import connection

import functools
import ctypes
import logging
import contextlib


@util.setup_logging
class PassThru(object):

    def api_required(api: str):
        """ Decorator to specify that the J2534 API is implemented in the DLL by the manufacturer

        Args:
            api (str): Name of the API Function
        """
        def _api_required(func):
            """Internal decorator that takes the argument and returns a decorator for our decorator
            
            Args:
                func: the wrapped function 
            """
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                """ Wrapper function to check if the required API is available in the DLL

                Args:
                    self (PassThru): the ``PassThru`` instance
                    args: list of arguments passed to the wrapper
                    kwargs: list of key-word arguments passed to the wrapper
                """
                if not hasattr(self.__dll, api):
                    raise PassThruApiNotSupportedException(
                        f'{api} is not supported by {self.dll}')
                return func(self, *args, **kwargs)
            return wrapper
        return _api_required

    def open_required(func):
        """ Decorator to specify that the J2534 API function is called only after ``PassThruOpen``

        Args:
            func: the wrapped function
        """
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            """ Wrapper funtion to check if the caller has opened the device

            Args:
                self (PassThru): the ``PassThru`` instance
                args: list of all arguments passed to the wrapper
                kwargs: list of key-word arguments passed to the wrapper
            """
            if self.__open_refs == 0:
                raise PassThruInterfaceException(
                    f'PassThru device must be opened before \'{func.__name__}\' call.')
            return func(self, *args, **kwargs)
        return wrapper

    def ver_required(version: str):
        def _ver_required(func):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                """
                """
                exact = not version.endswith('+')

                major = int(version.split('.')[0])
                minor = int(version.split('.')[
                            1] if exact else version.split('.')[1][:-1])
                usingmajor = int(self.apiversion.split('.')[0])
                usingminor = int(self.apiversion.split('.')[1])

                if exact and ((usingmajor != major) or (usingminor != minor)):
                    raise PassThruInterfaceException(
                        f'API call requires version {version} (using version {self.apiversion})')
                elif not exact and (usingmajor < major):
                    raise PassThruInterfaceException(
                        f'API call requires version {version} (using version {self.apiversion})')
                elif not exact and ((usingmajor == major) and (usingminor < minor)):
                    raise PassThruInterfaceException(
                        f'API call requires version {version} (using version {self.apiversion})')
                return func(self, *args, **kwargs)
            return wrapper
        return _ver_required

    def handle_dllreturn(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            rc, rv = func(self, *args, **kwargs)
            if rc != ErrorCode.Status_NoError:
                raise PassThruInterfaceException(rc)
            return rv
        return wrapper

    def __init__(self, lib: str, **kwargs):
        """
        """
        self.__log.setLevel(kwargs.get('loglevel', logging.WARN))
        self.apiversion = kwargs.get('apiversion', api.V4)
        # DLLs return weird error codes/ string when API is called without ``open``
        self.__open_refs = 0

        if lib is VectorPassThruXLLibrary:
            self.__lib = VectorPassThruXLLibrary(**kwargs)
        elif lib is IntrepidCsPassthruLibrary:
            self.__lib = IntrepidCsPassthruLibrary(**kwargs)
        else:
            raise PassThruInterfaceException(f'{lib} is not supported')

        self.__dll = self.__lib.dll

        # setup prototypes for all PassThru procedures supported by the DLL
        for proc, args, res in api.get_defs_for_version(self.apiversion):
            if hasattr(self.__dll, proc):
                self.__dll[proc].argtypes = args
                self.__dll[proc].restype = res
            self.__log.debug(
                f'{proc[8:]}: {"Available" if hasattr(self.__dll, proc) else "Not supported" }')

    @property
    def dll(self):
        return self.__lib.name

    @api_required('PassThruScanForDevices')
    @ver_required('5.0+')
    def scanfordevices(self) -> int:
        """ Generate a static list of devices accessible through this ``PassThru``

        Args:
            self (PassTHruDeviceInterface): the ``PassThru`` instance

        Returns:
            number of devices found
        """
        device_count = ctypes.c_ulong(0)
        p_device_count = ctypes.pointer(device_count)

        rv = self.__dll.PassThruScanForDevices(p_device_count)
        self.__log.debug(f'PassThruScanForDevices: {ErrorCode.to_string(rv)}')

        return rv, device_count.value

    @api_required('PassThruGetNextDevice')
    @ver_required('5.0+')
    @handle_dllreturn
    def getnextdevice(self) -> str:
        """ Return the devices found by the ``PassThru::scan_for_devices`` one at a time

        Args:
            self (passThruDeviceInterface): the ``PassThru`` instance

        Returns:
            device information string
        """
        sdevice = SDEVICE()
        p_sdevice = ctypes.pointer(sdevice)

        rv = self.__dll.PassThruGetNextDevice(p_sdevice)
        self.__log.debug(f'PassThruGetNextDevice: {ErrorCode.to_string(rv)}')

        return rv, str(sdevice)

    @api_required('PassThruOpen')
    @handle_dllreturn
    def open(self, name: str) -> int:
        """ Estabilish communications with the designated Pass-Thru device verifying that it is connected to the PC
        and initialize it.

        Args:
            self (PassThru): the ``PassThru`` instance
            name (str):

        Returns:
            the device_id which is  used as an handle for future function calls

        Raises:
            PassThruInterfaceException: if the DLL returns an error code, or the instance is not open
        """
        p_name = ctypes.create_string_buffer(name.encode('ascii'))
        device_id = ctypes.c_ulong(0)
        p_device_id = ctypes.pointer(device_id)

        rv = self.__dll.PassThruOpen(p_name, p_device_id)
        self.__log.debug(
            f'Open {name} ID: 0x{device_id.value:08x} RC<0x{rv:02x}>:{ErrorCode.to_string(rv)}')

        self.__open_refs += 1 if rv == ErrorCode.Status_NoError else 0
        return rv, device_id.value

    @api_required('PassThruClose')
    @open_required
    @handle_dllreturn
    def close(self, device_id):
        """ Close communications with the designated ``PassThru``.

        Args:
            self (PassThru): the ``PassThru`` instance
            device_id (str): the value returned by ``PassThru::open()``

        Returns:
            None

        Raises:
            PassThruInterfaceException: if the DLL returns an error code, or the instance has no device open
        """
        p_device_id = ctypes.pointer(ctypes.c_ulong(device_id))
        rv = self.__dll.PassThruClose(p_device_id)
        self.__log.debug(f'Close ID: 0x{p_device_id[0]:08x} RC<0x{rv:02x}>:{ErrorCode.to_string(rv)}')

        self.__open_refs -= 1
        return rv,

    @api_required('PassThruConnect')
    @open_required
    @handle_dllreturn
    def connect(self, device_id: int, protocol: Protocol) -> int:
        """ Establish a physical connection to the vehicle using the specified interface hardware in the designated
        Pass-Thru device.

        Args:
            self (PassThru): the ``PassThru`` instance
            device_id (int): the value returned by the ``PassThru::open()``

        Returns:
            handle to the channel for future function calls

        Raises:
            PassThruInterfaceException: if the DLL returns an error code, or no instance is open
        """
        device_id = ctypes.c_ulong(device_id)
        protocol_id = ctypes.c_ulong(protocol.id)
        flags = ctypes.c_ulong(protocol.flags)
        baudrate = ctypes.c_ulong(protocol.baudrate)
        p_channel_id = ctypes.pointer(ctypes.c_ulong(0))

        if self.apiversion == api.V5:
            assert cfg.protocol_id != ProtocolId.ISO15765, f'Use ``{__class__.__name__}.logicalconnect`` for ISO15765'
            # TODO: construct the RESOURCE_STRUCT
            # resource =
            raise NotImplementedError("APIV5 connect call")
        elif self.apiversion == api.V4:
            self.__log.debug(f'{device_id.value} {protocol_id.value} {flags.value} {baudrate.value}')
            rv = self.__dll.PassThruConnect(
                device_id, protocol_id, flags, baudrate, p_channel_id)
        else:
            raise NotImplementedError(
                f'PassThruConnect is not implemented in api.v{self.apiversion}')

        self.__log.debug(f'Connect: Channel 0x{p_channel_id[0]:08x} RC<0x{rv:02x}>:{ErrorCode.to_string(rv)}')
        return rv, p_channel_id[0]

    @api_required('PassThruDisconnect')
    @open_required
    @handle_dllreturn
    def disconnect(self, channel: int) -> None:
        """
        """
        channel = ctypes.c_ulong(channel)
        rv = self.__dll.PassThruDisconnect(channel)
        self.__log.debug(f'Disconnect: Channel 0x{channel:08x} RC[0x]')

        return rv, None

    @api_required('PassThruLogicalConnect')
    @ver_required('5.0+')
    @open_required
    def logical_connect():
        pass

    @api_required('PassThruLogicalDisconnect')
    def logical_disconnect():
        pass

    @api_required('PassThruSelect')
    def select():
        pass

    @api_required('PassThruReadMsgs')
    @open_required
    @handle_dllreturn
    def read(self, channel, msgs, timeout) -> dict:
        """ Read messages and Indications (special messages generated to report specific events) from the 
        designated channel
        """
        channel = ctypes.c_ulong(channel)
        if self.apiversion == api.V5:
            msgs = (PASSTHRU_MSG5*msgs)()
        else:
            msgs = (PASSTHRU_MSG4*msgs)()
        p_msgsread = ctypes.pointer(ctypes.c_ulong(0))
        timeout = ctypes.c_ulong(timeout)
        print(ctypes.pointer(msgs))
        rv = self.__dll.PassThruReadMsgs(channel, msgs, p_msgsread)
        return rv, None

    @api_required('PassThruWriteMsgs')
    def write(self, channel, msgs, timeout):
        pass

    @api_required('PassThruQueueMsgs')
    def queue_msgs():
        pass

    @api_required('PassThruStartPeriodicMsg')
    def start_periodic_msg():
        pass

    @api_required('PassThruStopPeriodicMsg')
    def stop_periodic_msg():
        pass

    @api_required('PassThruStartMsgFilter')
    @ver_required('4.4')
    @open_required
    @handle_dllreturn
    def set_filter(self,
                   channel: int,
                   filter: Filter) -> int:
        """ Add the specified filter to the message evaluation process for the designated physical
        communication channel

        Args:
            self (PassThru): the ``PassThru`` instance
            channel (int): the channel id returned by the ``PassThru.connect`` call
            type (int): the filter type value from ``j2534.enums.FilterType``

        Returns:
            the filter id for future calls

        Raises:
            PassTHruInterfaceException: if the DLL returns an error code or no device is open
        """
        channel = ctypes.c_ulong(channel)
        type = ctypes.c_ulong(filter.type)
        p_filter_id = ctypes.pointer(ctypes.c_ulong(0))
        mask_msg, pattern_msg, fc_msg = filter.msg4
        self.__log.debug(f'Mask:{mask_msg}')
        self.__log.debug(f'Pttn:{pattern_msg}')
        self.__log.debug(f'FCtl:{fc_msg}')
        p_mask_msg = ctypes.pointer(mask_msg)
        p_pattern_msg = ctypes.pointer(pattern_msg)
        p_fc_msg = ctypes.pointer(fc_msg)

        rv = self.__dll.PassThruStartMsgFilter(channel, type, p_mask_msg, p_pattern_msg, p_fc_msg, p_filter_id)
        self.__log.debug(f'SetFilter: ID: {p_filter_id[0]} RC<0x{rv:02x}>:{ErrorCode.to_string(rv)}')
        return rv, p_filter_id[0]

    @api_required('PassThruStartMsgFilter')
    @ver_required('5.0+')
    @open_required
    @handle_dllreturn
    def start_msg_filter(self, channel, type, mask, pattern) -> int:
        pass

    @api_required('PassThruStopMsgFilter')
    def stop_msg_filter():
        pass

    @api_required('PassThruSetProgrammingVoltage')
    def setprogrammingvoltage():
        pass

    @api_required('PassThruReadVersion')
    @open_required
    def readversion(self, device_id: int) -> tuple[str, str, str]:
        """ Return the Firmware, DLL and API version information for the designated device.

        Args:
            self (PassThru): the ``PassTheuDevice`` instance
            device_id (int): the device id

        Returns:
            A tuple containing the Firmware, DLL and API version strings

        Raises:
            PassThruInterfaceException: if the DLL returns an error code, or the instance is not open
        """
        firmware_version = ctypes.create_string_buffer(80)
        dll_version = ctypes.create_string_buffer(80)
        api_version = ctypes.create_string_buffer(80)
        device_id = ctypes.c_ulong(device_id)

        rv = self.__dll.PassThruReadVersion(
            device_id, firmware_version, dll_version, api_version)
        self.__log.debug(f'PassThruReadVersion: {ErrorCode.to_string(rv)}')

        if rv != ErrorCode.Status_NoError:
            raise PassThruInterfaceException(rv)
        return firmware_version.value.decode('ascii'), dll_version.value.decode('ascii'), api_version.value.decode('ascii')

    @api_required('PassThruGetLastError')
    def getlasterror(self) -> str:
        """ Return the text string description for an error detected during the last function call (except
        ``PassThruGetLastError``)

        Args:
            self (PassThru): the ``PassThru`` instance

        Returns:
            The error description string

        Raises:
            PassThruInterfaceException: if the DLL returns an error code
        """
        err_desc = ctypes.create_string_buffer(80)
        rv = self.__dll.PassThruGetLastError(err_desc)
        self.__log.debug(f'PassThruGetLastError: {ErrorCode.to_string(rv)}')
        if rv != ErrorCode.Status_NoError:
            raise PassThruInterfaceException(rv)
        return err_desc.value.decode('ascii')

    @api_required('PassThruIoctl')
    def ioctl():
        pass
