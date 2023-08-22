#! /usr/bin/env python3
# -*- coding: utf-8 -*-

""" Defines :Protocol: to be used for a PassThru connection
"""

from .enums import ProtocolId, Flags
from .util import set_supported_baudrates, set_supported_pins

import abc

class __Protocol(abc.ABC):
    """ Base class for extending into Protocols.
    
    Attributes:
        id: protocol id
        flags: connection flags for the protocol
        baudrate: baudrate for the protocol
        pins: connection pins to use for protocol
    """

    @abc.abstractmethod
    def __init__(self, id: int, flags: int, rate: int, pins: list[int] = None) -> None:
        """ Save ID and Flags, perform validation on pins and flags
        """
        self.__id = id
        self.__flags = flags
        self.__rate = rate
        self.__pins = pins

    @property
    def id(self):
        return self.__id

    @property
    def flags(self):
        return self.__flags

    @property
    def baudrate(self):
        supported_rates = getattr(self, f'_{self.__class__.__name__}__rates', [])
        if self.__rate not in supported_rates:
            raise ValueError(f'{self.__class__.__name__}: Baudrate {self.__rate} not supported. ({supported_rates})')
        return self.__rate

    @property
    def pins(self):
        supported_pins = getattr(self, f'_{self.__class__.__name__}__pins', [])
        if self.__pins and (self.__pins not in supported_pins):
            raise ValueError(f'{self.__class__.__name__}: Pin(s) {self.__pins} not supported. ({supported_pins})')
        return self.__pins


@set_supported_baudrates(10400, 41600)
@set_supported_pins(2)
class J1850VPW(__Protocol):
    def __init__(self, rate: int) -> None:
        super().__init__(ProtocolId.J1850VPW, 0, rate)


@set_supported_baudrates(10400)
@set_supported_pins(2, 10)
class J1850PWM(__Protocol):
    def __init__(self, rate: int) -> None:
        super().__init__(ProtocolId.J1850PWM, 0, rate)


@set_supported_baudrates(4800, 9600, 9615, 9800, 10000, 10400, 10870, 11905, 12500, 13158, 13889, 14706, 15625, 19200, 115200)
@set_supported_pins([7, 15], [7])
class ISO9141(__Protocol):
    def __init__(self, rate: int, pins: list[int], checksum=False) -> None:
        flags = 0
        if len(pins) != 1:
            flags |= Flags.K_LINE_ONLY
        if not checksum:
            flags |= Flags.CHKSM_DISABLE
        super().__init__(ProtocolId.ISO9141, flags, rate, pins)


@set_supported_baudrates(4800, 9600, 9615, 9800, 10000, 10400, 10870, 11905, 12500, 13158, 13889, 14706, 15625, 19200, 115200)
@set_supported_pins([7, 15], [7])
class ISO14230(__Protocol):
    def __init__(self, rate: int, pins: list[int], checksum=False) -> None:
        flags = 0
        if len(pins) != 1:
            flags |= Flags.K_LINE_ONLY
        if not checksum:
            flags |= Flags.CHKSM_DISABLE
        super().__init__(ProtocolId.ISO14230, flags, rate, pins)


@set_supported_baudrates(125000, 250000, 500000)
@set_supported_pins([6, 14])
class CAN(__Protocol):
    STANDARD_ID = 0
    EXTENDED_ID = 1
    STANDARD_AND_EXTENDED_ID = 2

    def __init__(self, rate: int) -> None:
        match flags:
            case CAN.STANDARD_AND_EXTENDED_ID:
                flags = Flags.CAN_ID_BOTH
            case CAN.STANDARD_ID:
                flags = 0
            case CAN.EXTENDED_ID:
                flags = Flags.CAN_ID_29BIT
            case _:
                raise ValueError(f'Unknown flags value {flags}')
        super().__init__(ProtocolId.CAN, flags, rate)


@set_supported_baudrates(125000, 250000, 500000)
@set_supported_pins([6, 14])
class ISO15765(__Protocol):
    def __init__(self, rate: int, flags: int) -> None:
        match flags:
            case CAN.STANDARD_AND_EXTENDED_ID:
                f = Flags.CAN_ID_BOTH
            case CAN.STANDARD_ID:
                f = 0
            case CAN.EXTENDED_ID:
                f = Flags.CAN_ID_29BIT
            case _:
                raise ValueError(f'Unknown flags value {flags}')
        super().__init__(ProtocolId.ISO15765, f, rate)


@set_supported_baudrates(7812, 62500)
@set_supported_pins([14, 7], [7, 12], [15, 9])
class J2610(__Protocol):
    def __init__(self, rate: int, pins: list[int]) -> None:
        super().__init__(ProtocolId.J2610, rate, pins)


class Protocol:
    """ Enumeration of all possible Protocol / Pin Usage specified in 7.3.5.8
    """
    J1850VPW = J1850VPW
    J1850PWM = J1850PWM
    ISO9141 = ISO9141
    CAN = CAN
    ISO15765 = ISO15765
    J2610 = J2610
