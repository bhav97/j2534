#! /usr/bin/env pythno3
# -*- coding: utf-8 -*-

from .structs import PASSTHRU_MSG4
from .structs import PASSTHRU_MSG5
from .enums import FilterType, ProtocolId
from .api import V4, V5

import abc
import ctypes

class Filter(abc.ABC):
    """ Abstract base class for creating filters for the PassThru messages
    """

    @abc.abstractmethod
    def __init__(self) -> None:
        """
        """
        pass

    @property
    def msg4(self) -> tuple[PASSTHRU_MSG4, PASSTHRU_MSG4, PASSTHRU_MSG4]:
        mask = PASSTHRU_MSG4()
        mask.ProtocolID = ProtocolId.ISO15765
        mask.RxStatus       = ctypes.c_ulong(self.rxstat)
        mask.TxFlags        = ctypes.c_ulong(self.txflags)
        mask.DataSize       = ctypes.c_ulong(self.size)
        mask.ExtraDataIndex = ctypes.c_ulong(self.size)
        ctypes.memmove(mask.Data, ctypes.byref(self.mask), self.size)

        patt = PASSTHRU_MSG4()
        patt.ProtocolID = ProtocolId.ISO15765
        patt.RxStatus = ctypes.c_ulong(self.rxstat)
        patt.TxFlags = ctypes.c_ulong(self.txflags)
        patt.DataSize = ctypes.c_ulong(self.size)
        patt.ExtraDataIndex = ctypes.c_ulong(self.size)
        ctypes.memmove(patt.Data, ctypes.byref(self.patt), self.size)

        flow = PASSTHRU_MSG4()
        flow.ProtocolID = ProtocolId.ISO15765
        flow.RxStatus = ctypes.c_ulong(self.rxstat)
        flow.TxFlags = ctypes.c_ulong(self.txflags)
        flow.DataSize = ctypes.c_ulong(self.size)
        flow.ExtraDataIndex = ctypes.c_ulong(self.size)
        ctypes.memmove(flow.Data, ctypes.byref(self.flow), self.size)

        return mask, patt, flow

    @property
    def type(self):
        if isinstance(self, FlowCtrlFilter):
            return FilterType.FLOW_CONTROL_FILTER
        elif isinstance(self, PassFilter):
            return FilterType.PASS_FILTER
        elif isinstance(self, BlockFilter):
            return FilterType.BLOCK_FILTER
        else:
            raise ValueError(f'Unknown Filter: {self}')

    @property
    def msg5(cls):
        raise NotImplementedError("Filter API v5 is not implemented.")

class BlockFilter(Filter):
    """ ``BlockFilter`` keeps the matching messages out of the receive queue.
    This filter type is only valid for non-logical channels
    """

    def __init__(self, protocol: int, mask: int, pattern: int):
        """
        """
        raise NotImplementedError('Block Filters are not implemented')

class PassFilter(Filter):
    """ ``PassFilter`` allows the matching messages into the receiving queue.
    This filter type is only valid for non-logical channels
    """

    def __init__(self) -> None:
        """
        """
        raise NotImplementedError('Pass Filters are not implemented')

class FlowCtrlFilter(Filter):
    """
    """

    def __init__(self, **kwargs) -> None:
        """
        """
        apiversion = kwargs.get('apiversion', V4)
        if apiversion is V4:
            self.__v4_init(**kwargs)
        elif apiversion is V5:
            self.__v5_init()
        else:
            raise NotImplementedError(f'API version: {apiversion} is not supported')

    def __v5_init(self):
        raise NotImplementedError()

    def __v4_init(self, **kwargs):
        self.size = kwargs.get('size', 4)
        self.rxstat = kwargs.get('rxstat', 0)
        self.txflags = kwargs.get('txflags', 0)
        try:
            self.patt = (ctypes.c_uint8*self.size).from_buffer_copy(kwargs['pattern'].to_bytes(self.size, 'big'))
            self.mask = (ctypes.c_uint8*self.size).from_buffer_copy(kwargs['mask'].to_bytes(self.size, 'big'))
            self.flow = (ctypes.c_uint8*self.size).from_buffer_copy(kwargs['flow'].to_bytes(self.size, 'big'))
        except KeyError as e:
            raise AttributeError(f'{__class__.__name__} requires pattern, mask and flow') from e


