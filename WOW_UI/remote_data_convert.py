import sys
from remote_context import *


def setGroupTotalInfo_to_Vector(groupTotalInfo):
    retVector = bytes()

    retVector += groupTotalInfo.lastUpdatedTime.to_bytes(8, 'little')
    retVector += groupTotalInfo.numGroup.to_bytes(1, 'little')

    groupIdx = 0
    while groupIdx < groupTotalInfo.numGroup:
        retVector += groupTotalInfo.stGroupInfo[groupIdx].chCfgType.to_bytes(1, 'little')
        retVector += groupTotalInfo.stGroupInfo[groupIdx].tpCfgType.to_bytes(1, 'little')
        retVector += groupTotalInfo.stGroupInfo[groupIdx].activated.to_bytes(1, 'little')

        pad = 0x00
        retVector += groupTotalInfo.stGroupInfo[groupIdx].groupName.encode()
        retVector += pad.to_bytes(MAX_GROUP_NAME_LEN+1 - len(groupTotalInfo.stGroupInfo[groupIdx].groupName), 'little')

        retVector += groupTotalInfo.stGroupInfo[groupIdx].numSpeaker.to_bytes(1, 'little')

        speakerIdx = 0
        while speakerIdx < groupTotalInfo.stGroupInfo[groupIdx].numSpeaker:
            retVector += groupTotalInfo.stGroupInfo[groupIdx].stGroupElement[speakerIdx].channel.to_bytes(4, 'little')
            retVector += groupTotalInfo.stGroupInfo[groupIdx].stGroupElement[speakerIdx].role.to_bytes(2, 'little')

            macIdx = 0
            while macIdx < MAX_MAC_ADDR_LEN:
                retVector += groupTotalInfo.stGroupInfo[groupIdx].stGroupElement[speakerIdx].macAddr[macIdx].to_bytes(1, 'little')
                macIdx += 1

            speakerIdx += 1

        groupIdx += 1

    return retVector


def setActivateInfo_to_Vector(activateInfo):
    retVector = bytes()

    retVector += activateInfo.lastUpdatedTime.to_bytes(8, 'little')
    retVector += activateInfo.groupIdx.to_bytes(1, 'little')

    pad = 0x00
    retVector += activateInfo.ssid.encode()
    retVector += pad.to_bytes(MAX_SSID_LEN + 1 - len(activateInfo.ssid), 'little')

    retVector += activateInfo.passwd.encode()
    retVector += pad.to_bytes(MAX_PASSWD_LEN + 1 - len(activateInfo.passwd), 'little')

    return retVector


def getGroupTotalInfo_from_Vector(rcvData):
    groupTotalInfo = S_GROUP_TOTAL_INFO()

    point = 0

    groupTotalInfo.lastUpdatedTime = int.from_bytes(rcvData[point:point+8], 'little')
    point += 8
    groupTotalInfo.numGroup = int.from_bytes(rcvData[point:point+1], 'little')
    point += 1

    groupIdx = 0
    groupTotalInfo.stGroupInfo.clear()
    while groupIdx < groupTotalInfo.numGroup:
        groupTotalInfo.stGroupInfo.append(S_GROUP_INFO())

        groupTotalInfo.stGroupInfo[groupIdx].chCfgType = int.from_bytes(rcvData[point:point+1], 'little')
        point += 1
        groupTotalInfo.stGroupInfo[groupIdx].tpCfgType = int.from_bytes(rcvData[point:point+1], 'little')
        point += 1
        groupTotalInfo.stGroupInfo[groupIdx].activated = int.from_bytes(rcvData[point:point+1], 'little')
        point += 1
        groupTotalInfo.stGroupInfo[groupIdx].groupName = rcvData[point:point+(MAX_GROUP_NAME_LEN+1)].decode('utf-8')
        point += (MAX_GROUP_NAME_LEN+1)
        groupTotalInfo.stGroupInfo[groupIdx].numSpeaker = int.from_bytes(rcvData[point:point+1], 'little')
        point += 1

        speakerIdx=0
        groupTotalInfo.stGroupInfo[groupIdx].stGroupElement = []
        while speakerIdx < groupTotalInfo.stGroupInfo[groupIdx].numSpeaker:
            groupTotalInfo.stGroupInfo[groupIdx].stGroupElement.append(S_GROUP_ELEMENT())

            groupTotalInfo.stGroupInfo[groupIdx].stGroupElement[speakerIdx].channel = int.from_bytes(rcvData[point:point+4], 'little')
            point += 4
            groupTotalInfo.stGroupInfo[groupIdx].stGroupElement[speakerIdx].role = int.from_bytes(rcvData[point:point+2], 'little')
            point += 2

            macIdx=0
            groupTotalInfo.stGroupInfo[groupIdx].stGroupElement[speakerIdx].macAddr = []
            while macIdx < MAX_MAC_ADDR_LEN:
                groupTotalInfo.stGroupInfo[groupIdx].stGroupElement[speakerIdx].macAddr.append(int.from_bytes(rcvData[point:point+1], 'little'))
                point += 1

                macIdx += 1

            speakerIdx += 1

        groupIdx += 1

    return groupTotalInfo


def getGroupVolumeInfo_from_Vector(rcvData):
    groupVolumeInfo = S_GROUP_VOLUME_INFO()

    point = 0

    groupVolumeInfo.groupVolume = int.from_bytes(rcvData[point:point+1], 'little')
    point += 1
    groupVolumeInfo.numSpeaker = int.from_bytes(rcvData[point:point+1], 'little')
    point += 1

    speakerIdx = 0
    groupVolumeInfo.volume = []
    while speakerIdx < groupVolumeInfo.numSpeaker:
        groupVolumeInfo.volume.append(int.from_bytes(rcvData[point:point+1], 'little'))
        point += 1

        speakerIdx += 1

    return groupVolumeInfo


def init_groupBox(ui):
    ui.group0_CheckBox.setChecked(False)
    ui.group0_Mono_Radio.setChecked(False)
    ui.group0_Stereo_Radio.setChecked(False)
    ui.group0_312_Radio.setChecked(False)
    ui.group0_51_Radio.setChecked(False)
    ui.group0_512_Radio.setChecked(False)
    ui.group0_71_Radio.setChecked(False)
    ui.group0_712_Radio.setChecked(False)
    ui.group0_714_Radio.setChecked(False)
    ui.group0_MultiCh_Radio.setChecked(False)
    ui.group0_MultiRo_Radio.setChecked(False)
    ui.group0_Concurr_Radio.setChecked(False)
    ui.group0_Name_LineEdit.clear()
    ui.group0_Device0_CheckBox.setChecked(False)
    ui.group0_Device1_CheckBox.setChecked(False)
    ui.group0_Device2_CheckBox.setChecked(False)
    ui.group0_Device3_CheckBox.setChecked(False)
    ui.group0_Device4_CheckBox.setChecked(False)
    ui.group0_Device5_CheckBox.setChecked(False)
    ui.group0_Device6_CheckBox.setChecked(False)
    ui.group0_Device7_CheckBox.setChecked(False)
    ui.group0_Device8_CheckBox.setChecked(False)
    ui.group0_Device0_Channel_LineEdit.clear()
    ui.group0_Device0_Role_LineEdit.clear()
    ui.group0_Device0_Mac0_lineEdit.clear()
    ui.group0_Device0_Mac1_lineEdit.clear()
    ui.group0_Device0_Mac2_lineEdit.clear()
    ui.group0_Device0_Mac3_lineEdit.clear()
    ui.group0_Device0_Mac4_lineEdit.clear()
    ui.group0_Device0_Mac5_lineEdit.clear()
    ui.group0_Device1_Channel_LineEdit.clear()
    ui.group0_Device1_Role_LineEdit.clear()
    ui.group0_Device1_Mac0_lineEdit.clear()
    ui.group0_Device1_Mac1_lineEdit.clear()
    ui.group0_Device1_Mac2_lineEdit.clear()
    ui.group0_Device1_Mac3_lineEdit.clear()
    ui.group0_Device1_Mac4_lineEdit.clear()
    ui.group0_Device1_Mac5_lineEdit.clear()
    ui.group0_Device2_Channel_LineEdit.clear()
    ui.group0_Device2_Role_LineEdit.clear()
    ui.group0_Device2_Mac0_lineEdit.clear()
    ui.group0_Device2_Mac1_lineEdit.clear()
    ui.group0_Device2_Mac2_lineEdit.clear()
    ui.group0_Device2_Mac3_lineEdit.clear()
    ui.group0_Device2_Mac4_lineEdit.clear()
    ui.group0_Device2_Mac5_lineEdit.clear()
    ui.group0_Device3_Channel_LineEdit.clear()
    ui.group0_Device3_Role_LineEdit.clear()
    ui.group0_Device3_Mac0_lineEdit.clear()
    ui.group0_Device3_Mac1_lineEdit.clear()
    ui.group0_Device3_Mac2_lineEdit.clear()
    ui.group0_Device3_Mac3_lineEdit.clear()
    ui.group0_Device3_Mac4_lineEdit.clear()
    ui.group0_Device3_Mac5_lineEdit.clear()
    ui.group0_Device4_Channel_LineEdit.clear()
    ui.group0_Device4_Role_LineEdit.clear()
    ui.group0_Device4_Mac0_lineEdit.clear()
    ui.group0_Device4_Mac1_lineEdit.clear()
    ui.group0_Device4_Mac2_lineEdit.clear()
    ui.group0_Device4_Mac3_lineEdit.clear()
    ui.group0_Device4_Mac4_lineEdit.clear()
    ui.group0_Device4_Mac5_lineEdit.clear()
    ui.group0_Device5_Channel_LineEdit.clear()
    ui.group0_Device5_Role_LineEdit.clear()
    ui.group0_Device5_Mac0_lineEdit.clear()
    ui.group0_Device5_Mac1_lineEdit.clear()
    ui.group0_Device5_Mac2_lineEdit.clear()
    ui.group0_Device5_Mac3_lineEdit.clear()
    ui.group0_Device5_Mac4_lineEdit.clear()
    ui.group0_Device5_Mac5_lineEdit.clear()
    ui.group0_Device6_Channel_LineEdit.clear()
    ui.group0_Device6_Role_LineEdit.clear()
    ui.group0_Device6_Mac0_lineEdit.clear()
    ui.group0_Device6_Mac1_lineEdit.clear()
    ui.group0_Device6_Mac2_lineEdit.clear()
    ui.group0_Device6_Mac3_lineEdit.clear()
    ui.group0_Device6_Mac4_lineEdit.clear()
    ui.group0_Device6_Mac5_lineEdit.clear()
    ui.group0_Device7_Channel_LineEdit.clear()
    ui.group0_Device7_Role_LineEdit.clear()
    ui.group0_Device7_Mac0_lineEdit.clear()
    ui.group0_Device7_Mac1_lineEdit.clear()
    ui.group0_Device7_Mac2_lineEdit.clear()
    ui.group0_Device7_Mac3_lineEdit.clear()
    ui.group0_Device7_Mac4_lineEdit.clear()
    ui.group0_Device7_Mac5_lineEdit.clear()
    ui.group0_Device8_Channel_LineEdit.clear()
    ui.group0_Device8_Role_LineEdit.clear()
    ui.group0_Device8_Mac0_lineEdit.clear()
    ui.group0_Device8_Mac1_lineEdit.clear()
    ui.group0_Device8_Mac2_lineEdit.clear()
    ui.group0_Device8_Mac3_lineEdit.clear()
    ui.group0_Device8_Mac4_lineEdit.clear()
    ui.group0_Device8_Mac5_lineEdit.clear()

    ui.group1_CheckBox.setChecked(False)
    ui.group1_Mono_Radio.setChecked(False)
    ui.group1_Stereo_Radio.setChecked(False)
    ui.group1_312_Radio.setChecked(False)
    ui.group1_51_Radio.setChecked(False)
    ui.group1_512_Radio.setChecked(False)
    ui.group1_71_Radio.setChecked(False)
    ui.group1_712_Radio.setChecked(False)
    ui.group1_714_Radio.setChecked(False)
    ui.group1_MultiCh_Radio.setChecked(False)
    ui.group1_MultiRo_Radio.setChecked(False)
    ui.group1_Concurr_Radio.setChecked(False)
    ui.group1_Name_LineEdit.clear()
    ui.group1_Device0_CheckBox.setChecked(False)
    ui.group1_Device1_CheckBox.setChecked(False)
    ui.group1_Device2_CheckBox.setChecked(False)
    ui.group1_Device3_CheckBox.setChecked(False)
    ui.group1_Device4_CheckBox.setChecked(False)
    ui.group1_Device5_CheckBox.setChecked(False)
    ui.group1_Device6_CheckBox.setChecked(False)
    ui.group1_Device7_CheckBox.setChecked(False)
    ui.group1_Device8_CheckBox.setChecked(False)
    ui.group1_Device0_Channel_LineEdit.clear()
    ui.group1_Device0_Role_LineEdit.clear()
    ui.group1_Device0_Mac0_lineEdit.clear()
    ui.group1_Device0_Mac1_lineEdit.clear()
    ui.group1_Device0_Mac2_lineEdit.clear()
    ui.group1_Device0_Mac3_lineEdit.clear()
    ui.group1_Device0_Mac4_lineEdit.clear()
    ui.group1_Device0_Mac5_lineEdit.clear()
    ui.group1_Device1_Channel_LineEdit.clear()
    ui.group1_Device1_Role_LineEdit.clear()
    ui.group1_Device1_Mac0_lineEdit.clear()
    ui.group1_Device1_Mac1_lineEdit.clear()
    ui.group1_Device1_Mac2_lineEdit.clear()
    ui.group1_Device1_Mac3_lineEdit.clear()
    ui.group1_Device1_Mac4_lineEdit.clear()
    ui.group1_Device1_Mac5_lineEdit.clear()
    ui.group1_Device2_Channel_LineEdit.clear()
    ui.group1_Device2_Role_LineEdit.clear()
    ui.group1_Device2_Mac0_lineEdit.clear()
    ui.group1_Device2_Mac1_lineEdit.clear()
    ui.group1_Device2_Mac2_lineEdit.clear()
    ui.group1_Device2_Mac3_lineEdit.clear()
    ui.group1_Device2_Mac4_lineEdit.clear()
    ui.group1_Device2_Mac5_lineEdit.clear()
    ui.group1_Device3_Channel_LineEdit.clear()
    ui.group1_Device3_Role_LineEdit.clear()
    ui.group1_Device3_Mac0_lineEdit.clear()
    ui.group1_Device3_Mac1_lineEdit.clear()
    ui.group1_Device3_Mac2_lineEdit.clear()
    ui.group1_Device3_Mac3_lineEdit.clear()
    ui.group1_Device3_Mac4_lineEdit.clear()
    ui.group1_Device3_Mac5_lineEdit.clear()
    ui.group1_Device4_Channel_LineEdit.clear()
    ui.group1_Device4_Role_LineEdit.clear()
    ui.group1_Device4_Mac0_lineEdit.clear()
    ui.group1_Device4_Mac1_lineEdit.clear()
    ui.group1_Device4_Mac2_lineEdit.clear()
    ui.group1_Device4_Mac3_lineEdit.clear()
    ui.group1_Device4_Mac4_lineEdit.clear()
    ui.group1_Device4_Mac5_lineEdit.clear()
    ui.group1_Device5_Channel_LineEdit.clear()
    ui.group1_Device5_Role_LineEdit.clear()
    ui.group1_Device5_Mac0_lineEdit.clear()
    ui.group1_Device5_Mac1_lineEdit.clear()
    ui.group1_Device5_Mac2_lineEdit.clear()
    ui.group1_Device5_Mac3_lineEdit.clear()
    ui.group1_Device5_Mac4_lineEdit.clear()
    ui.group1_Device5_Mac5_lineEdit.clear()
    ui.group1_Device6_Channel_LineEdit.clear()
    ui.group1_Device6_Role_LineEdit.clear()
    ui.group1_Device6_Mac0_lineEdit.clear()
    ui.group1_Device6_Mac1_lineEdit.clear()
    ui.group1_Device6_Mac2_lineEdit.clear()
    ui.group1_Device6_Mac3_lineEdit.clear()
    ui.group1_Device6_Mac4_lineEdit.clear()
    ui.group1_Device6_Mac5_lineEdit.clear()
    ui.group1_Device7_Channel_LineEdit.clear()
    ui.group1_Device7_Role_LineEdit.clear()
    ui.group1_Device7_Mac0_lineEdit.clear()
    ui.group1_Device7_Mac1_lineEdit.clear()
    ui.group1_Device7_Mac2_lineEdit.clear()
    ui.group1_Device7_Mac3_lineEdit.clear()
    ui.group1_Device7_Mac4_lineEdit.clear()
    ui.group1_Device7_Mac5_lineEdit.clear()
    ui.group1_Device8_Channel_LineEdit.clear()
    ui.group1_Device8_Role_LineEdit.clear()
    ui.group1_Device8_Mac0_lineEdit.clear()
    ui.group1_Device8_Mac1_lineEdit.clear()
    ui.group1_Device8_Mac2_lineEdit.clear()
    ui.group1_Device8_Mac3_lineEdit.clear()
    ui.group1_Device8_Mac4_lineEdit.clear()
    ui.group1_Device8_Mac5_lineEdit.clear()


def init_groupVolume(ui):
    ui.group0_groupVolume_LineEdit.clear()
    ui.group0_Device0_Vol_LineEdit.clear()
    ui.group0_Device1_Vol_LineEdit.clear()
    ui.group0_Device2_Vol_LineEdit.clear()
    ui.group0_Device3_Vol_LineEdit.clear()
    ui.group0_Device4_Vol_LineEdit.clear()
    ui.group0_Device5_Vol_LineEdit.clear()
    ui.group0_Device6_Vol_LineEdit.clear()
    ui.group0_Device7_Vol_LineEdit.clear()
    ui.group0_Device8_Vol_LineEdit.clear()

    ui.group1_groupVolume_LineEdit.clear()
    ui.group1_Device0_Vol_LineEdit.clear()
    ui.group1_Device1_Vol_LineEdit.clear()
    ui.group1_Device2_Vol_LineEdit.clear()
    ui.group1_Device3_Vol_LineEdit.clear()
    ui.group1_Device4_Vol_LineEdit.clear()
    ui.group1_Device5_Vol_LineEdit.clear()
    ui.group1_Device6_Vol_LineEdit.clear()
    ui.group1_Device7_Vol_LineEdit.clear()
    ui.group1_Device8_Vol_LineEdit.clear()