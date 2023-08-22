#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import j2534
from j2534.interface import PassThru
from j2534.connection import Configuration as ConnCfg
from j2534.connection import  Message
from j2534.protocols import Protocol
from j2534.filter import FlowCtrlFilter
from j2534 import VectorPassThruXLLibrary

import logging

class Uds4Example:
    """ J2534 Appendix A: General ISO 15765-2 Flow Control Example

    Overview:
        ISO 15765-2 was designed to send blocks of up to 4095 bytes on top of the limited 8-byte payload of raw CAN
        frames.

        If the data is small enough, it can fit in a single frame and be transmitted like a raw CAN 
message with additional headers. 
        For flexibility, the receiver of the segments can control the rate at which the segments are sent.
    """
    def __init__(self) -> None:
        """ Example class initialization
        """
        self.pt = PassThru(lib=VectorPassThruXLLibrary, apiversion=j2534.APIV4, loglevel=logging.DEBUG)
        self.cfg = ConnCfg(Protocol.ISO15765(500000, Protocol.CAN.STANDARD_AND_EXTENDED_ID))
        fcfilter = FlowCtrlFilter(pattern=0x000000ED, mask=0xFFFFFFFF, flow=0x000000F1)
        # No message shall be queued for reception without matching a FLOW_CTRL filter
        self.device = self.pt.open('J2534-1:ExampleUdsDev')
        self.channel = self.pt.connect(self.device, self.cfg)
        self.pt.set_filter(self.channel, fcfilter)
        self.pt.read(self.channel, 3, 0)

    def setup_conversation(self) -> None:
        pass

    def send_uds_message(self) -> None:
        pass

    def __def__(self) -> None:
        self.pt.disconnect(self.channel)
        self.pt.close(self.device)

if __name__ == "__main__":
    logging.basicConfig()

    ex = Uds4Example()
    ex.send_uds_message()
