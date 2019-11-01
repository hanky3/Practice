import datetime
from remote_context import *
from remote_data_convert import *
from remote_server import *
from remote_client import *


def setAddrButton_Handler_func(ui):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += " Set Address Button Clicked"
    ui.log_TextBrowser.append(log)

    ui.WoWIF.SPK_UI.Initialize_SPK_UI()
    ui.WoWIF.TBL_UI.Initialize_TBL_UI()
    if ui.Timer.isActive(): ui.Timer.stop()

    addr = ui.addr_LineEdit.text()
    send_SetControllerAddr(ui, addr)


def getGroupInfoButton_Handler_func(ui):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += " Get Group Info Button Clicked"
    ui.log_TextBrowser.append(log)

    send_GetGroupInfo(ui)


def setGroupInfoButton_Handler_func(ui):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += " Set Group Info Button Clicked"
    ui.log_TextBrowser.append(log)

    groupTotalInfo = S_GROUP_TOTAL_INFO()

    groupTotalInfo.lastUpdatedTime = round(datetime.datetime.utcnow().timestamp() * 1000)
    groupTotalInfo.numGroup = 0

    groupTotalInfo.stGroupInfo = []
    tmp = 0
    if ui.group0_CheckBox.isChecked() == True:
        groupTotalInfo.numGroup += 1
        groupTotalInfo.stGroupInfo.append(S_GROUP_INFO())
        tmp += 1
        if ui.group0_Mono_Radio.isChecked() == True:
            groupTotalInfo.stGroupInfo[0].chCfgType = CH_CFG_TYPE_MONO
        elif ui.group0_Stereo_Radio.isChecked() == True:
            groupTotalInfo.stGroupInfo[0].chCfgType = CH_CFG_TYPE_STEREO
        elif ui.group0_312_Radio.isChecked() == True:
            groupTotalInfo.stGroupInfo[0].chCfgType = CH_CFG_TYPE_3_1_2
        elif ui.group0_51_Radio.isChecked() == True:
            groupTotalInfo.stGroupInfo[0].chCfgType = CH_CFG_TYPE_5_1
        elif ui.group0_512_Radio.isChecked() == True:
            groupTotalInfo.stGroupInfo[0].chCfgType = CH_CFG_TYPE_5_1_2
        elif ui.group0_71_Radio.isChecked() == True:
            groupTotalInfo.stGroupInfo[0].chCfgType = CH_CFG_TYPE_7_1
        elif ui.group0_712_Radio.isChecked() == True:
            groupTotalInfo.stGroupInfo[0].chCfgType = CH_CFG_TYPE_7_1_2
        elif ui.group0_714_Radio.isChecked() == True:
            groupTotalInfo.stGroupInfo[0].chCfgType = CH_CFG_TYPE_7_1_4

        if ui.group0_MultiCh_Radio.isChecked() == True:
            groupTotalInfo.stGroupInfo[0].tpCfgType = TP_CFG_MULTI_CHANNEL
        elif ui.group0_MultiRo_Radio.isChecked() == True:
            groupTotalInfo.stGroupInfo[0].tpCfgType = TP_CFG_MULTI_ROOM
        elif ui.group0_Concurr_Radio.isChecked() == True:
            groupTotalInfo.stGroupInfo[0].tpCfgType = TP_CFG_CONCURRENT

        groupTotalInfo.stGroupInfo[0].activated = 0
        groupTotalInfo.stGroupInfo[0].groupName = ui.group0_Name_LineEdit.text()

        groupTotalInfo.stGroupInfo[0].numSpeaker = 0
        groupTotalInfo.stGroupInfo[0].stGroupElement = []
        if ui.group0_Device0_CheckBox.isChecked() == True:
            groupTotalInfo.stGroupInfo[0].stGroupElement.append(S_GROUP_ELEMENT())
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].channel = int(
                ui.group0_Device0_Channel_LineEdit.text(), 16)
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].role = int(ui.group0_Device0_Role_LineEdit.text())

            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr = []
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device0_Mac0_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device0_Mac1_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device0_Mac2_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device0_Mac3_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device0_Mac4_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device0_Mac5_lineEdit.text(), 16))

            groupTotalInfo.stGroupInfo[0].numSpeaker += 1

        if ui.group0_Device1_CheckBox.isChecked() == True:
            groupTotalInfo.stGroupInfo[0].stGroupElement.append(S_GROUP_ELEMENT())
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].channel = int(
                ui.group0_Device1_Channel_LineEdit.text(), 16)
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].role = int(ui.group0_Device1_Role_LineEdit.text())
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr = []
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device1_Mac0_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device1_Mac1_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device1_Mac2_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device1_Mac3_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device1_Mac4_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device1_Mac5_lineEdit.text(), 16))

            groupTotalInfo.stGroupInfo[0].numSpeaker += 1

        if ui.group0_Device2_CheckBox.isChecked() == True:
            groupTotalInfo.stGroupInfo[0].stGroupElement.append(S_GROUP_ELEMENT())
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].channel = int(
                ui.group0_Device2_Channel_LineEdit.text(), 16)
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].role = int(ui.group0_Device2_Role_LineEdit.text())
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr = []
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device2_Mac0_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device2_Mac1_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device2_Mac2_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device2_Mac3_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device2_Mac4_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device2_Mac5_lineEdit.text(), 16))

            groupTotalInfo.stGroupInfo[0].numSpeaker += 1

        if ui.group0_Device3_CheckBox.isChecked() == True:
            groupTotalInfo.stGroupInfo[0].stGroupElement.append(S_GROUP_ELEMENT())
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].channel = int(
                ui.group0_Device3_Channel_LineEdit.text(), 16)
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].role = int(ui.group0_Device3_Role_LineEdit.text())
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr = []
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device3_Mac0_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device3_Mac1_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device3_Mac2_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device3_Mac3_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device3_Mac4_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device3_Mac5_lineEdit.text(), 16))

            groupTotalInfo.stGroupInfo[0].numSpeaker += 1

        if ui.group0_Device4_CheckBox.isChecked() == True:
            groupTotalInfo.stGroupInfo[0].stGroupElement.append(S_GROUP_ELEMENT())
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].channel = int(
                ui.group0_Device4_Channel_LineEdit.text(), 16)
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].role = int(ui.group0_Device4_Role_LineEdit.text())
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr = []
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device4_Mac0_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device4_Mac1_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device4_Mac2_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device4_Mac3_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device4_Mac4_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device4_Mac5_lineEdit.text(), 16))

            groupTotalInfo.stGroupInfo[0].numSpeaker += 1

        if ui.group0_Device5_CheckBox.isChecked() == True:
            groupTotalInfo.stGroupInfo[0].stGroupElement.append(S_GROUP_ELEMENT())
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].channel = int(
                ui.group0_Device5_Channel_LineEdit.text(), 16)
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].role = int(ui.group0_Device5_Role_LineEdit.text())
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr = []
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device5_Mac0_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device5_Mac1_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device5_Mac2_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device5_Mac3_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device5_Mac4_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device5_Mac5_lineEdit.text(), 16))

            groupTotalInfo.stGroupInfo[0].numSpeaker += 1

        if ui.group0_Device6_CheckBox.isChecked() == True:
            groupTotalInfo.stGroupInfo[0].stGroupElement.append(S_GROUP_ELEMENT())
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].channel = int(
                ui.group0_Device6_Channel_LineEdit.text(), 16)
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].role = int(ui.group0_Device6_Role_LineEdit.text())
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr = []
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device6_Mac0_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device6_Mac1_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device6_Mac2_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device6_Mac3_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device6_Mac4_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device6_Mac5_lineEdit.text(), 16))

            groupTotalInfo.stGroupInfo[0].numSpeaker += 1

        if ui.group0_Device7_CheckBox.isChecked() == True:
            groupTotalInfo.stGroupInfo[0].stGroupElement.append(S_GROUP_ELEMENT())
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].channel = int(
                ui.group0_Device7_Channel_LineEdit.text(), 16)
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].role = int(ui.group0_Device7_Role_LineEdit.text())
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr = []
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device7_Mac0_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device7_Mac1_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device7_Mac2_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device7_Mac3_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device7_Mac4_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device7_Mac5_lineEdit.text(), 16))

            groupTotalInfo.stGroupInfo[0].numSpeaker += 1

        if ui.group0_Device8_CheckBox.isChecked() == True:
            groupTotalInfo.stGroupInfo[0].stGroupElement.append(S_GROUP_ELEMENT())
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].channel = int(
                ui.group0_Device8_Channel_LineEdit.text(), 16)
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].role = int(ui.group0_Device8_Role_LineEdit.text())
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr = []
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device8_Mac0_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device8_Mac1_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device8_Mac2_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device8_Mac3_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device8_Mac4_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[0].stGroupElement[groupTotalInfo.stGroupInfo[0].numSpeaker].macAddr.append(
                int(ui.group0_Device8_Mac5_lineEdit.text(), 16))

            groupTotalInfo.stGroupInfo[0].numSpeaker += 1

    if ui.group1_CheckBox.isChecked() == True:
        groupTotalInfo.numGroup += 1
        groupTotalInfo.stGroupInfo.append(S_GROUP_INFO())
        tmp += 2
        if ui.group1_Mono_Radio.isChecked() == True:
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].chCfgType = CH_CFG_TYPE_MONO
        elif ui.group1_Stereo_Radio.isChecked() == True:
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].chCfgType = CH_CFG_TYPE_STEREO
        elif ui.group1_312_Radio.isChecked() == True:
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].chCfgType = CH_CFG_TYPE_3_1_2
        elif ui.group1_51_Radio.isChecked() == True:
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].chCfgType = CH_CFG_TYPE_5_1
        elif ui.group1_512_Radio.isChecked() == True:
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].chCfgType = CH_CFG_TYPE_5_1_2
        elif ui.group1_71_Radio.isChecked() == True:
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].chCfgType = CH_CFG_TYPE_7_1
        elif ui.group1_712_Radio.isChecked() == True:
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].chCfgType = CH_CFG_TYPE_7_1_2
        elif ui.group1_714_Radio.isChecked() == True:
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].chCfgType = CH_CFG_TYPE_7_1_4

        if ui.group1_MultiCh_Radio.isChecked() == True:
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].tpCfgType = TP_CFG_MULTI_CHANNEL
        elif ui.group1_MultiRo_Radio.isChecked() == True:
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].tpCfgType = TP_CFG_MULTI_ROOM
        elif ui.group1_Concurr_Radio.isChecked() == True:
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].tpCfgType = TP_CFG_CONCURRENT

        groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].activated = 0
        groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].groupName = ui.group1_Name_LineEdit.text()

        groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker = 0
        groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement = []

        if ui.group1_Device0_CheckBox.isChecked() == True:
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement.append(S_GROUP_ELEMENT())
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].channel = int(
                ui.group1_Device0_Channel_LineEdit.text(), 16)
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].role = int(ui.group1_Device0_Role_LineEdit.text())
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr = []
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device0_Mac0_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device0_Mac1_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device0_Mac2_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device0_Mac3_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device0_Mac4_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device0_Mac5_lineEdit.text(), 16))

            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker += 1

        if ui.group1_Device1_CheckBox.isChecked() == True:
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement.append(S_GROUP_ELEMENT())
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].channel = int(
                ui.group1_Device1_Channel_LineEdit.text(), 16)
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].role = int(ui.group1_Device1_Role_LineEdit.text())
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr = []
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device1_Mac0_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device1_Mac1_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device1_Mac2_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device1_Mac3_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device1_Mac4_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device1_Mac5_lineEdit.text(), 16))

            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker += 1

        if ui.group1_Device2_CheckBox.isChecked() == True:
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement.append(S_GROUP_ELEMENT())
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].channel = int(
                ui.group1_Device2_Channel_LineEdit.text(), 16)
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].role = int(ui.group1_Device2_Role_LineEdit.text())
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr = []
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device2_Mac0_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device2_Mac1_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device2_Mac2_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device2_Mac3_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device2_Mac4_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device2_Mac5_lineEdit.text(), 16))

            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker += 1

        if ui.group1_Device3_CheckBox.isChecked() == True:
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement.append(S_GROUP_ELEMENT())
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].channel = int(
                ui.group1_Device3_Channel_LineEdit.text(), 16)
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].role = int(ui.group1_Device3_Role_LineEdit.text())
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr = []
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device3_Mac0_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device3_Mac1_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device3_Mac2_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device3_Mac3_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device3_Mac4_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device3_Mac5_lineEdit.text(), 16))

            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker += 1

        if ui.group1_Device4_CheckBox.isChecked() == True:
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement.append(S_GROUP_ELEMENT())
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].channel = int(
                ui.group1_Device4_Channel_LineEdit.text(), 16)
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].role = int(ui.group1_Device4_Role_LineEdit.text())
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr = []
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device4_Mac0_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device4_Mac1_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device4_Mac2_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device4_Mac3_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device4_Mac4_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device4_Mac5_lineEdit.text(), 16))

            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker += 1

        if ui.group1_Device5_CheckBox.isChecked() == True:
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement.append(S_GROUP_ELEMENT())
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].channel = int(
                ui.group1_Device5_Channel_LineEdit.text(), 16)
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].role = int(ui.group1_Device5_Role_LineEdit.text())
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr = []
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device5_Mac0_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device5_Mac1_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device5_Mac2_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device5_Mac3_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device5_Mac4_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device5_Mac5_lineEdit.text(), 16))

            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker += 1

        if ui.group1_Device6_CheckBox.isChecked() == True:
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement.append(S_GROUP_ELEMENT())
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].channel = int(
                ui.group1_Device6_Channel_LineEdit.text(), 16)
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].role = int(ui.group1_Device6_Role_LineEdit.text())
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr = []
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device6_Mac0_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device6_Mac1_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device6_Mac2_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device6_Mac3_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device6_Mac4_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device6_Mac5_lineEdit.text(), 16))

            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker += 1

        if ui.group1_Device7_CheckBox.isChecked() == True:
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement.append(S_GROUP_ELEMENT())
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].channel = int(
                ui.group1_Device7_Channel_LineEdit.text(), 16)
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].role = int(ui.group1_Device7_Role_LineEdit.text())
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr = []
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device7_Mac0_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device7_Mac1_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device7_Mac2_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device7_Mac3_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device7_Mac4_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device7_Mac5_lineEdit.text(), 16))

            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker += 1

        if ui.group1_Device8_CheckBox.isChecked() == True:
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement.append(S_GROUP_ELEMENT())
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].channel = int(
                ui.group1_Device8_Channel_LineEdit.text(), 16)
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].role = int(ui.group1_Device8_Role_LineEdit.text())
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr = []
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device8_Mac0_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device8_Mac1_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device8_Mac2_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device8_Mac3_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device8_Mac4_lineEdit.text(), 16))
            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].stGroupElement[groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker].macAddr.append(
                int(ui.group1_Device8_Mac5_lineEdit.text(), 16))

            groupTotalInfo.stGroupInfo[groupTotalInfo.numGroup - 1].numSpeaker += 1

    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += " Number of set group: "
    log += str(groupTotalInfo.numGroup)
    ui.log_TextBrowser.append(log)

    groupVector = setGroupTotalInfo_to_Vector(groupTotalInfo)
    send_SetGroupInfo(ui, groupVector)

    groupTotalInfo.numGroup = tmp
    updateSetGroupInfo(groupTotalInfo)


def activationButton_Handler_func(ui):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += " Activation Button Clicked"
    ui.log_TextBrowser.append(log)

    activateInfo = S_GROUP_ACTIVATE_INFO()

    activateInfo.lastUpdatedTime = round(datetime.datetime.utcnow().timestamp() * 1000)

    if ui.group0_Radio.isChecked() == True:
        activateInfo.groupIdx = 0
        setActivateIdx(0)
    elif ui.group1_Radio.isChecked() == True:
        activateInfo.groupIdx = 1
        setActivateIdx(1)
    else:
        log = datetime.datetime.now().strftime("[%H:%M:%S]")
        log += "Activation Button is not selected - MSG is not sent."
        return


    activateInfo.ssid = ui.ssid_LineEdit.text()
    activateInfo.passwd = ui.passwd_LineEdit.text()

    if ui.group0_Radio.isChecked() == True or ui.group1_Radio.isChecked() == True:
        activateVector = setActivateInfo_to_Vector(activateInfo)
        send_ActivateInfo(ui, activateVector)


def deactivationButton_Handler_func(ui):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += " Deactivation Button Clicked"
    ui.log_TextBrowser.append(log)

    if ui.Timer.isActive(): ui.Timer.stop()
    send_DeactivateInfo(ui, round(datetime.datetime.utcnow().timestamp() * 1000))


def playButton_Handler_func(ui):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += " Play Button Clicked"
    ui.log_TextBrowser.append(log)

    send_Play(ui, 1)
    updatePlayPauseInfo(1)

def pauseButton_Handler_func(ui):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += " Pause Button Clicked"
    ui.log_TextBrowser.append(log)

    send_Play(ui, 0)
    updatePlayPauseInfo(0)

def muteButton_Handler_func(ui):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += " Mute Button Clicked"
    ui.log_TextBrowser.append(log)

    send_Mute(ui, 0)
    updateMueteUnmuteInfo(0)


def unmuteButton_Handler_func(ui):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += " Unmute Button Clicked"
    ui.log_TextBrowser.append(log)

    send_Mute(ui, 1)
    updateMueteUnmuteInfo(1)


def getVolumeButton_Handler_func(ui):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += " Get Volume Button Clicked"
    ui.log_TextBrowser.append(log)

    send_GetGroupVolumeInfo(ui)


def setAbsVolumeButton_Handler_func(ui):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    str_dev_id = ui.deviceIndex_LineEdit.text() if ui.deviceIndex_LineEdit.text() is not "" else None
    str_vol = ui.volume_LineEdit.text() if ui.volume_LineEdit.text() is not "" else None

    if str_dev_id is not None and str_vol is not None:
        send_SetAbsVolumeReq(ui, int(str_dev_id, 16), int(str_vol))
        log += " Set Abs Volume Button Clicked"
    else:
        log += " Set Abs Volume Button Clicked - [Invalid Input] Message is not sent!!!!"

    ui.log_TextBrowser.append(log)


def upbutton_Handler_func(ui):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += " Volume Up Button Clicked"
    str_devid = ui.deviceIndex_LineEdit.text()
    if str_devid is not "":
        send_SetRelVolumeReq(ui, int(str_devid,16), 0)
    else:
        log += " - Message is not sent : device id is not configured!!"

    ui.log_TextBrowser.append(log)


def downButton_Handler_func(ui):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += " Volume Down Button Clicked"
    str_devid = ui.deviceIndex_LineEdit.text()

    if str_devid is not "":
        send_SetRelVolumeReq(ui, int(str_devid,16), 1)
    else:
        log += " - Message is not sent : device id is not configured!!"

    ui.log_TextBrowser.append(log)

def timeOut_Handler_func(ui):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += " Timer Expired - Get Wireless Info"
    send_GetWirelessInfo(ui)
    ui.WoWIF.UpdateTBL_PrintDebugView(log)
    # ui.log_TextBrowser.append(log)