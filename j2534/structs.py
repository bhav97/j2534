#! /usr/bin/env python3
# -*- coding:utf-8 -*-

""" Defines structures from the SAE J2534 for the C API.

Defines structures for both API V4 and V5.
"""

from ctypes import c_ulong as ulong, c_long as long, POINTER, Structure as struct, c_char as char, c_void_p as pvoid
from ctypes import c_uint8 as uint8

# Common
class SCONFIG(struct):
    _fields_ = [
        ('Parameter', ulong),
        ('Value', ulong),
    ]


class SCONFIG_LIST(struct):
    _fields_ = [
        ('NumOfParams', ulong),
        ('ConfigPtr', POINTER(SCONFIG)),
    ]

class SBYTE_ARRAY(struct):
    _fields_ = [
        ('NumOfBytes', ulong),
        ('BytePtr', POINTER(char))
    ]

# 5.0
class SDEVICE(struct):
    _fields_ = [
        ('DeviceName', char * 80),
        ('DeviceAvailable', ulong),
        ('DeviceDLLFWStatus', ulong),
        ('DeviceConnectedMedia', ulong),
        ('DeviceConnectSpeed', ulong),
        ('DeviceSignalQuality', ulong),
        ('DeviceSignalStrength', ulong),
    ]

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f'\
            DeviceName: {self.DeviceName}\
            DeviceAvailable: {self.DeviceAvailable}\
            DeviceDLLFWStatus: {self.DeviceDLLFWStatus}\
            DeviceConnectedMedia: {self.DeviceConnectedMedia}\
            DeviceSignalQuality: {self.DeviceSignalQuality}\
            DeviceSignalStrength: {self.DeviceSignalStrength}'


class RESOURCE_STRUCT(struct):
    _fields_ = [
        ('Connector', ulong),
        ('NumOfResources', ulong),
        ('ResourceListPtr', POINTER(ulong)),
    ]

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f'bleh'

    @property
    def value(self):
        return self._fields_[0][1].value, self._fields_[1][1].value, self._fields_[2][1].value


class ISO15765_CHANNEL_DESCRIPTOR(struct):
    _fields_ = [
        ('LocalTxFlags', ulong),
        ('RemoteTxFlags', ulong),
        ('LocalAddress', char * 5),
        ('RemoteAddress', char * 5)
    ]

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f'bleh'

    @property
    def value(self):
        return self._fields_[0][1].value, self._fields_[1][1].value, self._fields_[2][1].value, self._fields_[3][1].value


class SCHANNELSET(struct):
    _fields_ = [
        ('ChannelCount', ulong),
        ('ChannelThreshold', ulong),
        ('ChannelList', POINTER(ulong))
    ]

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f'bleh'

    @property
    def value(self):
        return self._fields_[0][1].value, self._fields_[1][1].value, self._fields_[2][1].value

class PASSTHRU_MSG5(struct):
    """ Messages are passed between the application and the Pass-Thru Interface via the PASSTHRU_MSG structure.
    This structure is protocol independent, but the exact content and limitations of some fields is not.

    Fields:
        ProtocolID: 
        MessageHandle:
    """
    _fields_ = [
        ('ProtocolID', ulong),
        ('MessageHandle', ulong),
        ('RxStatus', ulong),
        ('TxFlags', ulong),
        ('Timestamp', ulong),
        ('DataLength', ulong),
        ('ExtraDataIndex', ulong),
        ('DataBuffer', POINTER(char)),
        ('DataBufferSize', ulong)
    ]


# 04.04
class PASSTHRU_MSG4(struct):
    """ Messages are passed between the application and the Pass-Thru Interface via the PASSTHRU_MSG structure.
    This structure is protocol independent, but the exact content and limitations of some fields is not.
    """
    _fields_ = [
        ('ProtocolID', ulong),
        ('RxStatus', ulong),
        ('TxFlags', ulong),
        ('Timestamp', ulong),
        ('DataSize', ulong),
        ('ExtraDataIndex', ulong),
        ('Data',  uint8* 4128),
    ]

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f' Protocol: {self.ProtocolID}'\
               f' RxStatus: {self.RxStatus}'\
               f' TxFlags: {self.TxFlags}'\
               f' Timestamp: {self.Timestamp}'\
               f' DataSize: {self.DataSize}'\
               f' ExtraDataIndex: {self.ExtraDataIndex}'\
               f' Data: {bytes(list(self.Data)[:self.DataSize])}'


class PASSTHRU_HDR(struct):
    _fields_ = [
        ('ProtocolID', ulong),
        ('RxStatus', ulong),
        ('TxFlags', ulong),
        ('Timestamp', ulong),
        ('DataSize', ulong),
        ('ExtraDataIndex', ulong),
    ]

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f'{self.ProtocolID}:{self.RxStatus}:{self.TxFlags}:{self.Timestamp}:{self.DataSize}:{self.ExtraDataIndex}'
