#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .enums import Connector
from .structs import PASSTHRU_MSG4, PASSTHRU_MSG5
from .protocols import __Protocol as Protocol

import dataclasses


@dataclasses.dataclass
class Message(object):
    protocol: int
    status: int
    flags: int
    timestamp: int
    data: list[bytes]
    extra: list[bytes]

    @staticmethod
    def from_ptmsg(msg: PASSTHRU_MSG5 | PASSTHRU_MSG4) -> 'Message':
        if isinstance(msg, PASSTHRU_MSG4):
            return Message(msg.ProtocolID)
        elif isinstance(msg, PASSTHRU_MSG5):
            pass
        else:
            raise TypeError(
                f'{msg} must be {PASSTHRU_MSG5} or {PASSTHRU_MSG4}')
        return Message(0, 0, 0, 0, 0, 0)


@dataclasses.dataclass
class Configuration:
    """ Connection configuration for calling ``interface.PassThru.connect``

    Fields:
        ProtocolId: appropriate value from ``.connection.Protocol``
        Flags: appropriate value from ``.connection.Flags``
        BaudRate: appropriate value from ``.connection.BaudRate``

    Note:
        Attempting an interface connection with any other values will raise an Error
    """
    protocol: Protocol

    def __post_init__(self):
        if not isinstance(self.protocol, Protocol):
            raise TypeError(f'Unsupported protocol value.')

    @property
    def protocol_id(self):
        """ Get protocol_id from the ``self.protocol``

        Args:
            self (Connection): the ``Connnection`` instance

        Returns:
            the protocol id
        """
        return self.protocol.id

    @property
    def flags(self):
        """ Get flags from the ``self.protocol``

        Args:
            self (Connection): the ``Connnection`` instance

        Returns:
            the protocol flags
        """
        return self.protocol.flags

    @property
    def baudrate(self):
        """ Get baudrate of the associated protocol

        Args:
            self (Connection): the ``Connection`` instance

        Returns:
            the protocol baudrate
        """
        return self.protocol.baudrate

    @property
    def id(self):
        """ Get id of the associated protocol

        Args:
            self (Connection): the ``Connection`` instance

        Returns:
            the protocol id
        """
        return self.protocol.id

    @property
    def connector(self) -> int:
        """ Returns ConnectorType as J1962 (only one connector support by spec)

        Args:
            self (Configuration): the ``Configuration`` instance

        Returns:
            always ``enums.Connector.J1962``
        """
        return Connector.J1962

    @property
    def pins(self) -> list[int] | int | None:
        """ Get Pins from the ``self.protocol``

        Args:
            self (Connection): the ``Connnection`` instance

        Returns:
            a list of pins to use
        """
        return self.protocol.pins
