# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'remote_controller.ui'
#
# Created: Fri Sep  6 09:11:37 2019
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!Py
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import time

import threading
import json
import datetime
from remote_context import *
from remote_data_convert import *
from remote_server import *
from remote_client import *
from remote_event_handler import *
from state_main import *


class Ui_MainWindow(QObject):
    receive_signal = pyqtSignal(bytes)

    @pyqtSlot(bytes)
    def onReceive(self, rcvData:bytes):
        if rcvData[0] == SET_CTRL_ADDR_RET:
            set_CtrlAddrRet_Handler(self, rcvData)

        elif rcvData[0] == GET_GROUP_INFO_RET:
            get_GroupInfoRet_Handler(self, rcvData)
            a = 1

        elif rcvData[0] == GET_GROUP_VOLUME_RET:
            get_GroupVolumeRet_Handler(self, rcvData)
            a = 1

        elif rcvData[0] == GET_WIRELESS_INFO_RET:
            get_WirelessInfoRet_Handler(self, rcvData)

        elif rcvData[0] == SET_GROUP_INFO_RSP:
            set_GroupInfoRsp_Handler(self, rcvData)
            a = 1

        elif rcvData[0] == GROUP_ACTIVATE_RSP:
            groupActivateRsp_Handler(self, rcvData)
            a = 1;

        elif rcvData[0] == GROUP_DEACTIVATE_RSP:
            groupDeactivateRsp_Handler(self, rcvData)

        elif rcvData[0] == GROUP_PLAY_RSP:
            groupPlayRsp_Handler(self, rcvData)

        elif rcvData[0] == SET_GROUP_ABS_VOLUME_RSP:
            set_GroupAbsVolumeRsp_Handler(self, rcvData)

        elif rcvData[0] == SET_GROUP_REL_VOLUME_RSP:
            set_GroupRelVolumeRsp_Handler(self, rcvData)

        elif rcvData[0] == SET_GROUP_MUTE_RSP:
            set_GroupMuteRsp_Handler(self, rcvData)

        elif rcvData[0] == VOLUME_CHANGE_IND:
            volumeChangeInd_Handler(self, rcvData)

        elif rcvData[0] == GROUP_PLAY_IND:
            groupPlayInd_Handler(self, rcvData)

        elif rcvData[0] == GROUP_STATUS_IND:
            groupStatusInd_Handler(self, rcvData)

        elif rcvData[0] == AUDIO_PLAYBACK_INFO_IND:
            audioPlaybackInfoInd_Handler(self, rcvData)

        elif rcvData[0] == WIFI_CHANNEL_INFO_IND:
            wifiChannelInfoInd_Handler(self, rcvData)

        a = 1

    def setupUi(self, MainWindow):

        self.receive_signal.connect(self.onReceive)
        setUiSignal(self.receive_signal)

        self.Timer = QTimer(self)

        self.volume_commands = []

        self.WoWIF = []
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1244, 947)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.setAddr_Button = QtWidgets.QPushButton(self.centralwidget)
        self.setAddr_Button.setGeometry(QtCore.QRect(190, 20, 101, 23))
        self.setAddr_Button.setObjectName("setAddr_Button")
        self.getGroupInfo_Button = QtWidgets.QPushButton(self.centralwidget)
        self.getGroupInfo_Button.setGeometry(QtCore.QRect(10, 60, 141, 51))
        self.getGroupInfo_Button.setObjectName("getGroupInfo_Button")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 140, 591, 571))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 50, 131, 16))
        self.label.setObjectName("label")
        self.gridLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 67, 561, 31))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.group0_Mono_Radio = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.group0_Mono_Radio.setObjectName("group0_Mono_Radio")
        self.gridLayout.addWidget(self.group0_Mono_Radio, 0, 0, 1, 1)
        self.group0_512_Radio = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.group0_512_Radio.setObjectName("group0_512_Radio")
        self.gridLayout.addWidget(self.group0_512_Radio, 0, 4, 1, 1)
        self.group0_Stereo_Radio = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.group0_Stereo_Radio.setObjectName("group0_Stereo_Radio")
        self.gridLayout.addWidget(self.group0_Stereo_Radio, 0, 1, 1, 1)
        self.group0_71_Radio = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.group0_71_Radio.setObjectName("group0_71_Radio")
        self.gridLayout.addWidget(self.group0_71_Radio, 0, 5, 1, 1)
        self.group0_51_Radio = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.group0_51_Radio.setObjectName("group0_51_Radio")
        self.gridLayout.addWidget(self.group0_51_Radio, 0, 3, 1, 1)
        self.group0_312_Radio = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.group0_312_Radio.setObjectName("group0_312_Radio")
        self.gridLayout.addWidget(self.group0_312_Radio, 0, 2, 1, 1)
        self.group0_714_Radio = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.group0_714_Radio.setObjectName("group0_714_Radio")
        self.gridLayout.addWidget(self.group0_714_Radio, 0, 7, 1, 1)
        self.group0_712_Radio = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.group0_712_Radio.setObjectName("group0_712_Radio")
        self.gridLayout.addWidget(self.group0_712_Radio, 0, 6, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.groupBox)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 128, 391, 31))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.group0_Concurr_Radio = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        self.group0_Concurr_Radio.setObjectName("group0_Concurr_Radio")
        self.gridLayout_2.addWidget(self.group0_Concurr_Radio, 0, 2, 1, 1)
        self.group0_MultiCh_Radio = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        self.group0_MultiCh_Radio.setObjectName("group0_MultiCh_Radio")
        self.gridLayout_2.addWidget(self.group0_MultiCh_Radio, 0, 0, 1, 1)
        self.group0_MultiRo_Radio = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        self.group0_MultiRo_Radio.setObjectName("group0_MultiRo_Radio")
        self.gridLayout_2.addWidget(self.group0_MultiRo_Radio, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 111, 141, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 169, 91, 16))
        self.label_3.setObjectName("label_3")
        self.group0_Name_LineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.group0_Name_LineEdit.setGeometry(QtCore.QRect(9, 185, 271, 20))
        self.group0_Name_LineEdit.setObjectName("group0_Name_LineEdit")
        self.group0_CheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.group0_CheckBox.setGeometry(QtCore.QRect(10, 22, 121, 16))
        self.group0_CheckBox.setObjectName("group0_CheckBox")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.groupBox)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 212, 526, 31))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.frame_34 = QtWidgets.QFrame(self.gridLayoutWidget_3)
        self.frame_34.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_34.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_34.setObjectName("frame_34")
        self.gridLayout_3.addWidget(self.frame_34, 0, 11, 1, 1)
        self.group0_Device0_Mac2_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.group0_Device0_Mac2_lineEdit.setObjectName("group0_Device0_Mac2_lineEdit")
        self.gridLayout_3.addWidget(self.group0_Device0_Mac2_lineEdit, 0, 3, 1, 1)
        self.group0_Device0_Role_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.group0_Device0_Role_LineEdit.setObjectName("group0_Device0_Role_LineEdit")
        self.gridLayout_3.addWidget(self.group0_Device0_Role_LineEdit, 0, 8, 1, 1)
        self.group0_Device0_CheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget_3)
        self.group0_Device0_CheckBox.setObjectName("group0_Device0_CheckBox")
        self.gridLayout_3.addWidget(self.group0_Device0_CheckBox, 0, 0, 1, 1)
        self.group0_Device0_Mac0_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.group0_Device0_Mac0_lineEdit.setObjectName("group0_Device0_Mac0_lineEdit")
        self.gridLayout_3.addWidget(self.group0_Device0_Mac0_lineEdit, 0, 1, 1, 1)
        self.group0_Device0_Mac4_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.group0_Device0_Mac4_lineEdit.setObjectName("group0_Device0_Mac4_lineEdit")
        self.gridLayout_3.addWidget(self.group0_Device0_Mac4_lineEdit, 0, 5, 1, 1)
        self.group0_Device0_Mac5_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.group0_Device0_Mac5_lineEdit.setObjectName("group0_Device0_Mac5_lineEdit")
        self.gridLayout_3.addWidget(self.group0_Device0_Mac5_lineEdit, 0, 6, 1, 1)
        self.group0_Device0_Mac1_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.group0_Device0_Mac1_lineEdit.setObjectName("group0_Device0_Mac1_lineEdit")
        self.gridLayout_3.addWidget(self.group0_Device0_Mac1_lineEdit, 0, 2, 1, 1)
        self.group0_Device0_Channel_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.group0_Device0_Channel_LineEdit.setObjectName("group0_Device0_Channel_LineEdit")
        self.gridLayout_3.addWidget(self.group0_Device0_Channel_LineEdit, 0, 10, 1, 1)
        self.group0_Device0_Mac3_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.group0_Device0_Mac3_lineEdit.setObjectName("group0_Device0_Mac3_lineEdit")
        self.gridLayout_3.addWidget(self.group0_Device0_Mac3_lineEdit, 0, 4, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.gridLayoutWidget_3)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_3.addWidget(self.frame_2, 0, 9, 1, 1)
        self.frame = QtWidgets.QFrame(self.gridLayoutWidget_3)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_3.addWidget(self.frame, 0, 7, 1, 1)
        self.group0_Device0_Vol_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.group0_Device0_Vol_LineEdit.setObjectName("group0_Device0_Vol_LineEdit")
        self.gridLayout_3.addWidget(self.group0_Device0_Vol_LineEdit, 0, 12, 1, 1)
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.groupBox)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(10, 252, 526, 31))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.group0_Device1_Mac0_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_4)
        self.group0_Device1_Mac0_lineEdit.setObjectName("group0_Device1_Mac0_lineEdit")
        self.gridLayout_4.addWidget(self.group0_Device1_Mac0_lineEdit, 0, 1, 1, 1)
        self.group0_Device1_Role_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_4)
        self.group0_Device1_Role_LineEdit.setObjectName("group0_Device1_Role_LineEdit")
        self.gridLayout_4.addWidget(self.group0_Device1_Role_LineEdit, 0, 8, 1, 1)
        self.group0_Device1_Mac5_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_4)
        self.group0_Device1_Mac5_lineEdit.setObjectName("group0_Device1_Mac5_lineEdit")
        self.gridLayout_4.addWidget(self.group0_Device1_Mac5_lineEdit, 0, 6, 1, 1)
        self.group0_Device1_Mac2_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_4)
        self.group0_Device1_Mac2_lineEdit.setObjectName("group0_Device1_Mac2_lineEdit")
        self.gridLayout_4.addWidget(self.group0_Device1_Mac2_lineEdit, 0, 3, 1, 1)
        self.group0_Device1_CheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget_4)
        self.group0_Device1_CheckBox.setObjectName("group0_Device1_CheckBox")
        self.gridLayout_4.addWidget(self.group0_Device1_CheckBox, 0, 0, 1, 1)
        self.group0_Device1_Mac4_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_4)
        self.group0_Device1_Mac4_lineEdit.setObjectName("group0_Device1_Mac4_lineEdit")
        self.gridLayout_4.addWidget(self.group0_Device1_Mac4_lineEdit, 0, 5, 1, 1)
        self.group0_Device1_Channel_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_4)
        self.group0_Device1_Channel_LineEdit.setObjectName("group0_Device1_Channel_LineEdit")
        self.gridLayout_4.addWidget(self.group0_Device1_Channel_LineEdit, 0, 10, 1, 1)
        self.group0_Device1_Mac1_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_4)
        self.group0_Device1_Mac1_lineEdit.setObjectName("group0_Device1_Mac1_lineEdit")
        self.gridLayout_4.addWidget(self.group0_Device1_Mac1_lineEdit, 0, 2, 1, 1)
        self.group0_Device1_Mac3_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_4)
        self.group0_Device1_Mac3_lineEdit.setObjectName("group0_Device1_Mac3_lineEdit")
        self.gridLayout_4.addWidget(self.group0_Device1_Mac3_lineEdit, 0, 4, 1, 1)
        self.frame_35 = QtWidgets.QFrame(self.gridLayoutWidget_4)
        self.frame_35.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_35.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_35.setObjectName("frame_35")
        self.gridLayout_4.addWidget(self.frame_35, 0, 11, 1, 1)
        self.frame_4 = QtWidgets.QFrame(self.gridLayoutWidget_4)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_4.addWidget(self.frame_4, 0, 7, 1, 1)
        self.frame_3 = QtWidgets.QFrame(self.gridLayoutWidget_4)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_4.addWidget(self.frame_3, 0, 9, 1, 1)
        self.group0_Device1_Vol_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_4)
        self.group0_Device1_Vol_LineEdit.setObjectName("group0_Device1_Vol_LineEdit")
        self.gridLayout_4.addWidget(self.group0_Device1_Vol_LineEdit, 0, 12, 1, 1)
        self.gridLayoutWidget_5 = QtWidgets.QWidget(self.groupBox)
        self.gridLayoutWidget_5.setGeometry(QtCore.QRect(10, 292, 526, 31))
        self.gridLayoutWidget_5.setObjectName("gridLayoutWidget_5")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.gridLayoutWidget_5)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.group0_Device2_Mac2_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_5)
        self.group0_Device2_Mac2_lineEdit.setObjectName("group0_Device2_Mac2_lineEdit")
        self.gridLayout_5.addWidget(self.group0_Device2_Mac2_lineEdit, 0, 3, 1, 1)
        self.group0_Device2_Role_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_5)
        self.group0_Device2_Role_LineEdit.setObjectName("group0_Device2_Role_LineEdit")
        self.gridLayout_5.addWidget(self.group0_Device2_Role_LineEdit, 0, 8, 1, 1)
        self.group0_Device2_Mac3_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_5)
        self.group0_Device2_Mac3_lineEdit.setObjectName("group0_Device2_Mac3_lineEdit")
        self.gridLayout_5.addWidget(self.group0_Device2_Mac3_lineEdit, 0, 4, 1, 1)
        self.group0_Device2_Mac1_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_5)
        self.group0_Device2_Mac1_lineEdit.setObjectName("group0_Device2_Mac1_lineEdit")
        self.gridLayout_5.addWidget(self.group0_Device2_Mac1_lineEdit, 0, 2, 1, 1)
        self.group0_Device2_Mac4_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_5)
        self.group0_Device2_Mac4_lineEdit.setObjectName("group0_Device2_Mac4_lineEdit")
        self.gridLayout_5.addWidget(self.group0_Device2_Mac4_lineEdit, 0, 5, 1, 1)
        self.group0_Device2_CheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget_5)
        self.group0_Device2_CheckBox.setObjectName("group0_Device2_CheckBox")
        self.gridLayout_5.addWidget(self.group0_Device2_CheckBox, 0, 0, 1, 1)
        self.group0_Device2_Channel_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_5)
        self.group0_Device2_Channel_LineEdit.setObjectName("group0_Device2_Channel_LineEdit")
        self.gridLayout_5.addWidget(self.group0_Device2_Channel_LineEdit, 0, 10, 1, 1)
        self.group0_Device2_Mac0_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_5)
        self.group0_Device2_Mac0_lineEdit.setObjectName("group0_Device2_Mac0_lineEdit")
        self.gridLayout_5.addWidget(self.group0_Device2_Mac0_lineEdit, 0, 1, 1, 1)
        self.group0_Device2_Mac5_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_5)
        self.group0_Device2_Mac5_lineEdit.setObjectName("group0_Device2_Mac5_lineEdit")
        self.gridLayout_5.addWidget(self.group0_Device2_Mac5_lineEdit, 0, 6, 1, 1)
        self.frame_5 = QtWidgets.QFrame(self.gridLayoutWidget_5)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.gridLayout_5.addWidget(self.frame_5, 0, 9, 1, 1)
        self.frame_6 = QtWidgets.QFrame(self.gridLayoutWidget_5)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.gridLayout_5.addWidget(self.frame_6, 0, 7, 1, 1)
        self.frame_33 = QtWidgets.QFrame(self.gridLayoutWidget_5)
        self.frame_33.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_33.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_33.setObjectName("frame_33")
        self.gridLayout_5.addWidget(self.frame_33, 0, 11, 1, 1)
        self.group0_Device2_Vol_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_5)
        self.group0_Device2_Vol_LineEdit.setObjectName("group0_Device2_Vol_LineEdit")
        self.gridLayout_5.addWidget(self.group0_Device2_Vol_LineEdit, 0, 12, 1, 1)
        self.gridLayoutWidget_6 = QtWidgets.QWidget(self.groupBox)
        self.gridLayoutWidget_6.setGeometry(QtCore.QRect(10, 332, 526, 31))
        self.gridLayoutWidget_6.setObjectName("gridLayoutWidget_6")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.gridLayoutWidget_6)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.group0_Device3_Mac1_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_6)
        self.group0_Device3_Mac1_lineEdit.setObjectName("group0_Device3_Mac1_lineEdit")
        self.gridLayout_6.addWidget(self.group0_Device3_Mac1_lineEdit, 0, 2, 1, 1)
        self.group0_Device3_Mac3_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_6)
        self.group0_Device3_Mac3_lineEdit.setObjectName("group0_Device3_Mac3_lineEdit")
        self.gridLayout_6.addWidget(self.group0_Device3_Mac3_lineEdit, 0, 4, 1, 1)
        self.group0_Device3_Mac5_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_6)
        self.group0_Device3_Mac5_lineEdit.setObjectName("group0_Device3_Mac5_lineEdit")
        self.gridLayout_6.addWidget(self.group0_Device3_Mac5_lineEdit, 0, 6, 1, 1)
        self.group0_Device3_Mac4_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_6)
        self.group0_Device3_Mac4_lineEdit.setObjectName("group0_Device3_Mac4_lineEdit")
        self.gridLayout_6.addWidget(self.group0_Device3_Mac4_lineEdit, 0, 5, 1, 1)
        self.group0_Device3_Channel_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_6)
        self.group0_Device3_Channel_LineEdit.setObjectName("group0_Device3_Channel_LineEdit")
        self.gridLayout_6.addWidget(self.group0_Device3_Channel_LineEdit, 0, 10, 1, 1)
        self.frame_36 = QtWidgets.QFrame(self.gridLayoutWidget_6)
        self.frame_36.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_36.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_36.setObjectName("frame_36")
        self.gridLayout_6.addWidget(self.frame_36, 0, 11, 1, 1)
        self.frame_7 = QtWidgets.QFrame(self.gridLayoutWidget_6)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.gridLayout_6.addWidget(self.frame_7, 0, 9, 1, 1)
        self.frame_8 = QtWidgets.QFrame(self.gridLayoutWidget_6)
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.gridLayout_6.addWidget(self.frame_8, 0, 7, 1, 1)
        self.group0_Device3_Mac0_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_6)
        self.group0_Device3_Mac0_lineEdit.setObjectName("group0_Device3_Mac0_lineEdit")
        self.gridLayout_6.addWidget(self.group0_Device3_Mac0_lineEdit, 0, 1, 1, 1)
        self.group0_Device3_CheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget_6)
        self.group0_Device3_CheckBox.setObjectName("group0_Device3_CheckBox")
        self.gridLayout_6.addWidget(self.group0_Device3_CheckBox, 0, 0, 1, 1)
        self.group0_Device3_Role_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_6)
        self.group0_Device3_Role_LineEdit.setObjectName("group0_Device3_Role_LineEdit")
        self.gridLayout_6.addWidget(self.group0_Device3_Role_LineEdit, 0, 8, 1, 1)
        self.group0_Device3_Mac2_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_6)
        self.group0_Device3_Mac2_lineEdit.setObjectName("group0_Device3_Mac2_lineEdit")
        self.gridLayout_6.addWidget(self.group0_Device3_Mac2_lineEdit, 0, 3, 1, 1)
        self.group0_Device3_Vol_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_6)
        self.group0_Device3_Vol_LineEdit.setObjectName("group0_Device3_Vol_LineEdit")
        self.gridLayout_6.addWidget(self.group0_Device3_Vol_LineEdit, 0, 12, 1, 1)
        self.gridLayoutWidget_7 = QtWidgets.QWidget(self.groupBox)
        self.gridLayoutWidget_7.setGeometry(QtCore.QRect(10, 372, 526, 31))
        self.gridLayoutWidget_7.setObjectName("gridLayoutWidget_7")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.gridLayoutWidget_7)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.frame_38 = QtWidgets.QFrame(self.gridLayoutWidget_7)
        self.frame_38.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_38.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_38.setObjectName("frame_38")
        self.gridLayout_7.addWidget(self.frame_38, 0, 11, 1, 1)
        self.frame_9 = QtWidgets.QFrame(self.gridLayoutWidget_7)
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.gridLayout_7.addWidget(self.frame_9, 0, 9, 1, 1)
        self.frame_10 = QtWidgets.QFrame(self.gridLayoutWidget_7)
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.gridLayout_7.addWidget(self.frame_10, 0, 7, 1, 1)
        self.group0_Device4_Mac3_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_7)
        self.group0_Device4_Mac3_lineEdit.setObjectName("group0_Device4_Mac3_lineEdit")
        self.gridLayout_7.addWidget(self.group0_Device4_Mac3_lineEdit, 0, 4, 1, 1)
        self.group0_Device4_Mac4_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_7)
        self.group0_Device4_Mac4_lineEdit.setObjectName("group0_Device4_Mac4_lineEdit")
        self.gridLayout_7.addWidget(self.group0_Device4_Mac4_lineEdit, 0, 5, 1, 1)
        self.group0_Device4_CheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget_7)
        self.group0_Device4_CheckBox.setObjectName("group0_Device4_CheckBox")
        self.gridLayout_7.addWidget(self.group0_Device4_CheckBox, 0, 0, 1, 1)
        self.group0_Device4_Role_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_7)
        self.group0_Device4_Role_LineEdit.setObjectName("group0_Device4_Role_LineEdit")
        self.gridLayout_7.addWidget(self.group0_Device4_Role_LineEdit, 0, 8, 1, 1)
        self.group0_Device4_Mac2_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_7)
        self.group0_Device4_Mac2_lineEdit.setObjectName("group0_Device4_Mac2_lineEdit")
        self.gridLayout_7.addWidget(self.group0_Device4_Mac2_lineEdit, 0, 3, 1, 1)
        self.group0_Device4_Mac1_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_7)
        self.group0_Device4_Mac1_lineEdit.setObjectName("group0_Device4_Mac1_lineEdit")
        self.gridLayout_7.addWidget(self.group0_Device4_Mac1_lineEdit, 0, 2, 1, 1)
        self.group0_Device4_Mac5_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_7)
        self.group0_Device4_Mac5_lineEdit.setObjectName("group0_Device4_Mac5_lineEdit")
        self.gridLayout_7.addWidget(self.group0_Device4_Mac5_lineEdit, 0, 6, 1, 1)
        self.group0_Device4_Mac0_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_7)
        self.group0_Device4_Mac0_lineEdit.setObjectName("group0_Device4_Mac0_lineEdit")
        self.gridLayout_7.addWidget(self.group0_Device4_Mac0_lineEdit, 0, 1, 1, 1)
        self.group0_Device4_Channel_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_7)
        self.group0_Device4_Channel_LineEdit.setObjectName("group0_Device4_Channel_LineEdit")
        self.gridLayout_7.addWidget(self.group0_Device4_Channel_LineEdit, 0, 10, 1, 1)
        self.group0_Device4_Vol_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_7)
        self.group0_Device4_Vol_LineEdit.setObjectName("group0_Device4_Vol_LineEdit")
        self.gridLayout_7.addWidget(self.group0_Device4_Vol_LineEdit, 0, 12, 1, 1)
        self.gridLayoutWidget_8 = QtWidgets.QWidget(self.groupBox)
        self.gridLayoutWidget_8.setGeometry(QtCore.QRect(10, 410, 526, 31))
        self.gridLayoutWidget_8.setObjectName("gridLayoutWidget_8")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.gridLayoutWidget_8)
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.frame_39 = QtWidgets.QFrame(self.gridLayoutWidget_8)
        self.frame_39.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_39.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_39.setObjectName("frame_39")
        self.gridLayout_8.addWidget(self.frame_39, 0, 11, 1, 1)
        self.frame_12 = QtWidgets.QFrame(self.gridLayoutWidget_8)
        self.frame_12.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setObjectName("frame_12")
        self.gridLayout_8.addWidget(self.frame_12, 0, 7, 1, 1)
        self.frame_11 = QtWidgets.QFrame(self.gridLayoutWidget_8)
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.gridLayout_8.addWidget(self.frame_11, 0, 9, 1, 1)
        self.group0_Device5_Mac3_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_8)
        self.group0_Device5_Mac3_lineEdit.setObjectName("group0_Device5_Mac3_lineEdit")
        self.gridLayout_8.addWidget(self.group0_Device5_Mac3_lineEdit, 0, 4, 1, 1)
        self.group0_Device5_Mac5_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_8)
        self.group0_Device5_Mac5_lineEdit.setObjectName("group0_Device5_Mac5_lineEdit")
        self.gridLayout_8.addWidget(self.group0_Device5_Mac5_lineEdit, 0, 6, 1, 1)
        self.group0_Device5_Mac4_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_8)
        self.group0_Device5_Mac4_lineEdit.setObjectName("group0_Device5_Mac4_lineEdit")
        self.gridLayout_8.addWidget(self.group0_Device5_Mac4_lineEdit, 0, 5, 1, 1)
        self.group0_Device5_Channel_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_8)
        self.group0_Device5_Channel_LineEdit.setObjectName("group0_Device5_Channel_LineEdit")
        self.gridLayout_8.addWidget(self.group0_Device5_Channel_LineEdit, 0, 10, 1, 1)
        self.group0_Device5_Mac1_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_8)
        self.group0_Device5_Mac1_lineEdit.setObjectName("group0_Device5_Mac1_lineEdit")
        self.gridLayout_8.addWidget(self.group0_Device5_Mac1_lineEdit, 0, 2, 1, 1)
        self.group0_Device5_Mac2_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_8)
        self.group0_Device5_Mac2_lineEdit.setObjectName("group0_Device5_Mac2_lineEdit")
        self.gridLayout_8.addWidget(self.group0_Device5_Mac2_lineEdit, 0, 3, 1, 1)
        self.group0_Device5_Mac0_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_8)
        self.group0_Device5_Mac0_lineEdit.setObjectName("group0_Device5_Mac0_lineEdit")
        self.gridLayout_8.addWidget(self.group0_Device5_Mac0_lineEdit, 0, 1, 1, 1)
        self.group0_Device5_Role_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_8)
        self.group0_Device5_Role_LineEdit.setObjectName("group0_Device5_Role_LineEdit")
        self.gridLayout_8.addWidget(self.group0_Device5_Role_LineEdit, 0, 8, 1, 1)
        self.group0_Device5_CheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget_8)
        self.group0_Device5_CheckBox.setObjectName("group0_Device5_CheckBox")
        self.gridLayout_8.addWidget(self.group0_Device5_CheckBox, 0, 0, 1, 1)
        self.group0_Device5_Vol_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_8)
        self.group0_Device5_Vol_LineEdit.setObjectName("group0_Device5_Vol_LineEdit")
        self.gridLayout_8.addWidget(self.group0_Device5_Vol_LineEdit, 0, 12, 1, 1)
        self.gridLayoutWidget_9 = QtWidgets.QWidget(self.groupBox)
        self.gridLayoutWidget_9.setGeometry(QtCore.QRect(10, 450, 526, 31))
        self.gridLayoutWidget_9.setObjectName("gridLayoutWidget_9")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.gridLayoutWidget_9)
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.frame_40 = QtWidgets.QFrame(self.gridLayoutWidget_9)
        self.frame_40.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_40.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_40.setObjectName("frame_40")
        self.gridLayout_9.addWidget(self.frame_40, 0, 11, 1, 1)
        self.frame_13 = QtWidgets.QFrame(self.gridLayoutWidget_9)
        self.frame_13.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_13.setObjectName("frame_13")
        self.gridLayout_9.addWidget(self.frame_13, 0, 9, 1, 1)
        self.frame_14 = QtWidgets.QFrame(self.gridLayoutWidget_9)
        self.frame_14.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_14.setObjectName("frame_14")
        self.gridLayout_9.addWidget(self.frame_14, 0, 7, 1, 1)
        self.group0_Device6_Role_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_9)
        self.group0_Device6_Role_LineEdit.setObjectName("group0_Device6_Role_LineEdit")
        self.gridLayout_9.addWidget(self.group0_Device6_Role_LineEdit, 0, 8, 1, 1)
        self.group0_Device6_Channel_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_9)
        self.group0_Device6_Channel_LineEdit.setObjectName("group0_Device6_Channel_LineEdit")
        self.gridLayout_9.addWidget(self.group0_Device6_Channel_LineEdit, 0, 10, 1, 1)
        self.group0_Device6_Mac3_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_9)
        self.group0_Device6_Mac3_lineEdit.setObjectName("group0_Device6_Mac3_lineEdit")
        self.gridLayout_9.addWidget(self.group0_Device6_Mac3_lineEdit, 0, 4, 1, 1)
        self.group0_Device6_Mac1_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_9)
        self.group0_Device6_Mac1_lineEdit.setObjectName("group0_Device6_Mac1_lineEdit")
        self.gridLayout_9.addWidget(self.group0_Device6_Mac1_lineEdit, 0, 2, 1, 1)
        self.group0_Device6_Mac0_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_9)
        self.group0_Device6_Mac0_lineEdit.setObjectName("group0_Device6_Mac0_lineEdit")
        self.gridLayout_9.addWidget(self.group0_Device6_Mac0_lineEdit, 0, 1, 1, 1)
        self.group0_Device6_Mac4_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_9)
        self.group0_Device6_Mac4_lineEdit.setObjectName("group0_Device6_Mac4_lineEdit")
        self.gridLayout_9.addWidget(self.group0_Device6_Mac4_lineEdit, 0, 5, 1, 1)
        self.group0_Device6_CheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget_9)
        self.group0_Device6_CheckBox.setObjectName("group0_Device6_CheckBox")
        self.gridLayout_9.addWidget(self.group0_Device6_CheckBox, 0, 0, 1, 1)
        self.group0_Device6_Mac5_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_9)
        self.group0_Device6_Mac5_lineEdit.setObjectName("group0_Device6_Mac5_lineEdit")
        self.gridLayout_9.addWidget(self.group0_Device6_Mac5_lineEdit, 0, 6, 1, 1)
        self.group0_Device6_Mac2_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_9)
        self.group0_Device6_Mac2_lineEdit.setObjectName("group0_Device6_Mac2_lineEdit")
        self.gridLayout_9.addWidget(self.group0_Device6_Mac2_lineEdit, 0, 3, 1, 1)
        self.group0_Device6_Vol_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_9)
        self.group0_Device6_Vol_LineEdit.setObjectName("group0_Device6_Vol_LineEdit")
        self.gridLayout_9.addWidget(self.group0_Device6_Vol_LineEdit, 0, 12, 1, 1)
        self.gridLayoutWidget_10 = QtWidgets.QWidget(self.groupBox)
        self.gridLayoutWidget_10.setGeometry(QtCore.QRect(10, 490, 526, 31))
        self.gridLayoutWidget_10.setObjectName("gridLayoutWidget_10")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.gridLayoutWidget_10)
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.group0_Device7_Role_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_10)
        self.group0_Device7_Role_LineEdit.setObjectName("group0_Device7_Role_LineEdit")
        self.gridLayout_10.addWidget(self.group0_Device7_Role_LineEdit, 0, 8, 1, 1)
        self.group0_Device7_Mac3_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_10)
        self.group0_Device7_Mac3_lineEdit.setObjectName("group0_Device7_Mac3_lineEdit")
        self.gridLayout_10.addWidget(self.group0_Device7_Mac3_lineEdit, 0, 4, 1, 1)
        self.group0_Device7_Mac0_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_10)
        self.group0_Device7_Mac0_lineEdit.setObjectName("group0_Device7_Mac0_lineEdit")
        self.gridLayout_10.addWidget(self.group0_Device7_Mac0_lineEdit, 0, 1, 1, 1)
        self.group0_Device7_CheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget_10)
        self.group0_Device7_CheckBox.setObjectName("group0_Device7_CheckBox")
        self.gridLayout_10.addWidget(self.group0_Device7_CheckBox, 0, 0, 1, 1)
        self.group0_Device7_Channel_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_10)
        self.group0_Device7_Channel_LineEdit.setObjectName("group0_Device7_Channel_LineEdit")
        self.gridLayout_10.addWidget(self.group0_Device7_Channel_LineEdit, 0, 10, 1, 1)
        self.group0_Device7_Mac4_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_10)
        self.group0_Device7_Mac4_lineEdit.setObjectName("group0_Device7_Mac4_lineEdit")
        self.gridLayout_10.addWidget(self.group0_Device7_Mac4_lineEdit, 0, 5, 1, 1)
        self.group0_Device7_Mac2_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_10)
        self.group0_Device7_Mac2_lineEdit.setObjectName("group0_Device7_Mac2_lineEdit")
        self.gridLayout_10.addWidget(self.group0_Device7_Mac2_lineEdit, 0, 3, 1, 1)
        self.group0_Device7_Mac5_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_10)
        self.group0_Device7_Mac5_lineEdit.setObjectName("group0_Device7_Mac5_lineEdit")
        self.gridLayout_10.addWidget(self.group0_Device7_Mac5_lineEdit, 0, 6, 1, 1)
        self.group0_Device7_Mac1_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_10)
        self.group0_Device7_Mac1_lineEdit.setObjectName("group0_Device7_Mac1_lineEdit")
        self.gridLayout_10.addWidget(self.group0_Device7_Mac1_lineEdit, 0, 2, 1, 1)
        self.group0_Device7_Vol_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_10)
        self.group0_Device7_Vol_LineEdit.setObjectName("group0_Device7_Vol_LineEdit")
        self.gridLayout_10.addWidget(self.group0_Device7_Vol_LineEdit, 0, 12, 1, 1)
        self.frame_15 = QtWidgets.QFrame(self.gridLayoutWidget_10)
        self.frame_15.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_15.setObjectName("frame_15")
        self.gridLayout_10.addWidget(self.frame_15, 0, 9, 1, 1)
        self.frame_16 = QtWidgets.QFrame(self.gridLayoutWidget_10)
        self.frame_16.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_16.setObjectName("frame_16")
        self.gridLayout_10.addWidget(self.frame_16, 0, 7, 1, 1)
        self.frame_41 = QtWidgets.QFrame(self.gridLayoutWidget_10)
        self.frame_41.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_41.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_41.setObjectName("frame_41")
        self.gridLayout_10.addWidget(self.frame_41, 0, 11, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setGeometry(QtCore.QRect(380, 190, 31, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setGeometry(QtCore.QRect(431, 191, 51, 16))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        self.label_11.setGeometry(QtCore.QRect(503, 190, 31, 16))
        self.label_11.setObjectName("label_11")
        self.gridLayoutWidget_31 = QtWidgets.QWidget(self.groupBox)
        self.gridLayoutWidget_31.setGeometry(QtCore.QRect(10, 530, 526, 31))
        self.gridLayoutWidget_31.setObjectName("gridLayoutWidget_31")
        self.gridLayout_31 = QtWidgets.QGridLayout(self.gridLayoutWidget_31)
        self.gridLayout_31.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_31.setObjectName("gridLayout_31")
        self.group0_Device8_Role_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_31)
        self.group0_Device8_Role_LineEdit.setObjectName("group0_Device8_Role_LineEdit")
        self.gridLayout_31.addWidget(self.group0_Device8_Role_LineEdit, 0, 8, 1, 1)
        self.group0_Device8_Mac3_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_31)
        self.group0_Device8_Mac3_lineEdit.setObjectName("group0_Device8_Mac3_lineEdit")
        self.gridLayout_31.addWidget(self.group0_Device8_Mac3_lineEdit, 0, 4, 1, 1)
        self.group0_Device8_Mac0_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_31)
        self.group0_Device8_Mac0_lineEdit.setObjectName("group0_Device8_Mac0_lineEdit")
        self.gridLayout_31.addWidget(self.group0_Device8_Mac0_lineEdit, 0, 1, 1, 1)
        self.group0_Device8_CheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget_31)
        self.group0_Device8_CheckBox.setObjectName("group0_Device8_CheckBox")
        self.gridLayout_31.addWidget(self.group0_Device8_CheckBox, 0, 0, 1, 1)
        self.group0_Device8_Channel_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_31)
        self.group0_Device8_Channel_LineEdit.setObjectName("group0_Device8_Channel_LineEdit")
        self.gridLayout_31.addWidget(self.group0_Device8_Channel_LineEdit, 0, 10, 1, 1)
        self.group0_Device8_Mac4_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_31)
        self.group0_Device8_Mac4_lineEdit.setObjectName("group0_Device8_Mac4_lineEdit")
        self.gridLayout_31.addWidget(self.group0_Device8_Mac4_lineEdit, 0, 5, 1, 1)
        self.group0_Device8_Mac2_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_31)
        self.group0_Device8_Mac2_lineEdit.setObjectName("group0_Device8_Mac2_lineEdit")
        self.gridLayout_31.addWidget(self.group0_Device8_Mac2_lineEdit, 0, 3, 1, 1)
        self.group0_Device8_Mac5_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_31)
        self.group0_Device8_Mac5_lineEdit.setObjectName("group0_Device8_Mac5_lineEdit")
        self.gridLayout_31.addWidget(self.group0_Device8_Mac5_lineEdit, 0, 6, 1, 1)
        self.group0_Device8_Mac1_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_31)
        self.group0_Device8_Mac1_lineEdit.setObjectName("group0_Device8_Mac1_lineEdit")
        self.gridLayout_31.addWidget(self.group0_Device8_Mac1_lineEdit, 0, 2, 1, 1)
        self.group0_Device8_Vol_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_31)
        self.group0_Device8_Vol_LineEdit.setObjectName("group0_Device8_Vol_LineEdit")
        self.gridLayout_31.addWidget(self.group0_Device8_Vol_LineEdit, 0, 12, 1, 1)
        self.frame_73 = QtWidgets.QFrame(self.gridLayoutWidget_31)
        self.frame_73.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_73.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_73.setObjectName("frame_73")
        self.gridLayout_31.addWidget(self.frame_73, 0, 9, 1, 1)
        self.frame_74 = QtWidgets.QFrame(self.gridLayoutWidget_31)
        self.frame_74.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_74.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_74.setObjectName("frame_74")
        self.gridLayout_31.addWidget(self.frame_74, 0, 7, 1, 1)
        self.frame_75 = QtWidgets.QFrame(self.gridLayoutWidget_31)
        self.frame_75.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_75.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_75.setObjectName("frame_75")
        self.gridLayout_31.addWidget(self.frame_75, 0, 11, 1, 1)
        self.group0_groupVolume_LineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.group0_groupVolume_LineEdit.setGeometry(QtCore.QRect(490, 150, 51, 20))
        self.group0_groupVolume_LineEdit.setObjectName("group0_groupVolume_LineEdit")
        self.label_17 = QtWidgets.QLabel(self.groupBox)
        self.label_17.setGeometry(QtCore.QRect(487, 130, 61, 20))
        self.label_17.setObjectName("label_17")
        self.addr_LineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.addr_LineEdit.setGeometry(QtCore.QRect(10, 21, 171, 20))
        self.addr_LineEdit.setObjectName("addr_LineEdit")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(430, 60, 171, 71))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(310, 60, 111, 71))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(630, 140, 591, 571))
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(10, 50, 131, 16))
        self.label_4.setObjectName("label_4")
        self.gridLayoutWidget_11 = QtWidgets.QWidget(self.groupBox_2)
        self.gridLayoutWidget_11.setGeometry(QtCore.QRect(10, 67, 561, 31))
        self.gridLayoutWidget_11.setObjectName("gridLayoutWidget_11")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.gridLayoutWidget_11)
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.group1_71_Radio = QtWidgets.QRadioButton(self.gridLayoutWidget_11)
        self.group1_71_Radio.setObjectName("group1_71_Radio")
        self.gridLayout_11.addWidget(self.group1_71_Radio, 0, 5, 1, 1)
        self.group1_Stereo_Radio = QtWidgets.QRadioButton(self.gridLayoutWidget_11)
        self.group1_Stereo_Radio.setObjectName("group1_Stereo_Radio")
        self.gridLayout_11.addWidget(self.group1_Stereo_Radio, 0, 1, 1, 1)
        self.group1_51_Radio = QtWidgets.QRadioButton(self.gridLayoutWidget_11)
        self.group1_51_Radio.setObjectName("group1_51_Radio")
        self.gridLayout_11.addWidget(self.group1_51_Radio, 0, 3, 1, 1)
        self.group1_712_Radio = QtWidgets.QRadioButton(self.gridLayoutWidget_11)
        self.group1_712_Radio.setObjectName("group1_712_Radio")
        self.gridLayout_11.addWidget(self.group1_712_Radio, 0, 6, 1, 1)
        self.group1_512_Radio = QtWidgets.QRadioButton(self.gridLayoutWidget_11)
        self.group1_512_Radio.setObjectName("group1_512_Radio")
        self.gridLayout_11.addWidget(self.group1_512_Radio, 0, 4, 1, 1)
        self.group1_312_Radio = QtWidgets.QRadioButton(self.gridLayoutWidget_11)
        self.group1_312_Radio.setObjectName("group1_312_Radio")
        self.gridLayout_11.addWidget(self.group1_312_Radio, 0, 2, 1, 1)
        self.group1_Mono_Radio = QtWidgets.QRadioButton(self.gridLayoutWidget_11)
        self.group1_Mono_Radio.setObjectName("group1_Mono_Radio")
        self.gridLayout_11.addWidget(self.group1_Mono_Radio, 0, 0, 1, 1)
        self.group1_714_Radio = QtWidgets.QRadioButton(self.gridLayoutWidget_11)
        self.group1_714_Radio.setObjectName("group1_714_Radio")
        self.gridLayout_11.addWidget(self.group1_714_Radio, 0, 7, 1, 1)
        self.gridLayoutWidget_12 = QtWidgets.QWidget(self.groupBox_2)
        self.gridLayoutWidget_12.setGeometry(QtCore.QRect(10, 128, 391, 31))
        self.gridLayoutWidget_12.setObjectName("gridLayoutWidget_12")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.gridLayoutWidget_12)
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_12.setObjectName("gridLayout_12")

        self.group1_Concurr_Radio = QtWidgets.QRadioButton(self.gridLayoutWidget_12)
        self.group1_Concurr_Radio.setObjectName("group1_Concurr_Radio")
        self.gridLayout_12.addWidget(self.group1_Concurr_Radio, 0, 2, 1, 1)
        self.group1_MultiCh_Radio = QtWidgets.QRadioButton(self.gridLayoutWidget_12)
        self.group1_MultiCh_Radio.setObjectName("group1_MultiCh_Radio")
        self.gridLayout_12.addWidget(self.group1_MultiCh_Radio, 0, 0, 1, 1)
        self.group1_MultiRo_Radio = QtWidgets.QRadioButton(self.gridLayoutWidget_12)
        self.group1_MultiRo_Radio.setObjectName("group1_MultiRo_Radio")
        self.gridLayout_12.addWidget(self.group1_MultiRo_Radio, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(10, 111, 141, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(10, 169, 91, 16))
        self.label_6.setObjectName("label_6")
        self.group1_Name_LineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.group1_Name_LineEdit.setGeometry(QtCore.QRect(9, 185, 271, 20))
        self.group1_Name_LineEdit.setObjectName("group1_Name_LineEdit")
        self.group1_CheckBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.group1_CheckBox.setGeometry(QtCore.QRect(10, 22, 121, 16))
        self.group1_CheckBox.setObjectName("group1_CheckBox")
        self.gridLayoutWidget_13 = QtWidgets.QWidget(self.groupBox_2)
        self.gridLayoutWidget_13.setGeometry(QtCore.QRect(10, 212, 526, 31))
        self.gridLayoutWidget_13.setObjectName("gridLayoutWidget_13")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.gridLayoutWidget_13)
        self.gridLayout_13.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.group1_Device0_Mac3_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_13)
        self.group1_Device0_Mac3_lineEdit.setObjectName("group1_Device0_Mac3_lineEdit")
        self.gridLayout_13.addWidget(self.group1_Device0_Mac3_lineEdit, 0, 4, 1, 1)
        self.group1_Device0_Mac1_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_13)
        self.group1_Device0_Mac1_lineEdit.setObjectName("group1_Device0_Mac1_lineEdit")
        self.gridLayout_13.addWidget(self.group1_Device0_Mac1_lineEdit, 0, 2, 1, 1)
        self.group1_Device0_Mac5_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_13)
        self.group1_Device0_Mac5_lineEdit.setObjectName("group1_Device0_Mac5_lineEdit")
        self.gridLayout_13.addWidget(self.group1_Device0_Mac5_lineEdit, 0, 6, 1, 1)
        self.group1_Device0_Role_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_13)
        self.group1_Device0_Role_LineEdit.setObjectName("group1_Device0_Role_LineEdit")
        self.gridLayout_13.addWidget(self.group1_Device0_Role_LineEdit, 0, 8, 1, 1)
        self.group1_Device0_CheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget_13)
        self.group1_Device0_CheckBox.setObjectName("group1_Device0_CheckBox")
        self.gridLayout_13.addWidget(self.group1_Device0_CheckBox, 0, 0, 1, 1)
        self.group1_Device0_Mac2_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_13)
        self.group1_Device0_Mac2_lineEdit.setObjectName("group1_Device0_Mac2_lineEdit")
        self.gridLayout_13.addWidget(self.group1_Device0_Mac2_lineEdit, 0, 3, 1, 1)
        self.group1_Device0_Mac0_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_13)
        self.group1_Device0_Mac0_lineEdit.setObjectName("group1_Device0_Mac0_lineEdit")
        self.gridLayout_13.addWidget(self.group1_Device0_Mac0_lineEdit, 0, 1, 1, 1)
        self.group1_Device0_Mac4_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_13)
        self.group1_Device0_Mac4_lineEdit.setObjectName("group1_Device0_Mac4_lineEdit")
        self.gridLayout_13.addWidget(self.group1_Device0_Mac4_lineEdit, 0, 5, 1, 1)
        self.group1_Device0_Channel_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_13)
        self.group1_Device0_Channel_LineEdit.setObjectName("group1_Device0_Channel_LineEdit")
        self.gridLayout_13.addWidget(self.group1_Device0_Channel_LineEdit, 0, 10, 1, 1)
        self.frame_17 = QtWidgets.QFrame(self.gridLayoutWidget_13)
        self.frame_17.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_17.setObjectName("frame_17")
        self.gridLayout_13.addWidget(self.frame_17, 0, 9, 1, 1)
        self.frame_18 = QtWidgets.QFrame(self.gridLayoutWidget_13)
        self.frame_18.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_18.setObjectName("frame_18")
        self.gridLayout_13.addWidget(self.frame_18, 0, 7, 1, 1)
        self.frame_42 = QtWidgets.QFrame(self.gridLayoutWidget_13)
        self.frame_42.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_42.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_42.setObjectName("frame_42")
        self.gridLayout_13.addWidget(self.frame_42, 0, 11, 1, 1)
        self.group1_Device0_Vol_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_13)
        self.group1_Device0_Vol_LineEdit.setObjectName("group1_Device0_Vol_LineEdit")
        self.gridLayout_13.addWidget(self.group1_Device0_Vol_LineEdit, 0, 12, 1, 1)
        self.gridLayoutWidget_14 = QtWidgets.QWidget(self.groupBox_2)
        self.gridLayoutWidget_14.setGeometry(QtCore.QRect(10, 252, 526, 31))
        self.gridLayoutWidget_14.setObjectName("gridLayoutWidget_14")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.gridLayoutWidget_14)
        self.gridLayout_14.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.group1_Device1_Mac1_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_14)
        self.group1_Device1_Mac1_lineEdit.setObjectName("group1_Device1_Mac1_lineEdit")
        self.gridLayout_14.addWidget(self.group1_Device1_Mac1_lineEdit, 0, 2, 1, 1)
        self.group1_Device1_Mac3_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_14)
        self.group1_Device1_Mac3_lineEdit.setObjectName("group1_Device1_Mac3_lineEdit")
        self.gridLayout_14.addWidget(self.group1_Device1_Mac3_lineEdit, 0, 4, 1, 1)
        self.group1_Device1_CheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget_14)
        self.group1_Device1_CheckBox.setObjectName("group1_Device1_CheckBox")
        self.gridLayout_14.addWidget(self.group1_Device1_CheckBox, 0, 0, 1, 1)
        self.group1_Device1_Channel_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_14)
        self.group1_Device1_Channel_LineEdit.setObjectName("group1_Device1_Channel_LineEdit")
        self.gridLayout_14.addWidget(self.group1_Device1_Channel_LineEdit, 0, 10, 1, 1)
        self.group1_Device1_Mac0_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_14)
        self.group1_Device1_Mac0_lineEdit.setObjectName("group1_Device1_Mac0_lineEdit")
        self.gridLayout_14.addWidget(self.group1_Device1_Mac0_lineEdit, 0, 1, 1, 1)
        self.group1_Device1_Mac4_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_14)
        self.group1_Device1_Mac4_lineEdit.setObjectName("group1_Device1_Mac4_lineEdit")
        self.gridLayout_14.addWidget(self.group1_Device1_Mac4_lineEdit, 0, 5, 1, 1)
        self.group1_Device1_Mac5_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_14)
        self.group1_Device1_Mac5_lineEdit.setObjectName("group1_Device1_Mac5_lineEdit")
        self.gridLayout_14.addWidget(self.group1_Device1_Mac5_lineEdit, 0, 6, 1, 1)
        self.group1_Device1_Mac2_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_14)
        self.group1_Device1_Mac2_lineEdit.setObjectName("group1_Device1_Mac2_lineEdit")
        self.gridLayout_14.addWidget(self.group1_Device1_Mac2_lineEdit, 0, 3, 1, 1)
        self.group1_Device1_Role_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_14)
        self.group1_Device1_Role_LineEdit.setObjectName("group1_Device1_Role_LineEdit")
        self.gridLayout_14.addWidget(self.group1_Device1_Role_LineEdit, 0, 8, 1, 1)
        self.frame_19 = QtWidgets.QFrame(self.gridLayoutWidget_14)
        self.frame_19.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_19.setObjectName("frame_19")
        self.gridLayout_14.addWidget(self.frame_19, 0, 9, 1, 1)
        self.frame_20 = QtWidgets.QFrame(self.gridLayoutWidget_14)
        self.frame_20.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_20.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_20.setObjectName("frame_20")
        self.gridLayout_14.addWidget(self.frame_20, 0, 7, 1, 1)
        self.frame_43 = QtWidgets.QFrame(self.gridLayoutWidget_14)
        self.frame_43.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_43.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_43.setObjectName("frame_43")
        self.gridLayout_14.addWidget(self.frame_43, 0, 11, 1, 1)
        self.group1_Device1_Vol_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_14)
        self.group1_Device1_Vol_LineEdit.setObjectName("group1_Device1_Vol_LineEdit")
        self.gridLayout_14.addWidget(self.group1_Device1_Vol_LineEdit, 0, 12, 1, 1)
        self.gridLayoutWidget_15 = QtWidgets.QWidget(self.groupBox_2)
        self.gridLayoutWidget_15.setGeometry(QtCore.QRect(10, 292, 526, 31))
        self.gridLayoutWidget_15.setObjectName("gridLayoutWidget_15")
        self.gridLayout_15 = QtWidgets.QGridLayout(self.gridLayoutWidget_15)
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.group1_Device2_Mac2_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_15)
        self.group1_Device2_Mac2_lineEdit.setObjectName("group1_Device2_Mac2_lineEdit")
        self.gridLayout_15.addWidget(self.group1_Device2_Mac2_lineEdit, 0, 3, 1, 1)
        self.group1_Device2_Role_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_15)
        self.group1_Device2_Role_LineEdit.setObjectName("group1_Device2_Role_LineEdit")
        self.gridLayout_15.addWidget(self.group1_Device2_Role_LineEdit, 0, 8, 1, 1)
        self.group1_Device2_CheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget_15)
        self.group1_Device2_CheckBox.setObjectName("group1_Device2_CheckBox")
        self.gridLayout_15.addWidget(self.group1_Device2_CheckBox, 0, 0, 1, 1)
        self.group1_Device2_Mac0_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_15)
        self.group1_Device2_Mac0_lineEdit.setObjectName("group1_Device2_Mac0_lineEdit")
        self.gridLayout_15.addWidget(self.group1_Device2_Mac0_lineEdit, 0, 1, 1, 1)
        self.group1_Device2_Mac4_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_15)
        self.group1_Device2_Mac4_lineEdit.setObjectName("group1_Device2_Mac4_lineEdit")
        self.gridLayout_15.addWidget(self.group1_Device2_Mac4_lineEdit, 0, 5, 1, 1)
        self.group1_Device2_Mac5_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_15)
        self.group1_Device2_Mac5_lineEdit.setObjectName("group1_Device2_Mac5_lineEdit")
        self.gridLayout_15.addWidget(self.group1_Device2_Mac5_lineEdit, 0, 6, 1, 1)
        self.group1_Device2_Mac1_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_15)
        self.group1_Device2_Mac1_lineEdit.setObjectName("group1_Device2_Mac1_lineEdit")
        self.gridLayout_15.addWidget(self.group1_Device2_Mac1_lineEdit, 0, 2, 1, 1)
        self.group1_Device2_Mac3_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_15)
        self.group1_Device2_Mac3_lineEdit.setObjectName("group1_Device2_Mac3_lineEdit")
        self.gridLayout_15.addWidget(self.group1_Device2_Mac3_lineEdit, 0, 4, 1, 1)
        self.group1_Device2_Channel_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_15)
        self.group1_Device2_Channel_LineEdit.setObjectName("group1_Device2_Channel_LineEdit")
        self.gridLayout_15.addWidget(self.group1_Device2_Channel_LineEdit, 0, 10, 1, 1)
        self.frame_21 = QtWidgets.QFrame(self.gridLayoutWidget_15)
        self.frame_21.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_21.setObjectName("frame_21")
        self.gridLayout_15.addWidget(self.frame_21, 0, 9, 1, 1)
        self.frame_22 = QtWidgets.QFrame(self.gridLayoutWidget_15)
        self.frame_22.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_22.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_22.setObjectName("frame_22")
        self.gridLayout_15.addWidget(self.frame_22, 0, 7, 1, 1)
        self.frame_44 = QtWidgets.QFrame(self.gridLayoutWidget_15)
        self.frame_44.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_44.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_44.setObjectName("frame_44")
        self.gridLayout_15.addWidget(self.frame_44, 0, 11, 1, 1)
        self.group1_Device2_Vol_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_15)
        self.group1_Device2_Vol_LineEdit.setObjectName("group1_Device2_Vol_LineEdit")
        self.gridLayout_15.addWidget(self.group1_Device2_Vol_LineEdit, 0, 12, 1, 1)
        self.gridLayoutWidget_16 = QtWidgets.QWidget(self.groupBox_2)
        self.gridLayoutWidget_16.setGeometry(QtCore.QRect(10, 332, 526, 31))
        self.gridLayoutWidget_16.setObjectName("gridLayoutWidget_16")
        self.gridLayout_16 = QtWidgets.QGridLayout(self.gridLayoutWidget_16)
        self.gridLayout_16.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.group1_Device3_Mac2_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_16)
        self.group1_Device3_Mac2_lineEdit.setObjectName("group1_Device3_Mac2_lineEdit")
        self.gridLayout_16.addWidget(self.group1_Device3_Mac2_lineEdit, 0, 3, 1, 1)
        self.group1_Device3_Role_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_16)
        self.group1_Device3_Role_LineEdit.setObjectName("group1_Device3_Role_LineEdit")
        self.gridLayout_16.addWidget(self.group1_Device3_Role_LineEdit, 0, 8, 1, 1)
        self.group1_Device3_CheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget_16)
        self.group1_Device3_CheckBox.setObjectName("group1_Device3_CheckBox")
        self.gridLayout_16.addWidget(self.group1_Device3_CheckBox, 0, 0, 1, 1)
        self.group1_Device3_Mac0_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_16)
        self.group1_Device3_Mac0_lineEdit.setObjectName("group1_Device3_Mac0_lineEdit")
        self.gridLayout_16.addWidget(self.group1_Device3_Mac0_lineEdit, 0, 1, 1, 1)
        self.group1_Device3_Mac4_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_16)
        self.group1_Device3_Mac4_lineEdit.setObjectName("group1_Device3_Mac4_lineEdit")
        self.gridLayout_16.addWidget(self.group1_Device3_Mac4_lineEdit, 0, 5, 1, 1)
        self.group1_Device3_Mac5_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_16)
        self.group1_Device3_Mac5_lineEdit.setObjectName("group1_Device3_Mac5_lineEdit")
        self.gridLayout_16.addWidget(self.group1_Device3_Mac5_lineEdit, 0, 6, 1, 1)
        self.group1_Device3_Mac1_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_16)
        self.group1_Device3_Mac1_lineEdit.setObjectName("group1_Device3_Mac1_lineEdit")
        self.gridLayout_16.addWidget(self.group1_Device3_Mac1_lineEdit, 0, 2, 1, 1)
        self.group1_Device3_Mac3_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_16)
        self.group1_Device3_Mac3_lineEdit.setObjectName("group1_Device3_Mac3_lineEdit")
        self.gridLayout_16.addWidget(self.group1_Device3_Mac3_lineEdit, 0, 4, 1, 1)
        self.group1_Device3_Channel_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_16)
        self.group1_Device3_Channel_LineEdit.setObjectName("group1_Device3_Channel_LineEdit")
        self.gridLayout_16.addWidget(self.group1_Device3_Channel_LineEdit, 0, 10, 1, 1)
        self.frame_23 = QtWidgets.QFrame(self.gridLayoutWidget_16)
        self.frame_23.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_23.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_23.setObjectName("frame_23")
        self.gridLayout_16.addWidget(self.frame_23, 0, 9, 1, 1)
        self.frame_24 = QtWidgets.QFrame(self.gridLayoutWidget_16)
        self.frame_24.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_24.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_24.setObjectName("frame_24")
        self.gridLayout_16.addWidget(self.frame_24, 0, 7, 1, 1)
        self.frame_37 = QtWidgets.QFrame(self.gridLayoutWidget_16)
        self.frame_37.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_37.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_37.setObjectName("frame_37")
        self.gridLayout_16.addWidget(self.frame_37, 0, 11, 1, 1)
        self.group1_Device3_Vol_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_16)
        self.group1_Device3_Vol_LineEdit.setObjectName("group1_Device3_Vol_LineEdit")
        self.gridLayout_16.addWidget(self.group1_Device3_Vol_LineEdit, 0, 12, 1, 1)
        self.gridLayoutWidget_17 = QtWidgets.QWidget(self.groupBox_2)
        self.gridLayoutWidget_17.setGeometry(QtCore.QRect(10, 372, 526, 31))
        self.gridLayoutWidget_17.setObjectName("gridLayoutWidget_17")
        self.gridLayout_17 = QtWidgets.QGridLayout(self.gridLayoutWidget_17)
        self.gridLayout_17.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.group1_Device4_Mac2_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_17)
        self.group1_Device4_Mac2_lineEdit.setObjectName("group1_Device4_Mac2_lineEdit")
        self.gridLayout_17.addWidget(self.group1_Device4_Mac2_lineEdit, 0, 3, 1, 1)
        self.group1_Device4_Role_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_17)
        self.group1_Device4_Role_LineEdit.setObjectName("group1_Device4_Role_LineEdit")
        self.gridLayout_17.addWidget(self.group1_Device4_Role_LineEdit, 0, 8, 1, 1)
        self.group1_Device4_CheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget_17)
        self.group1_Device4_CheckBox.setObjectName("group1_Device4_CheckBox")
        self.gridLayout_17.addWidget(self.group1_Device4_CheckBox, 0, 0, 1, 1)
        self.group1_Device4_Mac0_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_17)
        self.group1_Device4_Mac0_lineEdit.setObjectName("group1_Device4_Mac0_lineEdit")
        self.gridLayout_17.addWidget(self.group1_Device4_Mac0_lineEdit, 0, 1, 1, 1)
        self.group1_Device4_Mac4_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_17)
        self.group1_Device4_Mac4_lineEdit.setObjectName("group1_Device4_Mac4_lineEdit")
        self.gridLayout_17.addWidget(self.group1_Device4_Mac4_lineEdit, 0, 5, 1, 1)
        self.group1_Device4_Mac5_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_17)
        self.group1_Device4_Mac5_lineEdit.setObjectName("group1_Device4_Mac5_lineEdit")
        self.gridLayout_17.addWidget(self.group1_Device4_Mac5_lineEdit, 0, 6, 1, 1)
        self.group1_Device4_Mac1_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_17)
        self.group1_Device4_Mac1_lineEdit.setObjectName("group1_Device4_Mac1_lineEdit")
        self.gridLayout_17.addWidget(self.group1_Device4_Mac1_lineEdit, 0, 2, 1, 1)
        self.group1_Device4_Mac3_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_17)
        self.group1_Device4_Mac3_lineEdit.setObjectName("group1_Device4_Mac3_lineEdit")
        self.gridLayout_17.addWidget(self.group1_Device4_Mac3_lineEdit, 0, 4, 1, 1)
        self.group1_Device4_Channel_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_17)
        self.group1_Device4_Channel_LineEdit.setObjectName("group1_Device4_Channel_LineEdit")
        self.gridLayout_17.addWidget(self.group1_Device4_Channel_LineEdit, 0, 10, 1, 1)
        self.frame_25 = QtWidgets.QFrame(self.gridLayoutWidget_17)
        self.frame_25.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_25.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_25.setObjectName("frame_25")
        self.gridLayout_17.addWidget(self.frame_25, 0, 9, 1, 1)
        self.frame_26 = QtWidgets.QFrame(self.gridLayoutWidget_17)
        self.frame_26.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_26.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_26.setObjectName("frame_26")
        self.gridLayout_17.addWidget(self.frame_26, 0, 7, 1, 1)
        self.frame_46 = QtWidgets.QFrame(self.gridLayoutWidget_17)
        self.frame_46.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_46.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_46.setObjectName("frame_46")
        self.gridLayout_17.addWidget(self.frame_46, 0, 11, 1, 1)
        self.group1_Device4_Vol_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_17)
        self.group1_Device4_Vol_LineEdit.setObjectName("group1_Device4_Vol_LineEdit")
        self.gridLayout_17.addWidget(self.group1_Device4_Vol_LineEdit, 0, 12, 1, 1)
        self.gridLayoutWidget_18 = QtWidgets.QWidget(self.groupBox_2)
        self.gridLayoutWidget_18.setGeometry(QtCore.QRect(10, 410, 526, 31))
        self.gridLayoutWidget_18.setObjectName("gridLayoutWidget_18")
        self.gridLayout_18 = QtWidgets.QGridLayout(self.gridLayoutWidget_18)
        self.gridLayout_18.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.group1_Device5_Mac2_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_18)
        self.group1_Device5_Mac2_lineEdit.setObjectName("group1_Device5_Mac2_lineEdit")
        self.gridLayout_18.addWidget(self.group1_Device5_Mac2_lineEdit, 0, 3, 1, 1)
        self.group1_Device5_Role_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_18)
        self.group1_Device5_Role_LineEdit.setObjectName("group1_Device5_Role_LineEdit")
        self.gridLayout_18.addWidget(self.group1_Device5_Role_LineEdit, 0, 8, 1, 1)
        self.group1_Device5_CheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget_18)
        self.group1_Device5_CheckBox.setObjectName("group1_Device5_CheckBox")
        self.gridLayout_18.addWidget(self.group1_Device5_CheckBox, 0, 0, 1, 1)
        self.group1_Device5_Mac0_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_18)
        self.group1_Device5_Mac0_lineEdit.setObjectName("group1_Device5_Mac0_lineEdit")
        self.gridLayout_18.addWidget(self.group1_Device5_Mac0_lineEdit, 0, 1, 1, 1)
        self.group1_Device5_Mac4_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_18)
        self.group1_Device5_Mac4_lineEdit.setObjectName("group1_Device5_Mac4_lineEdit")
        self.gridLayout_18.addWidget(self.group1_Device5_Mac4_lineEdit, 0, 5, 1, 1)
        self.group1_Device5_Mac5_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_18)
        self.group1_Device5_Mac5_lineEdit.setObjectName("group1_Device5_Mac5_lineEdit")
        self.gridLayout_18.addWidget(self.group1_Device5_Mac5_lineEdit, 0, 6, 1, 1)
        self.group1_Device5_Mac1_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_18)
        self.group1_Device5_Mac1_lineEdit.setObjectName("group1_Device5_Mac1_lineEdit")
        self.gridLayout_18.addWidget(self.group1_Device5_Mac1_lineEdit, 0, 2, 1, 1)
        self.group1_Device5_Mac3_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_18)
        self.group1_Device5_Mac3_lineEdit.setObjectName("group1_Device5_Mac3_lineEdit")
        self.gridLayout_18.addWidget(self.group1_Device5_Mac3_lineEdit, 0, 4, 1, 1)
        self.group1_Device5_Channel_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_18)
        self.group1_Device5_Channel_LineEdit.setObjectName("group1_Device5_Channel_LineEdit")
        self.gridLayout_18.addWidget(self.group1_Device5_Channel_LineEdit, 0, 10, 1, 1)
        self.frame_27 = QtWidgets.QFrame(self.gridLayoutWidget_18)
        self.frame_27.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_27.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_27.setObjectName("frame_27")
        self.gridLayout_18.addWidget(self.frame_27, 0, 9, 1, 1)
        self.frame_28 = QtWidgets.QFrame(self.gridLayoutWidget_18)
        self.frame_28.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_28.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_28.setObjectName("frame_28")
        self.gridLayout_18.addWidget(self.frame_28, 0, 7, 1, 1)
        self.frame_47 = QtWidgets.QFrame(self.gridLayoutWidget_18)
        self.frame_47.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_47.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_47.setObjectName("frame_47")
        self.gridLayout_18.addWidget(self.frame_47, 0, 11, 1, 1)
        self.group1_Device5_Vol_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_18)
        self.group1_Device5_Vol_LineEdit.setObjectName("group1_Device5_Vol_LineEdit")
        self.gridLayout_18.addWidget(self.group1_Device5_Vol_LineEdit, 0, 12, 1, 1)
        self.gridLayoutWidget_19 = QtWidgets.QWidget(self.groupBox_2)
        self.gridLayoutWidget_19.setGeometry(QtCore.QRect(10, 450, 526, 31))
        self.gridLayoutWidget_19.setObjectName("gridLayoutWidget_19")
        self.gridLayout_19 = QtWidgets.QGridLayout(self.gridLayoutWidget_19)
        self.gridLayout_19.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.group1_Device6_CheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget_19)
        self.group1_Device6_CheckBox.setObjectName("group1_Device6_CheckBox")
        self.gridLayout_19.addWidget(self.group1_Device6_CheckBox, 0, 0, 1, 1)
        self.group1_Device6_Mac0_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_19)
        self.group1_Device6_Mac0_lineEdit.setObjectName("group1_Device6_Mac0_lineEdit")
        self.gridLayout_19.addWidget(self.group1_Device6_Mac0_lineEdit, 0, 1, 1, 1)
        self.group1_Device6_Mac4_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_19)
        self.group1_Device6_Mac4_lineEdit.setObjectName("group1_Device6_Mac4_lineEdit")
        self.gridLayout_19.addWidget(self.group1_Device6_Mac4_lineEdit, 0, 5, 1, 1)
        self.group1_Device6_Mac5_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_19)
        self.group1_Device6_Mac5_lineEdit.setObjectName("group1_Device6_Mac5_lineEdit")
        self.gridLayout_19.addWidget(self.group1_Device6_Mac5_lineEdit, 0, 6, 1, 1)
        self.group1_Device6_Mac1_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_19)
        self.group1_Device6_Mac1_lineEdit.setObjectName("group1_Device6_Mac1_lineEdit")
        self.gridLayout_19.addWidget(self.group1_Device6_Mac1_lineEdit, 0, 2, 1, 1)
        self.group1_Device6_Mac3_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_19)
        self.group1_Device6_Mac3_lineEdit.setObjectName("group1_Device6_Mac3_lineEdit")
        self.gridLayout_19.addWidget(self.group1_Device6_Mac3_lineEdit, 0, 4, 1, 1)
        self.group1_Device6_Channel_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_19)
        self.group1_Device6_Channel_LineEdit.setObjectName("group1_Device6_Channel_LineEdit")
        self.gridLayout_19.addWidget(self.group1_Device6_Channel_LineEdit, 0, 10, 1, 1)
        self.group1_Device6_Mac2_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_19)
        self.group1_Device6_Mac2_lineEdit.setObjectName("group1_Device6_Mac2_lineEdit")
        self.gridLayout_19.addWidget(self.group1_Device6_Mac2_lineEdit, 0, 3, 1, 1)
        self.group1_Device6_Role_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_19)
        self.group1_Device6_Role_LineEdit.setObjectName("group1_Device6_Role_LineEdit")
        self.gridLayout_19.addWidget(self.group1_Device6_Role_LineEdit, 0, 8, 1, 1)
        self.frame_29 = QtWidgets.QFrame(self.gridLayoutWidget_19)
        self.frame_29.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_29.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_29.setObjectName("frame_29")
        self.gridLayout_19.addWidget(self.frame_29, 0, 9, 1, 1)
        self.frame_30 = QtWidgets.QFrame(self.gridLayoutWidget_19)
        self.frame_30.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_30.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_30.setObjectName("frame_30")
        self.gridLayout_19.addWidget(self.frame_30, 0, 7, 1, 1)
        self.frame_48 = QtWidgets.QFrame(self.gridLayoutWidget_19)
        self.frame_48.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_48.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_48.setObjectName("frame_48")
        self.gridLayout_19.addWidget(self.frame_48, 0, 11, 1, 1)
        self.group1_Device6_Vol_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_19)
        self.group1_Device6_Vol_LineEdit.setObjectName("group1_Device6_Vol_LineEdit")
        self.gridLayout_19.addWidget(self.group1_Device6_Vol_LineEdit, 0, 12, 1, 1)
        self.gridLayoutWidget_20 = QtWidgets.QWidget(self.groupBox_2)
        self.gridLayoutWidget_20.setGeometry(QtCore.QRect(10, 490, 526, 31))
        self.gridLayoutWidget_20.setObjectName("gridLayoutWidget_20")
        self.gridLayout_20 = QtWidgets.QGridLayout(self.gridLayoutWidget_20)
        self.gridLayout_20.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.group1_Device7_Mac2_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_20)
        self.group1_Device7_Mac2_lineEdit.setObjectName("group1_Device7_Mac2_lineEdit")
        self.gridLayout_20.addWidget(self.group1_Device7_Mac2_lineEdit, 0, 3, 1, 1)
        self.group1_Device7_Role_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_20)
        self.group1_Device7_Role_LineEdit.setObjectName("group1_Device7_Role_LineEdit")
        self.gridLayout_20.addWidget(self.group1_Device7_Role_LineEdit, 0, 8, 1, 1)
        self.group1_Device7_CheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget_20)
        self.group1_Device7_CheckBox.setObjectName("group1_Device7_CheckBox")
        self.gridLayout_20.addWidget(self.group1_Device7_CheckBox, 0, 0, 1, 1)
        self.group1_Device7_Mac0_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_20)
        self.group1_Device7_Mac0_lineEdit.setObjectName("group1_Device7_Mac0_lineEdit")
        self.gridLayout_20.addWidget(self.group1_Device7_Mac0_lineEdit, 0, 1, 1, 1)
        self.group1_Device7_Mac4_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_20)
        self.group1_Device7_Mac4_lineEdit.setObjectName("group1_Device7_Mac4_lineEdit")
        self.gridLayout_20.addWidget(self.group1_Device7_Mac4_lineEdit, 0, 5, 1, 1)
        self.group1_Device7_Mac5_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_20)
        self.group1_Device7_Mac5_lineEdit.setObjectName("group1_Device7_Mac5_lineEdit")
        self.gridLayout_20.addWidget(self.group1_Device7_Mac5_lineEdit, 0, 6, 1, 1)
        self.group1_Device7_Mac1_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_20)
        self.group1_Device7_Mac1_lineEdit.setObjectName("group1_Device7_Mac1_lineEdit")
        self.gridLayout_20.addWidget(self.group1_Device7_Mac1_lineEdit, 0, 2, 1, 1)
        self.group1_Device7_Mac3_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_20)
        self.group1_Device7_Mac3_lineEdit.setObjectName("group1_Device7_Mac3_lineEdit")
        self.gridLayout_20.addWidget(self.group1_Device7_Mac3_lineEdit, 0, 4, 1, 1)
        self.group1_Device7_Channel_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_20)
        self.group1_Device7_Channel_LineEdit.setObjectName("group1_Device7_Channel_LineEdit")
        self.gridLayout_20.addWidget(self.group1_Device7_Channel_LineEdit, 0, 10, 1, 1)
        self.frame_31 = QtWidgets.QFrame(self.gridLayoutWidget_20)
        self.frame_31.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_31.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_31.setObjectName("frame_31")
        self.gridLayout_20.addWidget(self.frame_31, 0, 9, 1, 1)
        self.frame_32 = QtWidgets.QFrame(self.gridLayoutWidget_20)
        self.frame_32.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_32.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_32.setObjectName("frame_32")
        self.gridLayout_20.addWidget(self.frame_32, 0, 7, 1, 1)
        self.frame_45 = QtWidgets.QFrame(self.gridLayoutWidget_20)
        self.frame_45.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_45.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_45.setObjectName("frame_45")
        self.gridLayout_20.addWidget(self.frame_45, 0, 11, 1, 1)
        self.group1_Device7_Vol_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_20)
        self.group1_Device7_Vol_LineEdit.setObjectName("group1_Device7_Vol_LineEdit")
        self.gridLayout_20.addWidget(self.group1_Device7_Vol_LineEdit, 0, 12, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        self.label_12.setGeometry(QtCore.QRect(380, 190, 31, 16))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.groupBox_2)
        self.label_13.setGeometry(QtCore.QRect(503, 190, 31, 16))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.groupBox_2)
        self.label_14.setGeometry(QtCore.QRect(431, 191, 51, 16))
        self.label_14.setObjectName("label_14")
        self.gridLayoutWidget_32 = QtWidgets.QWidget(self.groupBox_2)
        self.gridLayoutWidget_32.setGeometry(QtCore.QRect(10, 530, 526, 31))
        self.gridLayoutWidget_32.setObjectName("gridLayoutWidget_32")
        self.gridLayout_32 = QtWidgets.QGridLayout(self.gridLayoutWidget_32)
        self.gridLayout_32.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_32.setObjectName("gridLayout_32")
        self.group1_Device8_Mac2_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_32)
        self.group1_Device8_Mac2_lineEdit.setObjectName("group1_Device8_Mac2_lineEdit")
        self.gridLayout_32.addWidget(self.group1_Device8_Mac2_lineEdit, 0, 3, 1, 1)
        self.group1_Device8_Role_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_32)
        self.group1_Device8_Role_LineEdit.setObjectName("group1_Device8_Role_LineEdit")
        self.gridLayout_32.addWidget(self.group1_Device8_Role_LineEdit, 0, 8, 1, 1)
        self.group1_Device8_CheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget_32)
        self.group1_Device8_CheckBox.setObjectName("group1_Device8_CheckBox")
        self.gridLayout_32.addWidget(self.group1_Device8_CheckBox, 0, 0, 1, 1)
        self.group1_Device8_Mac0_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_32)
        self.group1_Device8_Mac0_lineEdit.setObjectName("group1_Device8_Mac0_lineEdit")
        self.gridLayout_32.addWidget(self.group1_Device8_Mac0_lineEdit, 0, 1, 1, 1)
        self.group1_Device8_Mac4_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_32)
        self.group1_Device8_Mac4_lineEdit.setObjectName("group1_Device8_Mac4_lineEdit")
        self.gridLayout_32.addWidget(self.group1_Device8_Mac4_lineEdit, 0, 5, 1, 1)
        self.group1_Device8_Mac5_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_32)
        self.group1_Device8_Mac5_lineEdit.setObjectName("group1_Device8_Mac5_lineEdit")
        self.gridLayout_32.addWidget(self.group1_Device8_Mac5_lineEdit, 0, 6, 1, 1)
        self.group1_Device8_Mac1_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_32)
        self.group1_Device8_Mac1_lineEdit.setObjectName("group1_Device8_Mac1_lineEdit")
        self.gridLayout_32.addWidget(self.group1_Device8_Mac1_lineEdit, 0, 2, 1, 1)
        self.group1_Device8_Mac3_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_32)
        self.group1_Device8_Mac3_lineEdit.setObjectName("group1_Device8_Mac3_lineEdit")
        self.gridLayout_32.addWidget(self.group1_Device8_Mac3_lineEdit, 0, 4, 1, 1)
        self.group1_Device8_Channel_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_32)
        self.group1_Device8_Channel_LineEdit.setObjectName("group1_Device8_Channel_LineEdit")
        self.gridLayout_32.addWidget(self.group1_Device8_Channel_LineEdit, 0, 10, 1, 1)
        self.frame_76 = QtWidgets.QFrame(self.gridLayoutWidget_32)
        self.frame_76.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_76.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_76.setObjectName("frame_76")
        self.gridLayout_32.addWidget(self.frame_76, 0, 9, 1, 1)
        self.frame_77 = QtWidgets.QFrame(self.gridLayoutWidget_32)
        self.frame_77.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_77.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_77.setObjectName("frame_77")
        self.gridLayout_32.addWidget(self.frame_77, 0, 7, 1, 1)
        self.frame_78 = QtWidgets.QFrame(self.gridLayoutWidget_32)
        self.frame_78.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_78.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_78.setObjectName("frame_78")
        self.gridLayout_32.addWidget(self.frame_78, 0, 11, 1, 1)
        self.group1_Device8_Vol_LineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget_32)
        self.group1_Device8_Vol_LineEdit.setObjectName("group1_Device8_Vol_LineEdit")
        self.gridLayout_32.addWidget(self.group1_Device8_Vol_LineEdit, 0, 12, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.groupBox_2)
        self.label_18.setGeometry(QtCore.QRect(487, 130, 61, 20))
        self.label_18.setObjectName("label_18")
        self.group1_groupVolume_LineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.group1_groupVolume_LineEdit.setGeometry(QtCore.QRect(490, 150, 51, 20))
        self.group1_groupVolume_LineEdit.setObjectName("group1_groupVolume_LineEdit")
        self.setGroupInfo_Button = QtWidgets.QPushButton(self.centralwidget)
        self.setGroupInfo_Button.setGeometry(QtCore.QRect(160, 60, 141, 51))
        self.setGroupInfo_Button.setObjectName("setGroupInfo_Button")
        self.activation_Button = QtWidgets.QPushButton(self.centralwidget)
        self.activation_Button.setGeometry(QtCore.QRect(730, 70, 81, 51))
        self.activation_Button.setObjectName("activation_Button")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(640, 70, 81, 51))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.group0_Radio = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.group0_Radio.setObjectName("group0_Radio")
        self.verticalLayout.addWidget(self.group0_Radio)
        self.group1_Radio = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.group1_Radio.setObjectName("group1_Radio")
        self.verticalLayout.addWidget(self.group1_Radio)
        self.deactivation_Button = QtWidgets.QPushButton(self.centralwidget)
        self.deactivation_Button.setGeometry(QtCore.QRect(820, 70, 81, 51))
        self.deactivation_Button.setObjectName("deactivation_Button")
        self.mute_Button = QtWidgets.QPushButton(self.centralwidget)
        self.mute_Button.setGeometry(QtCore.QRect(915, 95, 60, 31))
        self.mute_Button.setObjectName("mute_Button")
        self.unmute_Button = QtWidgets.QPushButton(self.centralwidget)
        self.unmute_Button.setGeometry(QtCore.QRect(975, 95, 60, 31))
        self.unmute_Button.setObjectName("unmute_Button")
        self.getVolume_Button = QtWidgets.QPushButton(self.centralwidget)
        self.getVolume_Button.setGeometry(QtCore.QRect(1062, 65, 111, 31))
        self.getVolume_Button.setObjectName("getVolume_Button")
        self.up_Button = QtWidgets.QPushButton(self.centralwidget)
        self.up_Button.setGeometry(QtCore.QRect(1180, 64, 51, 31))
        self.up_Button.setObjectName("up_Button")
        self.down_Button = QtWidgets.QPushButton(self.centralwidget)
        self.down_Button.setGeometry(QtCore.QRect(1180, 100, 51, 31))
        self.down_Button.setObjectName("down_Button")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(1059, 21, 81, 16))
        self.label_7.setObjectName("label_7")
        self.deviceIndex_LineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.deviceIndex_LineEdit.setGeometry(QtCore.QRect(1065, 40, 71, 20))
        self.deviceIndex_LineEdit.setObjectName("deviceIndex_LineEdit")
        self.setAbsVolume_Button = QtWidgets.QPushButton(self.centralwidget)
        self.setAbsVolume_Button.setGeometry(QtCore.QRect(1062, 100, 111, 31))
        self.setAbsVolume_Button.setObjectName("setAbsVolume_Button")
        self.volume_LineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.volume_LineEdit.setGeometry(QtCore.QRect(1150, 40, 71, 20))
        self.volume_LineEdit.setObjectName("volume_LineEdit")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(1162, 21, 51, 16))
        self.label_8.setObjectName("label_8")
        self.play_Button = QtWidgets.QPushButton(self.centralwidget)
        self.play_Button.setGeometry(QtCore.QRect(915, 62, 60, 31))
        self.play_Button.setObjectName("play_Button")
        self.pause_Button = QtWidgets.QPushButton(self.centralwidget)
        self.pause_Button.setGeometry(QtCore.QRect(975, 62, 60, 31))
        self.pause_Button.setObjectName("pause_Button")
        self.log_TextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.log_TextBrowser.setGeometry(QtCore.QRect(10, 720, 1151, 181))
        self.log_TextBrowser.setObjectName("log_TextBrowser")
        self.ssid_LineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.ssid_LineEdit.setGeometry(QtCore.QRect(730, 10, 171, 20))
        self.ssid_LineEdit.setObjectName("ssid_LineEdit")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(700, 14, 31, 16))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(680, 40, 51, 20))
        self.label_16.setObjectName("label_16")
        self.passwd_LineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.passwd_LineEdit.setGeometry(QtCore.QRect(730, 40, 171, 20))
        self.passwd_LineEdit.setObjectName("passwd_LineEdit")
        MainWindow.setCentralWidget(self.centralwidget)

        self.main_window = MainWindow
        self.menubar1 = MainWindow.menuBar()
        fileMenu = self.menubar1.addMenu('File')
        loadAct = QAction('&Load Config', self)
        loadAct.setShortcut('Ctrl+L')
        loadAct.setStatusTip('Load WoWPlay Group Config!!')
        loadAct.triggered.connect(self.loadFile)
        fileMenu.addAction(loadAct)

        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.exit)
        fileMenu.addAction(exitAct)

        #self.menubar = QtWidgets.QMenuBar(MainWindow)
        #self.menubar.setGeometry(QtCore.QRect(0, 0, 1244, 21))
        #self.menubar.setObjectName("menubar")
        #MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)



        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.group_ui_list = [
            {
                'check_box' : self.group0_CheckBox,
                'group_name' : self.group0_Name_LineEdit,
                'device_list' : [
                    {"check": self.group0_Device0_CheckBox,
                     "mac_addr": [self.group0_Device0_Mac0_lineEdit, self.group0_Device0_Mac1_lineEdit,
                                  self.group0_Device0_Mac2_lineEdit,
                                  self.group0_Device0_Mac3_lineEdit, self.group0_Device0_Mac4_lineEdit,
                                  self.group0_Device0_Mac5_lineEdit],
                     "role": self.group0_Device0_Role_LineEdit,
                     "channel": self.group0_Device0_Channel_LineEdit,
                     "volume": self.group0_Device0_Vol_LineEdit},
                    {"check": self.group0_Device1_CheckBox,
                     "mac_addr": [self.group0_Device1_Mac0_lineEdit, self.group0_Device1_Mac1_lineEdit,
                                  self.group0_Device1_Mac2_lineEdit,
                                  self.group0_Device1_Mac3_lineEdit, self.group0_Device1_Mac4_lineEdit,
                                  self.group0_Device1_Mac5_lineEdit],
                     "role": self.group0_Device1_Role_LineEdit,
                     "channel": self.group0_Device1_Channel_LineEdit,
                     "volume": self.group0_Device1_Vol_LineEdit},
                    {"check": self.group0_Device2_CheckBox,
                     "mac_addr": [self.group0_Device2_Mac0_lineEdit, self.group0_Device2_Mac1_lineEdit,
                                  self.group0_Device2_Mac2_lineEdit,
                                  self.group0_Device2_Mac3_lineEdit, self.group0_Device2_Mac4_lineEdit,
                                  self.group0_Device2_Mac5_lineEdit],
                     "role": self.group0_Device2_Role_LineEdit,
                     "channel": self.group0_Device2_Channel_LineEdit,
                     "volume": self.group0_Device2_Vol_LineEdit},
                    {"check": self.group0_Device3_CheckBox,
                     "mac_addr": [self.group0_Device3_Mac0_lineEdit, self.group0_Device3_Mac1_lineEdit,
                                  self.group0_Device3_Mac2_lineEdit,
                                  self.group0_Device3_Mac3_lineEdit, self.group0_Device3_Mac4_lineEdit,
                                  self.group0_Device3_Mac5_lineEdit],
                     "role": self.group0_Device3_Role_LineEdit,
                     "channel": self.group0_Device3_Channel_LineEdit,
                     "volume": self.group0_Device3_Vol_LineEdit},
                    {"check": self.group0_Device4_CheckBox,
                     "mac_addr": [self.group0_Device4_Mac0_lineEdit, self.group0_Device4_Mac1_lineEdit,
                                  self.group0_Device4_Mac2_lineEdit,
                                  self.group0_Device4_Mac3_lineEdit, self.group0_Device4_Mac4_lineEdit,
                                  self.group0_Device4_Mac5_lineEdit],
                     "role": self.group0_Device4_Role_LineEdit,
                     "channel": self.group0_Device4_Channel_LineEdit,
                     "volume": self.group0_Device4_Vol_LineEdit},
                    {"check": self.group0_Device5_CheckBox,
                     "mac_addr": [self.group0_Device5_Mac0_lineEdit, self.group0_Device5_Mac1_lineEdit,
                                  self.group0_Device5_Mac2_lineEdit,
                                  self.group0_Device5_Mac3_lineEdit, self.group0_Device5_Mac4_lineEdit,
                                  self.group0_Device5_Mac5_lineEdit],
                     "role": self.group0_Device5_Role_LineEdit,
                     "channel": self.group0_Device5_Channel_LineEdit,
                     "volume": self.group0_Device5_Vol_LineEdit},
                    {"check": self.group0_Device6_CheckBox,
                     "mac_addr": [self.group0_Device6_Mac0_lineEdit, self.group0_Device6_Mac1_lineEdit,
                                  self.group0_Device6_Mac2_lineEdit,
                                  self.group0_Device6_Mac3_lineEdit, self.group0_Device6_Mac4_lineEdit,
                                  self.group0_Device6_Mac5_lineEdit],
                     "role": self.group0_Device6_Role_LineEdit,
                     "channel": self.group0_Device6_Channel_LineEdit,
                     "volume": self.group0_Device6_Vol_LineEdit},
                    {"check": self.group0_Device7_CheckBox,
                     "mac_addr": [self.group0_Device7_Mac0_lineEdit, self.group0_Device7_Mac1_lineEdit,
                                  self.group0_Device7_Mac2_lineEdit,
                                  self.group0_Device7_Mac3_lineEdit, self.group0_Device7_Mac4_lineEdit,
                                  self.group0_Device7_Mac5_lineEdit],
                     "role": self.group0_Device7_Role_LineEdit,
                     "channel": self.group0_Device7_Channel_LineEdit,
                     "volume": self.group0_Device7_Vol_LineEdit},
                    {"check": self.group0_Device8_CheckBox,
                     "mac_addr": [self.group0_Device8_Mac0_lineEdit, self.group0_Device8_Mac1_lineEdit,
                                  self.group0_Device8_Mac2_lineEdit,
                                  self.group0_Device8_Mac3_lineEdit, self.group0_Device8_Mac4_lineEdit,
                                  self.group0_Device8_Mac5_lineEdit],
                     "role": self.group0_Device8_Role_LineEdit,
                     "channel": self.group0_Device8_Channel_LineEdit,
                     "volume": self.group0_Device8_Vol_LineEdit}
                ],
                "channel_list" : {
                    "Mono": self.group0_Mono_Radio,
                    "Stereo": self.group0_Stereo_Radio,
                    "3.1.2": self.group0_312_Radio,
                    "5.1": self.group0_51_Radio,
                    "5.1.2": self.group0_512_Radio,
                    "7.1": self.group0_71_Radio,
                    "7.1.2": self.group0_712_Radio,
                    "7.1.4": self.group0_714_Radio
                },
                "topology_list" : {
                    "Multi-Channel": self.group0_MultiCh_Radio,
                    "Multi-Room": self.group0_MultiRo_Radio,
                    "Concurrent": self.group0_Concurr_Radio
                }
            },

            {
                'check_box': self.group1_CheckBox,
                'group_name': self.group1_Name_LineEdit,
                'device_list': [
                    {"check": self.group1_Device0_CheckBox,
                     "mac_addr": [self.group1_Device0_Mac0_lineEdit, self.group1_Device0_Mac1_lineEdit,
                                  self.group1_Device0_Mac2_lineEdit,
                                  self.group1_Device0_Mac3_lineEdit, self.group1_Device0_Mac4_lineEdit,
                                  self.group1_Device0_Mac5_lineEdit],
                     "role": self.group1_Device0_Role_LineEdit,
                     "channel": self.group1_Device0_Channel_LineEdit,
                     "volume": self.group1_Device0_Vol_LineEdit},
                    {"check": self.group1_Device1_CheckBox,
                     "mac_addr": [self.group1_Device1_Mac0_lineEdit, self.group1_Device1_Mac1_lineEdit,
                                  self.group1_Device1_Mac2_lineEdit,
                                  self.group1_Device1_Mac3_lineEdit, self.group1_Device1_Mac4_lineEdit,
                                  self.group1_Device1_Mac5_lineEdit],
                     "role": self.group1_Device1_Role_LineEdit,
                     "channel": self.group1_Device1_Channel_LineEdit,
                     "volume": self.group1_Device1_Vol_LineEdit},
                    {"check": self.group1_Device2_CheckBox,
                     "mac_addr": [self.group1_Device2_Mac0_lineEdit, self.group1_Device2_Mac1_lineEdit,
                                  self.group1_Device2_Mac2_lineEdit,
                                  self.group1_Device2_Mac3_lineEdit, self.group1_Device2_Mac4_lineEdit,
                                  self.group1_Device2_Mac5_lineEdit],
                     "role": self.group1_Device2_Role_LineEdit,
                     "channel": self.group1_Device2_Channel_LineEdit,
                     "volume": self.group1_Device2_Vol_LineEdit},
                    {"check": self.group1_Device3_CheckBox,
                     "mac_addr": [self.group1_Device3_Mac0_lineEdit, self.group1_Device3_Mac1_lineEdit,
                                  self.group1_Device3_Mac2_lineEdit,
                                  self.group1_Device3_Mac3_lineEdit, self.group1_Device3_Mac4_lineEdit,
                                  self.group1_Device3_Mac5_lineEdit],
                     "role": self.group1_Device3_Role_LineEdit,
                     "channel": self.group1_Device3_Channel_LineEdit,
                     "volume": self.group1_Device3_Vol_LineEdit},
                    {"check": self.group1_Device4_CheckBox,
                     "mac_addr": [self.group1_Device4_Mac0_lineEdit, self.group1_Device4_Mac1_lineEdit,
                                  self.group1_Device4_Mac2_lineEdit,
                                  self.group1_Device4_Mac3_lineEdit, self.group1_Device4_Mac4_lineEdit,
                                  self.group1_Device4_Mac5_lineEdit],
                     "role": self.group1_Device4_Role_LineEdit,
                     "channel": self.group1_Device4_Channel_LineEdit,
                     "volume": self.group1_Device4_Vol_LineEdit},
                    {"check": self.group1_Device5_CheckBox,
                     "mac_addr": [self.group1_Device5_Mac0_lineEdit, self.group1_Device5_Mac1_lineEdit,
                                  self.group1_Device5_Mac2_lineEdit,
                                  self.group1_Device5_Mac3_lineEdit, self.group1_Device5_Mac4_lineEdit,
                                  self.group1_Device5_Mac5_lineEdit],
                     "role": self.group1_Device5_Role_LineEdit,
                     "channel": self.group1_Device5_Channel_LineEdit,
                     "volume": self.group1_Device5_Vol_LineEdit},
                    {"check": self.group1_Device6_CheckBox,
                     "mac_addr": [self.group1_Device6_Mac0_lineEdit, self.group1_Device6_Mac1_lineEdit,
                                  self.group1_Device6_Mac2_lineEdit,
                                  self.group1_Device6_Mac3_lineEdit, self.group1_Device6_Mac4_lineEdit,
                                  self.group1_Device6_Mac5_lineEdit],
                     "role": self.group1_Device6_Role_LineEdit,
                     "channel": self.group1_Device6_Channel_LineEdit,
                     "volume": self.group1_Device6_Vol_LineEdit},
                    {"check": self.group1_Device7_CheckBox,
                     "mac_addr": [self.group1_Device7_Mac0_lineEdit, self.group1_Device7_Mac1_lineEdit,
                                  self.group1_Device7_Mac2_lineEdit,
                                  self.group1_Device7_Mac3_lineEdit, self.group1_Device7_Mac4_lineEdit,
                                  self.group1_Device7_Mac5_lineEdit],
                     "role": self.group1_Device7_Role_LineEdit,
                     "channel": self.group1_Device7_Channel_LineEdit,
                     "volume": self.group1_Device7_Vol_LineEdit},
                    {"check": self.group1_Device8_CheckBox,
                     "mac_addr": [self.group1_Device8_Mac0_lineEdit, self.group1_Device8_Mac1_lineEdit,
                                  self.group1_Device8_Mac2_lineEdit,
                                  self.group1_Device8_Mac3_lineEdit, self.group1_Device8_Mac4_lineEdit,
                                  self.group1_Device8_Mac5_lineEdit],
                     "role": self.group1_Device8_Role_LineEdit,
                     "channel": self.group1_Device8_Channel_LineEdit,
                     "volume": self.group1_Device8_Vol_LineEdit}
                ],
                "channel_list": {
                    "Mono": self.group1_Mono_Radio,
                    "Stereo": self.group1_Stereo_Radio,
                    "3.1.2": self.group1_312_Radio,
                    "5.1": self.group1_51_Radio,
                    "5.1.2": self.group1_512_Radio,
                    "7.1": self.group1_71_Radio,
                    "7.1.2": self.group1_712_Radio,
                    "7.1.4": self.group1_714_Radio
                },
                "topology_list": {
                    "Multi-Channel": self.group1_MultiCh_Radio,
                    "Multi-Room": self.group1_MultiRo_Radio,
                    "Concurrent": self.group1_Concurr_Radio
                }
            }
        ]

    def loadFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self.main_window,"QFileDialog.getOpenFileName()", "","JSON Files (*.json)", options=options)
        if fileName:
            self.loadCfg(fileName)

    def exit(self):
        stopPythonServer()
        time.sleep(0.5)
        sys.exit(0)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.setAddr_Button.setText(_translate("MainWindow", "Set Address"))
        self.getGroupInfo_Button.setText(_translate("MainWindow", "Get Group Information"))
        self.groupBox.setTitle(_translate("MainWindow", "Group 0"))
        self.label.setText(_translate("MainWindow", "Channel Confguration"))
        self.group0_Mono_Radio.setText(_translate("MainWindow", "Mono "))
        self.group0_512_Radio.setText(_translate("MainWindow", "5.1.2"))
        self.group0_Stereo_Radio.setText(_translate("MainWindow", "Stereo"))
        self.group0_71_Radio.setText(_translate("MainWindow", "7.1"))
        self.group0_51_Radio.setText(_translate("MainWindow", "5.1"))
        self.group0_312_Radio.setText(_translate("MainWindow", "3.1.2"))
        self.group0_714_Radio.setText(_translate("MainWindow", "7.1.4"))
        self.group0_712_Radio.setText(_translate("MainWindow", "7.1.2"))
        self.group0_Concurr_Radio.setText(_translate("MainWindow", "Concurrent"))
        self.group0_MultiCh_Radio.setText(_translate("MainWindow", "Multi-Channel"))
        self.group0_MultiRo_Radio.setText(_translate("MainWindow", "Multi-Room"))
        self.label_2.setText(_translate("MainWindow", "Topology Confguration"))
        self.label_3.setText(_translate("MainWindow", "Group Name"))
        self.group0_CheckBox.setText(_translate("MainWindow", "Do configuration"))
        self.group0_Device0_CheckBox.setText(_translate("MainWindow", "Device 0"))
        self.group0_Device1_CheckBox.setText(_translate("MainWindow", "Device 1"))
        self.group0_Device2_CheckBox.setText(_translate("MainWindow", "Device 2"))
        self.group0_Device3_CheckBox.setText(_translate("MainWindow", "Device 3"))
        self.group0_Device4_CheckBox.setText(_translate("MainWindow", "Device 4"))
        self.group0_Device5_CheckBox.setText(_translate("MainWindow", "Device 5"))
        self.group0_Device6_CheckBox.setText(_translate("MainWindow", "Device 6"))
        self.group0_Device7_CheckBox.setText(_translate("MainWindow", "Device 7"))
        self.label_9.setText(_translate("MainWindow", "Role"))
        self.label_10.setText(_translate("MainWindow", "Channel"))
        self.label_11.setText(_translate("MainWindow", "Vol."))
        self.group0_Device8_CheckBox.setText(_translate("MainWindow", "Device 8"))
        self.label_17.setText(_translate("MainWindow", "Group Vol"))
        self.textBrowser.setHtml(_translate("MainWindow",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Channel Information</p>\n"
                                            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Front Left: 0x00001</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Front Right: 0x00002</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Front Center: 0x00004</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Low Frequency: 0x00008</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Rear Left: 0x00010</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Rear Right: 0x00020</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Front Left of Center: 0x00040</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Front Right of Center: 0x00080</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">RC: Rear Center: 0x00100</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Side Left: 0x00200</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Side Right: 0x00400</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Top Center: 0x00800</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Top Front Left: 0x01000</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Top Front Center: 0x02000</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Top Front Right: 0x04000</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Top Rear Left: 0x08000</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Top Rear Center: 0x10000</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Top Rear Right: 0x20000</p></body></html>"))
        self.textBrowser_2.setHtml(_translate("MainWindow",
                                              "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                              "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                              "p, li { white-space: pre-wrap; }\n"
                                              "</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                              "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Role Information</p>\n"
                                              "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                              "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Master: 0x00</p>\n"
                                              "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Slave: 0x01</p></body></html>"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Group 1"))
        self.label_4.setText(_translate("MainWindow", "Channel Confguration"))
        self.group1_71_Radio.setText(_translate("MainWindow", "7.1"))
        self.group1_Stereo_Radio.setText(_translate("MainWindow", "Stereo"))
        self.group1_51_Radio.setText(_translate("MainWindow", "5.1"))
        self.group1_712_Radio.setText(_translate("MainWindow", "7.1.2"))
        self.group1_512_Radio.setText(_translate("MainWindow", "5.1.2"))
        self.group1_312_Radio.setText(_translate("MainWindow", "3.1.2"))
        self.group1_Mono_Radio.setText(_translate("MainWindow", "Mono "))
        self.group1_714_Radio.setText(_translate("MainWindow", "7.1.4"))
        self.group1_Concurr_Radio.setText(_translate("MainWindow", "Concurrent"))
        self.group1_MultiCh_Radio.setText(_translate("MainWindow", "Multi-Channel"))
        self.group1_MultiRo_Radio.setText(_translate("MainWindow", "Multi-Room"))
        self.label_5.setText(_translate("MainWindow", "Topology Confguration"))
        self.label_6.setText(_translate("MainWindow", "Group Name"))
        self.group1_CheckBox.setText(_translate("MainWindow", "Do configuration"))
        self.group1_Device0_CheckBox.setText(_translate("MainWindow", "Device 0"))
        self.group1_Device1_CheckBox.setText(_translate("MainWindow", "Device 1"))
        self.group1_Device2_CheckBox.setText(_translate("MainWindow", "Device 2"))
        self.group1_Device3_CheckBox.setText(_translate("MainWindow", "Device 3"))
        self.group1_Device4_CheckBox.setText(_translate("MainWindow", "Device 4"))
        self.group1_Device5_CheckBox.setText(_translate("MainWindow", "Device 5"))
        self.group1_Device6_CheckBox.setText(_translate("MainWindow", "Device 6"))
        self.group1_Device7_CheckBox.setText(_translate("MainWindow", "Device 7"))
        self.label_12.setText(_translate("MainWindow", "Role"))
        self.label_13.setText(_translate("MainWindow", "Vol."))
        self.label_14.setText(_translate("MainWindow", "Channel"))
        self.group1_Device8_CheckBox.setText(_translate("MainWindow", "Device 8"))
        self.label_18.setText(_translate("MainWindow", "Group Vol"))
        self.setGroupInfo_Button.setText(_translate("MainWindow", "Set Group Information"))
        self.activation_Button.setText(_translate("MainWindow", "Activation"))
        self.group0_Radio.setText(_translate("MainWindow", "Group 0"))
        self.group1_Radio.setText(_translate("MainWindow", "Group 1"))
        self.deactivation_Button.setText(_translate("MainWindow", "Deactivation"))
        self.mute_Button.setText(_translate("MainWindow", "Mute"))
        self.unmute_Button.setText(_translate("MainWindow", "UnMute"))
        self.getVolume_Button.setText(_translate("MainWindow", "Get Volume"))
        self.up_Button.setText(_translate("MainWindow", "Up"))
        self.down_Button.setText(_translate("MainWindow", "Down"))
        self.label_7.setText(_translate("MainWindow", "Device Index"))
        self.setAbsVolume_Button.setText(_translate("MainWindow", "Set Abs Volume"))
        self.label_8.setText(_translate("MainWindow", "Volume"))
        self.play_Button.setText(_translate("MainWindow", "Play"))
        self.pause_Button.setText(_translate("MainWindow", "Pause"))
        self.log_TextBrowser.setHtml(_translate("MainWindow",
                                                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                "p, li { white-space: pre-wrap; }\n"
                                                "</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label_15.setText(_translate("MainWindow", "SSID"))
        self.label_16.setText(_translate("MainWindow", "Passwd"))

        self.ssid_LineEdit.setText('WOWPLAY_SM10-3')

        # Event Handler Register
        self.setAddr_Button.clicked.connect(self.setAddrButton_Handler)
        self.getGroupInfo_Button.clicked.connect(self.getGroupInfoButton_Handler)
        self.setGroupInfo_Button.clicked.connect(self.setGroupInfoButton_Handler)
        self.activation_Button.clicked.connect(self.activationButton_Handler)
        self.deactivation_Button.clicked.connect(self.deactivationButton_Handler)
        self.play_Button.clicked.connect(self.playButton_Handler)
        self.pause_Button.clicked.connect(self.pauseButton_Handler)
        self.mute_Button.clicked.connect(self.muteButton_Handler)
        self.unmute_Button.clicked.connect(self.unmuteButton_Handler)
        self.getVolume_Button.clicked.connect(self.getVolumeButton_Handler)
        self.setAbsVolume_Button.clicked.connect(self.setAbsVolumeButton_Handler)
        self.up_Button.clicked.connect(self.upbutton_Handler)
        self.down_Button.clicked.connect(self.downButton_Handler)

        self.Timer.timeout.connect(self.Timeout_Handler)

        self.WoWIF = state_main()



    # Event Handler
    def setAddrButton_Handler(self):
        setAddrButton_Handler_func(self)

    def getGroupInfoButton_Handler(self):
        getGroupInfoButton_Handler_func(self)

    def setGroupInfoButton_Handler(self):
        setGroupInfoButton_Handler_func(self)

    def activationButton_Handler(self):
        activationButton_Handler_func(self)

    def deactivationButton_Handler(self):
        deactivationButton_Handler_func(self)

    def playButton_Handler(self):
        playButton_Handler_func(self)

    def pauseButton_Handler(self):
        pauseButton_Handler_func(self)

    def muteButton_Handler(self):
        muteButton_Handler_func(self)

    def unmuteButton_Handler(self):
        unmuteButton_Handler_func(self)

    def getVolumeButton_Handler(self):
        getVolumeButton_Handler_func(self)

    def setAbsVolumeButton_Handler(self):
        setAbsVolumeButton_Handler_func(self)

    def upbutton_Handler(self):
        upbutton_Handler_func(self)

    def downButton_Handler(self):
        downButton_Handler_func(self)

    def Timeout_Handler(self):
        timeOut_Handler_func(self)

    def loadCfg(self, cfg_file: str):
        if cfg_file is None:
            return

        with open(cfg_file) as json_cfg:
            data = json.load(json_cfg)
            group_info_list = [None, None]
            if 'Group_Info_0' in data:
                group_info_list[0] = data['Group_Info_0']
            if 'Group_Info_1' in data:
                group_info_list[1] = data['Group_Info_1']

            for group_ui in self.group_ui_list :
                group_ui['check_box'].setChecked(False)
                group_ui['group_name'].setText('')

                for channel_radio in group_ui['channel_list'].values():
                    channel_radio.setChecked(False)

                for topology_radio in group_ui['topology_list'].values():
                    topology_radio.setChecked(False)

                for ui in group_ui['device_list'] :
                    ui['check'].setChecked(False)
                    for mac_edit in ui['mac_addr']:
                        mac_edit.setText('')
                    ui['role'].setText('')
                    ui['channel'].setText('')
                    ui['volume'].setText('')

            for group_idx, group_info in enumerate(group_info_list) :
                if group_info is None :
                    continue

                self.group_ui_list[group_idx]['check_box'].setChecked(group_info['Group_Check'] == 1)
                self.group_ui_list[group_idx]['group_name'].setText(group_info['Group_Name'])
                for key in self.group_ui_list[group_idx]['channel_list']:
                    self.group_ui_list[group_idx]['channel_list'][key].setChecked(group_info['Channel_Cfg'] == key)
                for key in self.group_ui_list[group_idx]['topology_list']:
                    self.group_ui_list[group_idx]['topology_list'][key].setChecked(group_info['Topology_Cfg'] == key)

                device_ui_list = self.group_ui_list[group_idx]['device_list']
                for id, dev_info in enumerate(group_info['Devices']):
                    device_ui_list[id]['check'].setChecked(True)
                    mac_addrs = dev_info['Mac Addr'].strip().split(':')
                    for pos in range(len(mac_addrs)):
                        device_ui_list[id]['mac_addr'][pos].setText(mac_addrs[pos])
                    device_ui_list[id]['role'].setText(str(dev_info['Role']))
                    channelBits = sum((1 << data['Channel_Info'][ch]) for ch in dev_info['Channel'].split(":"))
                    device_ui_list[id]['channel'].setText('%X' % channelBits)
                    device_ui_list[id]['volume'].setText(str(dev_info['Volume']))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    #ui.loadCfg('wowplay_group_cfg_01.json')

    sock_init()

    t = threading.Thread(target=pythonServer, args=(ui,))
    t.start()

    sys.exit(app.exec_())

    t.join()

