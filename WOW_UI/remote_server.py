import sys
import socket
import datetime
from remote_context import *
from remote_data_convert import *
from remote_server_handler import *

ui_signal = None

def setUiSignal(signal) :
    global ui_signal
    ui_signal = signal


def pythonServer(ui):
    global sock, ui_signal

    print("Python Server Starts")

    while True:
        rcvData, cppAddr = sock.recvfrom(BUF_SIZE)

        print("rcv: ", rcvData)
        ui_signal.emit(rcvData)

        # if rcvData[0] == SET_CTRL_ADDR_RET:
        #     set_CtrlAddrRet_Handler(ui, rcvData)
        #
        # elif rcvData[0] == GET_GROUP_INFO_RET:
        #     get_GroupInfoRet_Handler(ui, rcvData)
        #     a = 1
        #
        # elif rcvData[0] == GET_GROUP_VOLUME_RET:
        #     get_GroupVolumeRet_Handler(ui, rcvData)
        #
        # elif rcvData[0] == GET_WIRELESS_INFO_RET:
        #     get_WirelessInfoRet_Handler(ui,rcvData)
        #
        # elif rcvData[0] == SET_GROUP_INFO_RSP:
        #     set_GroupInfoRsp_Handler(ui, rcvData)
        #     a = 1
        #
        # elif rcvData[0] == GROUP_ACTIVATE_RSP:
        #     groupActivateRsp_Handler(ui, rcvData)
        #     a=1;
        #
        # elif rcvData[0] == GROUP_DEACTIVATE_RSP:
        #     groupDeactivateRsp_Handler(ui, rcvData)
        #
        # elif rcvData[0] == GROUP_PLAY_RSP:
        #     groupPlayRsp_Handler(ui, rcvData)
        #
        # elif rcvData[0] == SET_GROUP_ABS_VOLUME_RSP:
        #     set_GroupAbsVolumeRsp_Handler(ui, rcvData)
        #
        # elif rcvData[0] == SET_GROUP_REL_VOLUME_RSP:
        #     set_GroupRelVolumeRsp_Handler(ui, rcvData)
        #
        # elif rcvData[0] == SET_GROUP_MUTE_RSP:
        #     set_GroupMuteRsp_Handler(ui, rcvData)
        #
        # elif rcvData[0] == VOLUME_CHANGE_IND:
        #     volumeChangeInd_Handler(ui, rcvData)
        #
        # elif rcvData[0] == GROUP_PLAY_IND:
        #     groupPlayInd_Handler(ui, rcvData)
        #
        # elif rcvData[0] == GROUP_STATUS_IND:
        #     groupStatusInd_Handler(ui, rcvData)
        #
        # elif rcvData[0] == AUDIO_PLAYBACK_INFO_IND:
        #     audioPlaybackInfoInd_Handler(ui,rcvData)
        #
        # elif rcvData[0] == WIFI_CHANNEL_INFO_IND:
        #     wifiChannelInfoInd_Handler(ui,rcvData)
        #
        # a = 1