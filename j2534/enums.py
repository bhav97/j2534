#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Figure 95 - Return Values
class ErrorCode(object):
    Status_NoError                  = 0x00000000
    Err_NotSupported                = 0x00000001
    Err_InvalidChannelId            = 0x00000002
    Err_ProtocolIdNotSupported      = 0x00000003
    Err_NullParameter               = 0x00000004
    Err_IoctlValueNotSupported      = 0x00000005
    Err_FlagNotSupported            = 0x00000006
    Err_Failed                      = 0x00000007
    Err_DeviceNotConnected          = 0x00000008
    Err_Timeout                     = 0x00000009
    Err_InvalidMsg                  = 0x0000000A
    Err_TimeIntervalNotSupported    = 0x0000000B
    Err_ExceededLimit               = 0x0000000C
    Err_InvalidMsgId                = 0x0000000D
    Err_DeviceInUse                 = 0x0000000E
    Err_IoctlIdNotSupported         = 0x0000000F
    Err_BufferEmpty                 = 0x00000010
    Err_BufferFull                  = 0x00000011
    Err_BufferOverflow              = 0x00000012
    Err_PinNotSupported             = 0x00000013
    Err_ResourceConflict            = 0x00000014
    Err_MsgProtocolId               = 0x00000015
    Err_InvalidFilterId             = 0x00000016
    Err_MsgNotAllowed               = 0x00000017
    Err_NotUnique                   = 0x00000018
    Err_BaudrateNotSupported        = 0x00000019
    Err_InvalidDeviceId             = 0x0000001A
    Err_DeviceNotOpen               = 0x0000001B
    Err_NullRequired                = 0x0000001C
    Err_FilterTypeNotSupported      = 0x0000001D
    Err_IoctlParamIdNotSupported    = 0x0000001E
    Err_VoltageInUse                = 0x0000001F
    Err_PinInUse                    = 0x00000020
    Err_InitFailed                  = 0x00000021
    Err_OpenFailed                  = 0x00000022
    Err_BufferTooSmall              = 0x00000023
    Err_LogChanNotAllowed           = 0x00000024
    Err_SelectTypeNotSupported      = 0x00000025
    Err_ConcurrentApiCall           = 0x00000026

    @classmethod
    def to_string(cls, err):
        """
        """
        match err:
            case cls.Status_NoError:
                return 'Function call was successful.'
            case cls.Err_NotSupported:
                return 'Device does not support the API function.'
            case cls.Err_InvalidChannelId:
                return 'Invalid <ChannelID> value.'
            case cls.Err_ProtocolIdNotSupported:
                return '<ProtocolID> value is not supported'
            case cls.Err_NullParameter:
                return 'NULL pointer supplied where a valid pointer is required.'
            case cls.Err_IoctlValueNotSupported:
                return 'SCONFIG_LIST is either invalid, out of range, or not applicable for the current channel.'
            case cls.Err_FlagNotSupported:
                return '<Flags> value(s) are either invalid, unknown, or not applicable for the current channel.'
            case cls.Err_Failed:
                return 'Undefined error.'
            case cls.Err_DeviceNotConnected:
                return 'Pass-Thru Device communication error.'
            case cls.Err_Timeout:
                return 'Request could not be completed in the designated time'
            case cls.Err_InvalidMsg:
                return 'Message structure is invalid for the given <ChannelID>.'
            case cls.Err_TimeIntervalNotSupported:
                return 'Value for the <TimeInterval> is either invalid or out of range for the current channel.'
            case cls.Err_ExceededLimit:
                return 'Exceeded the allowed limits.'
            case cls.Err_InvalidMsgId:
                return 'Invalid <MsgID> value.'
            case cls.Err_DeviceInUse:
                return 'Device is currently open.'
            case cls.Err_IoctlIdNotSupported:
                return '<IoctlID> value is either invalid, unknown, or not applicable for the current channel.'
            case cls.Err_BufferEmpty:
                return 'The buffer is empty, no data available.'
            case cls.Err_BufferFull:
                return 'Buffer is full.'
            case cls.Err_BufferOverflow:
                return 'Indicates a buffer overflow occurred, data was lost.'
            case cls.Err_PinNotSupported:
                return 'Pin number and/or connector specified is either invalid or unknown.'
            case cls.Err_ResourceConflict:
                return 'Request causes a resource conflict.'
            case cls.Err_MsgProtocolId:
                return 'Protocol ID in the PASSTHRU_MSG structure does not match the Protocol ID from the original call \
                    to PassThruConnect/ PassThruLogicalConnect for the Channel ID.'
            case cls.Err_InvalidFilterId:
                return 'Invalid <FilterID> value'
            case cls.Err_MsgNotAllowed:
                return 'Attempting to queue a Segmented Message whose network address and/or <TxFlags> does not match \
                    those defined for the <RemoteAddress> or <RemoteTxFlags> during channel creation on a logical \
                        communication channel'
            case cls.Err_NotUnique:
                return 'Attempt was made to create a duplicate where one is not allowed.'
            case cls.Err_BaudrateNotSupported:
                return 'Baud rate is either invalid or unachievable for the current channel.'
            case cls.Err_InvalidDeviceId:
                return 'PassThruOpen has been successfully called, but the current Device ID is not valid.'
            case cls.Err_DeviceNotOpen:
                return 'PassThruOpen has not been successfully called.'
            case cls.Err_NullRequired:
                return 'A parameter that is required to be NULL is not set to NULL.'
            case cls.Err_FilterTypeNotSupported:
                return '<FilterType> is either invalid or unknown for the current channel.'
            case cls.Err_IoctlParamIdNotSupported:
                return 'Parameter referenced in the SCONFIG_LIST structure is not supported.'
            case cls.Err_VoltageInUse:
                return 'Programming voltage is currently being applied to another pin.'
            case cls.Err_PinInUse:
                return 'Pin number specified is currently in use (either for voltage, ground, or by another channel).'
            case cls.Err_InitFailed:
                return 'Physical vehicle bus initialization failed.'
            case cls.Err_OpenFailed:
                return 'There is an invalid name or there is a configuration issue (e.g., firmware/DLL mismatch, etc.) \
                    and the associated device could not be opened - run the device configuration application (from the \
                        Pass-Thru Interface manufacturer) to resolve'
            case cls.Err_BufferTooSmall:
                return 'The size of <DataBuffer>, as indicated by the parameter <DataBufferSize> in the PASSTHRU_MSG \
                    structure, is too small to accommodate the full message'
            case cls.Err_LogChanNotAllowed:
                return 'Logical communication channel is not allowed for the designated physical communication channel \
                    and Protocol ID combination.'
            case cls.Err_SelectTypeNotSupported:
                return '<SelectType> is either invalid or unknown.'
            case cls.Err_ConcurrentApiCall:
                return 'A J2534 API function has been called before the previous J2534 function call has completed.'
            case _:
                raise ValueError(f'Unknown error code: {err}')

class ProtocolId(object):
    """ Protocol IDs specified in Figure 27 and Section 9.6
    """
    # GM/ Chrysler CLASS2
    J1850VPW = 0x00000001
    # Ford SCP
    J1850PWM = 0x00000002
    # ISO 9141 and ISO 9141-2
    ISO9141 = 0x00000003
    # ISO14230 (Keyword Protocol 2000)
    ISO14230 = 0x00000004
    # CAN Frames (no transport layer)
    CAN = 0x00000005
    ISO15765 = 0x00000006
    J2610 = 0x00000007
    ISO15765_LOGICAL = 0x00000200

class Flags(object):
    K_LINE_ONLY = 0x000040000
    CAN_ID_BOTH = 0x000020000
    CHKSM_DISABLE = 0x00000200
    CAN_ID_29BIT = 0x00000100

class Connector(object):
    """ Connector specified in Figure 87
    """
    J1962 = 0x00000001

class SelectType(object):
    """ SelectType specified in Figure 89
    """
    READABLE_TYPE = 0x00000001

class FilterType(object):
    """ FilterType specified in Figure 90
    """
    PASS_FILTER = 0x00000001
    BLOCK_FILTER = 0x00000002
    FLOW_CONTROL_FILTER = 0x00000003

class Voltage(object):
    """ Standardized voltages specified in Figure 91
    """
    SHORT_TO_GROUND = 0xFFFFFFFE
    PIN_OFF = 0xFFFFFFFF

class IoctlId(object):
    """ IOCTL ID specified in Figure 92
    """
    GET_CONFIG = 0x00000001
    SET_CONFIG = 0x00000002
    READ_PIN_VOLTAGE = 0x00000003
    FIVE_BAUD_INIT = 0x00000004
    FAST_INIT = 0x00000005
    CLEAR_TX_QUEUE = 0x00000007
    CLEAR_RX_QUEUE = 0x00000008
    CLEAR_PERIODIC_MSGS = 0x00000009
    CLEAR_MSG_FILTERS = 0x0000000A
    CLEAR_FUNCT_MSG_LOOKUP_TABLE = 0x0000000B
    ADD_TO_FUNCT_MSG_LOOKUP_TABLE = 0x0000000C
    DELETE_FROM_FUNCT_MSG_LOOKUP_TABLE = 0x0000000D
    READ_PROG_VOLTAGE = 0x0000000E
    BUS_ON = 0x0000000F

class ConfigParams(object):
    DATA_RATE = 0x00000001
    NODE_ADDRESS = 0x00000004
    NETWORK_LINE = 0x00000005
    P1_MIN = 0x00000006
    P1_MAX = 0x00000007
    P2_MIN = 0x00000008
    P2_MAX = 0x00000009
    P3_MIN = 0x0000000A
    P3_MAX = 0x0000000B
    P4_MIN = 0x0000000C
    P4_MAX = 0x0000000D
    W1_MAX = 0x0000000E
    W2_MAX = 0x0000000F
    W3_MAX = 0x00000010
    W4_MIN = 0x00000011
    W5_MIN = 0x00000012
    TIDLE = 0x00000013
    TINIL = 0x00000014
    TWUP = 0x00000015
    PARITY = 0x00000016
    W0_MIN = 0x00000019
    T1_MAX = 0x0000001A
    T2_MIN = 0x0000001B
    T4_MAX = 0x0000001C
    T5_MIN = 0x0000001D
    ISO15765_BS = 0x0000001E
    ISO15765_STMIN = 0x0000001F
    DATA_BITS = 0x00000020
    FIVE_BAUD_MOD = 0x00000021
    BS_TX = 0x00000022
    STMIN_TX = 0x00000023
    T3_MAX = 0x00000024
    ISO15765_WAIT_LIMIT = 0x00000025
    W1_MIN = 0x00000026
    W2_MIN = 0x00000027
    W3_MIN = 0x00000028
    W4_MAX = 0x00000029
    N_BR_MIN = 0x0000002A
    ISO15765_PAD_VALUE = 0x0000002B
    N_AS_MAX = 0x0000002C
    N_AR_MAX = 0x0000002D
    N_BS_MAX = 0x0000002E
    N_CR_MAX = 0x0000002F
    N_CS_MIN = 0x00000030
    ECHO_PHYSICAL_CHANNEL_TX = 0x00000031
    # --?
    BUS_NORMAL = 0x000000000
    BUS_PLUS = 0x000000001
    BUS_MINUS = 0x000000002
    NO_PARITY = 0x000000000
    ODD_PARITY = 0x000000001
    EVEN_PARITY = 0x000000002
    DATA_BITS_8 = 0x000000000
    DATA_BITS_7 = 0x000000001
    ISO_STD_INIT = 0x000000000
    ISO_INV_KB2 = 0x000000001
    ISO_INV_ADD = 0x000000002
    ISO_9141_STD = 0x000000003
    DISABLE_ECHO = 0x000000000
    ENABLE_ECHO = 0x000000001
