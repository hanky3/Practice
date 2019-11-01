import sys
import socket
import datetime
from remote_context import *
from remote_data_convert import *

def sock_init():
    global sock
    sock.bind((socket.gethostbyname(socket.gethostname()), PYTHON_PORT))

def send_SetControllerAddr(ui, addr):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += " Address of Remote Controller is "
    log += addr
    ui.log_TextBrowser.append(log)

    sendData = bytes(SET_CTRL_ADDR.to_bytes(1, 'little'))
    sendData += addr.encode()
    sendData += 0x00.to_bytes(1, 'little')
    sock.sendto(sendData, (CPP_ADDR, CPP_PORT))

def send_GetGroupInfo(ui):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += " Sends Get Group Info Request "
    ui.log_TextBrowser.append(log)

    sendData = bytes(GET_GROUP_INFO.to_bytes(1, 'little'))
    sock.sendto(sendData, (CPP_ADDR, CPP_PORT))

def send_SetGroupInfo(ui, groupInfo):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += " Sends Set Group Info Request "
    ui.log_TextBrowser.append(log)

    sendData = bytes(SET_GROUP_INFO_REQ.to_bytes(1, 'little'))
    sendData += groupInfo
    sock.sendto(sendData, (CPP_ADDR, CPP_PORT))

def send_ActivateInfo(ui, activateInfo):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += " Sends Group Activaion Request "
    ui.log_TextBrowser.append(log)

    sendData = bytes(GROUP_ACTIVATE_REQ.to_bytes(1, 'little'))
    sendData += activateInfo
    sock.sendto(sendData, (CPP_ADDR, CPP_PORT))

def send_DeactivateInfo(ui, currentTime):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += " Sends Group Deactivaion Request "
    ui.log_TextBrowser.append(log)

    sendData = bytes(GROUP_DEACTIVATE_REQ.to_bytes(1, 'little'))
    sendData += currentTime.to_bytes(8, 'little')
    sock.sendto(sendData, (CPP_ADDR, CPP_PORT))

def send_Play(ui, bPlay):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    if bPlay == 0:
        log += " Sends Group Pause Request "
    else:
        log += " Sends Group Play Request "
    ui.log_TextBrowser.append(log)

    sendData = bytes(GROUP_PLAY_REQ.to_bytes(1, 'little'))
    sendData += bPlay.to_bytes(1, 'little')
    sock.sendto(sendData, (CPP_ADDR, CPP_PORT))

def send_Mute(ui, bMute):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    if bMute == 0:
        log += " Sends Group Mute Request "
    else:
        log += " Sends Group Unmute Request "
    ui.log_TextBrowser.append(log)

    sendData = bytes(SET_GROUP_MUTE_REQ.to_bytes(1, 'little'))
    sendData += bMute.to_bytes(1, 'little')
    sock.sendto(sendData, (CPP_ADDR, CPP_PORT))

def send_GetGroupVolumeInfo(ui):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += " Sends Get Group Volume Info Request "
    ui.log_TextBrowser.append(log)

    sendData = bytes(GET_GROUP_VOLUME.to_bytes(1, 'little'))
    sock.sendto(sendData, (CPP_ADDR, CPP_PORT))

def send_SetAbsVolumeReq(ui, deviceIdx, volume):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += " Sends Set Abs Volume Request "
    ui.log_TextBrowser.append(log)

    sendData = bytes(SET_GROUP_ABS_VOLUME_REQ.to_bytes(1, 'little'))
    sendData += deviceIdx.to_bytes(1, 'little')
    sendData += volume.to_bytes(1, 'little')
    sock.sendto(sendData, (CPP_ADDR, CPP_PORT))

def send_SetRelVolumeReq(ui, deviceIdx, upDown):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")

    if upDown == 0:
        log += " Sends Set Rel Volume (Up) Request "
    else:
        log += " Sends Set Rel Volume (Down) Request "
    ui.log_TextBrowser.append(log)

    sendData = bytes(SET_GROUP_REL_VOLUME_REQ.to_bytes(1, 'little'))
    sendData += deviceIdx.to_bytes(1, 'little')
    sendData += upDown.to_bytes(1, 'little')
    sock.sendto(sendData, (CPP_ADDR, CPP_PORT))

def send_GetWirelessInfo(ui):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += " Sends Get Wireless Info"
    sendData = bytes(GET_WIRELESS_INFO.to_bytes(1,'little'))
    sock.sendto(sendData,(CPP_ADDR,CPP_PORT))