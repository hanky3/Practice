import sys
import socket
from PyQt5 import QtCore, QtGui, QtWidgets

CH_CFG_TYPE_MONO   = 0x00
CH_CFG_TYPE_STEREO = 0x01
CH_CFG_TYPE_3_1_2  = 0x02
CH_CFG_TYPE_5_1    = 0x03
CH_CFG_TYPE_5_1_2  = 0x04
CH_CFG_TYPE_7_1    = 0x05
CH_CFG_TYPE_7_1_2  = 0x06
CH_CFG_TYPE_7_1_4  = 0x07

# CH_CFG_TYPE to String
CH_CFG_TYPE_TO_STRING = {0x00 : ['Mono','MONO']    , 0x01 : ['Stereo','STEREO'],
						 0x02 : ['312','3.1.2'] , 0x03 : ['51','5.1.0'],
						 0x04 : ['512','5.1.2'] , 0x05 : ['71','7.1.0'],
						 0x06 : ['712','7.1.2'] , 0x07 : ['714','7.1.4'] }

TP_CFG_MULTI_CHANNEL = 0x00
TP_CFG_MULTI_ROOM = 0x01
TP_CFG_CONCURRENT = 0x02

TP_CFG_TYPE_TO_STRING = {0x00 : ['MultiCh','Multi Channel'],
						 0x01 : ['MultiRo','Multi Room'],
						 0x02 : ['Concurr','Concurrent'] }
CH_BITMAP_TO_STRING = {
	0x00001 : 'FL' , # Front Left
	0x00002 : 'FR' , # Front Right
	0x00004 : 'C'  , # Front Center
	0x00008 : 'Wf' , # Low Frequency
	0x00010 : 'RL' , # Rear Left
	0x00020 : 'RR' , # Rear Right
	0x00040 : 'FLC', # Front Left of Center
	0x00080 : 'FRC', # Front Right of Center
	0x00100 : 'RC' , # Rear Center
	0x00200 : 'SL' , # Side Left
	0x00400 : 'SR' , # Side Right
	0x00800 : 'TC' , # Top Center
	0x01000 : 'TFL', # Top Front Left
	0x02000 : 'TFC', # Top Front Center
	0x04000 : 'TFR', # Top Front Right
	0x08000 : 'TRL', # Top Rear Left
	0x10000 : 'TRC', # Top Rear Center
	0x20000 : 'TRR'	 # Top Rear Right
}

CH_BITMAP_TO_CONFIG_CH_NUM = {
	0x00001 : [1,0,0], # Front Left
	0x00002 : [1,0,0], # Front Right
	0x00004 : [1,0,0], # Front Center
	0x00008 : [0,1,0], # Low Frequency
	0x00010 : [1,0,0], # Rear Left
	0x00020 : [1,0,0], # Rear Right
	0x00040 : [1,0,0], # Front Left of Center
	0x00080 : [1,0,0], # Front Right of Center
	0x00100 : [1,0,0], # Rear Center
	0x00200 : [1,0,0], # Side Left
	0x00400 : [1,0,0], # Side Right
	0x00800 : [0,0,1], # Top Center
	0x01000 : [0,0,1], # Top Front Left
	0x02000 : [0,0,1], # Top Front Center
	0x04000 : [0,0,1], # Top Front Right
	0x08000 : [0,0,1], # Top Rear Left
	0x10000 : [0,0,1], # Top Rear Center
	0x20000 : [0,0,1]  # Top Rear Right
}

AUDIO_SAMPLE_ENUM_TO_KHZ = {
	0x01:    8,  #     8,000 Hz
	0x02:   11,  #    11,025 Hz
	0x03:   16,  #    16,000 Hz
	0x04:   22,  #    22,050 Hz
	0x05:   32,  #    32,000 Hz
	0x06:   44,  #    44,056 Hz
	0x07:   44,  #    44,100 Hz
	0x08:   47,  #    47,250 Hz
	0x09:   48,  #    48,000 Hz
	0x0A:   50,  #    50,000 Hz
	0x0B:   50,  #    50,400 Hz
	0x0C:   88,  #    88,200 Hz
	0x0D:   96,  #    96,000 Hz
	0x0E:  176,  #   176,400 Hz
	0x0F:  192,  #   192,000 Hz
	0x10:  352,  #   352,800 Hz
	0x11: 2822,  # 2,822,400 Hz
	0x12: 5644   # 5,644,800 Hz
}

# Data Structures
class S_GROUP_ELEMENT:
	channel = 0
	role = 0
	macAddr = []

class S_GROUP_INFO:
	chCfgType = 0
	tpCfgType = 0
	activated = 0
	groupName = ""
	numSpeaker = 0
	stGroupElement = []

class S_GROUP_TOTAL_INFO:
	lastUpdatedTime = 0
	numGroup = 0
	stGroupInfo = []

class S_GROUP_ACTIVATE_INFO:
	lastUpdatedTime = 0
	groupIdx = 0
	ssid = ""
	passwd = ""

class S_GROUP_VOLUME_INFO:
	groupVolume = 0
	numSpeaker = 0
	volume = []

class S_ABS_VOLUME_INFO:
	speakerIdx = 0
	volume = 0

class S_REL_VOLUME_INFO:
	speakerIdx = 0
	upDown = 0

# Message Definition
SET_CTRL_ADDR = 0x01
GET_GROUP_INFO = 0x02
SET_GROUP_INFO_REQ = 0x03
GROUP_ACTIVATE_REQ = 0x04
GROUP_DEACTIVATE_REQ = 0x05
GROUP_PLAY_REQ = 0x06
GET_GROUP_VOLUME = 0x07
SET_GROUP_ABS_VOLUME_REQ = 0x08
SET_GROUP_REL_VOLUME_REQ = 0x09
SET_GROUP_MUTE_REQ = 0x0A
GET_WIRELESS_INFO = 0x0B
SET_CTRL_ADDR_RET = 0x11
GET_GROUP_INFO_RET = 0x12
GET_GROUP_VOLUME_RET = 0x13
GET_WIRELESS_INFO_RET = 0x14
SET_GROUP_INFO_RSP = 0x21
GROUP_ACTIVATE_RSP = 0x22
GROUP_DEACTIVATE_RSP = 0x23
GROUP_PLAY_RSP = 0x24
SET_GROUP_ABS_VOLUME_RSP = 0x25
SET_GROUP_REL_VOLUME_RSP = 0x26
SET_GROUP_MUTE_RSP = 0x27
VOLUME_CHANGE_IND = 0x31
GROUP_PLAY_IND = 0x32
GROUP_STATUS_IND = 0x33
AUDIO_PLAYBACK_INFO_IND = 0x34
WIFI_CHANNEL_INFO_IND = 0x35
# Const Value
MAX_GROUP_NAME_LEN = 19
MAX_MAC_ADDR_LEN = 6
MAX_SSID_LEN = 19
MAX_PASSWD_LEN = 19
INVALID_IDX = 0xFF

# Socket
BUF_SIZE = 1200
PYTHON_PORT = 44444
CPP_PORT = 55555
CPP_ADDR = "192.168.1.4"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Group Values
gActivateIdx = 0

def setActivateIdx(idx):
	global gActivateIdx
	gActivateIdx = idx

def getActivateIdx():
	global gActivateIdx
	return gActivateIdx

# Set Group Info Context
gMsgParam_SetGroupInfo = []
def updateSetGroupInfo(msg):
	global gMsgParam_SetGroupInfo
	gMsgParam_SetGroupInfo = msg

def getSetGroupInfo():
	global gMsgParam_SetGroupInfo
	return gMsgParam_SetGroupInfo

# Play/Pause State
gMsgParam_PlayPause = 0
def updatePlayPauseInfo(PlayPause):
	global gMsgParam_PlayPause
	gMsgParam_PlayPause = PlayPause

def getPlayPauseInfo():
	global gMsgParam_PlayPause
	return gMsgParam_PlayPause

# Mute/Unmute State
gMsgParam_MuteUnmute = 0
def updateMueteUnmuteInfo(MuteUnmute):
	global gMsgParam_MuteUnmute
	gMsgParam_MuteUnmute = MuteUnmute

def getMuteUnMuteInfo():
	global gMsgParam_MuteUnmute
	return gMsgParam_MuteUnmute