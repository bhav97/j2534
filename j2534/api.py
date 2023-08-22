#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .structs import PASSTHRU_MSG4, PASSTHRU_MSG5, RESOURCE_STRUCT, SDEVICE, SCHANNELSET

from ctypes import c_ulong as ulong, c_long as long, POINTER, Structure as struct, c_char as char, c_void_p as pvoid

class Version(object):
    V2='02.02' # 2002 publication, obsolete release?
    V4='04.04' # 2004 publication
    V5='05.00' # 2015 publication

V4 = Version.V4
V5 = Version.V5

# 1. PassThruOpen (4.4+)
# extern "C" long WINAPI PassThruOpen(
#   char * name
#   unsigned long *pDeviceID);
PTOPEN = ('PassThruOpen', ( POINTER(char), POINTER(ulong) ), long)

# 2. PassThruClose (4.4+)
# extern "C" long WINAPI PassThruClose(
#   unsigned long DeviceID);
PTCLOSE = ('PassThruClose', ( ulong, ), long)

# 3. PassThruConnect (4.4+)
# extern "C" long WINAPI PassThruConnect(
#   unsigned long DeviceID,
#   unsigned long ProtocolID,
#   unsigned long Flags,
#   unsigned long Baudrate,
#   unsigned long *pChannelID);
PTCONNECT4 = ('PassThruConnect', ( ulong, ulong, ulong, ulong, POINTER(ulong) ), long)

# 4. PassThruDisconnect (4.4+)
# extern "C" long WINAPI PassThruDisconnect(
#   unsigned long ChannelID);
PTDISCONNECT = ('PassThruDisconnect', ( ulong, ), long)

# 5. PassThruReadMsgs (4.4+)
# extern "C" long WINAPI PassThruReadMsgs(
#   unsigned long ChannelID,
#   PASSTHRU_MSG *pMsg,
#   unsigned long *pNumMsgs,
#   unsigned long timeout);
PTREADMSGS4 = ('PassThruReadMsgs', ( ulong, POINTER(PASSTHRU_MSG4), POINTER(ulong), ulong ), long)

# 6. PassThruWriteMsgs (4.4, deprecated in 5.0)
# extern "C" long WINAPI PassThruWriteMsgs(
#   unsigned long ChannelID,
#   PASSTHRU_MSG *pMsg,
#   unsigned long *pNumMsgs,
# unsigned long Timeout);
PTWRITEMSGS = ('PassThruWriteMsgs', ( ulong, POINTER(PASSTHRU_MSG4), POINTER(ulong), ulong ), long)

# 7. PassThruStartPeriodicMsg (4.4+)
# extern "C" long WINAPI PassThruStartPeriodicMsg(
#   unsigned long ChannelID,
#   PASSTHRU_MSG *pMsg,
#   unsigned long *pMsgID,
#   unsigned long TimeInterval);
PTSTARTPERIODICMSG4 = ('PassThruStartPeriodicMsg', ( ulong, POINTER(PASSTHRU_MSG4), POINTER(ulong), ulong ), long)

# 8. PassThruStopPeriodicMsg (4.4+)
# extern "C" long WINAPI PassThruStopPeriodicMsg(
#   unsigned long ChannelID,
#   unsigned long MsgID);
PTSTOPPERIODICMSG = ('PassThruStopPeriodicMsg', ( ulong, ulong ), long)

# 9. PassThruStartMsgFilter (4.4)
# extern "C" long WINAPI PassThruStartMsgFilter(
#   unsigned long ChannelID,
#   unsigned long FilterType,
#   const PASSTHRU_MSG *pMaskMsg,
#   const PASSTHRU_MSG *pPatternMsg,
#   const PASSTHRU_MSG *pFlowControlMsg,
#   unsigned long *pFilterID);
PTSTARTMSGFILTER4 = ('PassThruStartMsgFilter', ( ulong, ulong, POINTER(PASSTHRU_MSG4), POINTER(PASSTHRU_MSG4), POINTER(PASSTHRU_MSG4), POINTER(ulong) ), long)

# 10. PassThruStopMsgFilter (4.4+)
# extern "C" long WINAPI PassThruStopMsgFilter(
#   unsigned long ChannelID,
#   unsigned long FilterID);
PTSTOPMSGFILTER = ('PassThruStopMsgFilter', ( ulong, ulong ), long)

# 11. PassThruSetProgrammingVoltage (4.4)
# extern "C" long WINAPI PassThruSetProgrammingVoltage(
#   unsigned long DeviceID,
#   unsigned long PinNumber,
#   unsigned long Voltage);
PTSETPROGRAMMINGVOLTAGE4 = ('PassThruSetProgrammingVoltage', ( ulong, ulong, ulong ), long)

# 12. PassThruReadVersion (4.4+)
# extern "C" long WINAPI PassThruReadVersion(
#   unsigned long DeviceID,
#   char * pFirmwareVersion,
#   char *pDllVersion,
#   char *pApiVersion);
PTREADVERSION = ('PassThruReadVersion',  ( ulong, POINTER(char), POINTER(char), POINTER(char)), long)

# 13. PassThruGetLastError (4.4+)
# extern "C" long WINAPI PassThruGetLastError(
#   char * pErrorDescription);
PTGETLASTERROR = ('PassThruGetLastError', ( POINTER(char), ), long)

# 14. PassThruIoctl (4.4+)
# extern "C" long WINAPI PassThruIoctl(
#   unsigned long ChannelID,
#   unsigned long IoctlID,
#   void *pInput,
#   void *pOutput);
PTIOCTL = ('PassThruIoctl', ( ulong, ulong, pvoid, pvoid ), long)

# 15. PassThruScanForDevices (5.0+)
# extern "C" long WAPI PassThruScanForDevices(
#   unsigned long *pDeviceCount)
PTSCANFORDEVICES = ('PassThruScanForDevices', (POINTER(long), ), long)

# 16. PassThruGetNextDevice
# extern "C" long WINAPI PassThruGetNextDevice(
#   SDEVICE *psDevice)
PTGETNEXTDEVICE = ('PassThruGetNextDevice', ( POINTER(SDEVICE), ), long )

# 17. PassThruLogicalConnect (5.0+)
# extern "C" long WINAPI PassThruLogicalConnect(
#   unsigned long PhysicalChannelID,
#   unsigned long ProtocolID,
#   unsigned long Flags,
#   void * pChannelDescriptor,
#   unsigned long * pChannelID)
PTLOGICALCONNECT = ('PassThruLogicalConnect', (ulong, ulong, ulong, pvoid, POINTER(ulong)), long)

# 18.  PassThruLogicalDisconnect (5.0+)
# extern "C" long WINAPI PassThruLogicalDisconnect(
#   unsigned long ChannelID)
PTLOGICALDISCONNECT = ('PassThruLogicalDisconnect', (ulong, ), long)

# 19. PassThruSelect (5.0+)
# extern "C" long WINAPI PassThruSelect(
#   SCHANNELSET *ChannelSetPtr,
#   unsigned long SelectType,
#   unsigned long Timeout)
PTSELECT = ('PassThruSelect', ( POINTER(SCHANNELSET), ulong, ulong ), long)

# 20. PassThruConnect (5.0+)
# extern "C" long WINAPI PassThruConnect(
#   unsigned long DeviceID,
#   unsigned long ProtocolID,
#   unsigned long Flags,
#   RESOURCE_STRUCT ResourceStruct,
#   unsigned long *pChannelID);
PTCONNECT5 = ('PassThruConnect', ( ulong, ulong, ulong, RESOURCE_STRUCT, POINTER(ulong) ), long)

# 21 PassThruQueueMsgs (5.0+)
# extern "C" long WINAPI PassThruQueueMsgs(
#   unsigned long ChannelID,
#   PASSTHRU_MSG * pMsg,
#   unsigned long * pNumMsgs)
PTQUEUEMSGS = ('PassThruQueueMsgs', ( ulong, POINTER(PASSTHRU_MSG5), POINTER(ulong) ), long)

# 22. PassThruStartMsgFilter (5.0+)
# extern "C" long WINAPI PassThruStartMsgFilter(
#   unsigned long ChannelID,
#   unsigned long FilterType,
#   const PASSTHRU_MSG *pMaskMsg,
#   const PASSTHRU_MSG *pPatternMsg,
#   unsigned long *pFilterID);
PTSTARTMSGFILTER5 = ('PassThruStartMsgFilter', ( ulong, ulong, POINTER(PASSTHRU_MSG5), POINTER(PASSTHRU_MSG5), POINTER(PASSTHRU_MSG5), POINTER(ulong) ), long)

# 23. PassThruSetProgrammingVoltage (5.0)
# extern "C" long WINAPI PassThruSetProgrammingVoltage(
#   unsigned long DeviceID,
#   RESOURCE_STRUCT ResourceStruct,
#   unsigned long Voltage);
PTSETPROGRAMMINGVOLTAGE = ('PassThruSetProgrammingVoltage', ( ulong, RESOURCE_STRUCT, ulong ), long)

# 24. PassThruReadMsgs (5.0+)
# extern "C" long WINAPI PassThruReadMsgs(
#   unsigned long ChannelID,
#   PASSTHRU_MSG *pMsg,
#   unsigned long *pNumMsgs,
#   unsigned long timeout);
PTREADMSGS5 = ('PassThruReadMsgs', ( ulong, POINTER(PASSTHRU_MSG5), POINTER(ulong), ulong ), long)

# 25. PassThruStartPeriodicMsg (5.0+)
# extern "C" long WINAPI PassThruStartPeriodicMsg(
#   unsigned long ChannelID,
#   PASSTHRU_MSG *pMsg,
#   unsigned long *pMsgID,
#   unsigned long TimeInterval);
PTSTARTPERIODICMSG5 = ('PassThruStartPeriodicMsg', ( ulong, POINTER(PASSTHRU_MSG5), POINTER(ulong), ulong ), long)

PASSTHRU_DEF4 = [
    PTOPEN,
    PTCLOSE,
    PTCONNECT4,
    PTDISCONNECT,
    PTREADMSGS4,
    PTWRITEMSGS,
    PTSTARTPERIODICMSG4,
    PTSTOPPERIODICMSG,
    PTSTARTMSGFILTER4,
    PTSTOPMSGFILTER,
    PTSETPROGRAMMINGVOLTAGE4,
    PTREADVERSION,
    PTGETLASTERROR,
    PTIOCTL,
]

PASSTHRU_DEF5 = [
    PTOPEN,
    PTCLOSE,
    PTCONNECT5,
    PTDISCONNECT,
    PTLOGICALCONNECT,
    PTLOGICALDISCONNECT,
    PTREADMSGS5,
    PTQUEUEMSGS,
    PTSTARTPERIODICMSG5,
    PTSTOPPERIODICMSG,
    PTSTARTMSGFILTER5,
    PTSTOPMSGFILTER,
    PTREADVERSION,
    PTGETLASTERROR,
    PTIOCTL,
]

def get_defs_for_version(version: str) -> list:
    match version:
        case Version.V4:
            return PASSTHRU_DEF4
        case Version.V5:
            return PASSTHRU_DEF5
        case _:
            raise ValueError(f'API version {version} is not supported')

if __name__ == "__main__":
    pass