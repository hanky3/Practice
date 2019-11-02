import sys
import socket
import datetime
from remote_context import *
from remote_data_convert import *
from remote_server import *
import ui_context
from statistics import mean

Timeout_Time = 1000*5       # 5 sec

def set_CtrlAddrRet_Handler(ui, rcvData):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += " Address setting done. CID: "
    log += str(rcvData[1])
    ui.log_TextBrowser.append(log)

def get_GroupInfoRet_Handler(ui, rcvData):
    groupTotalInfo = getGroupTotalInfo_from_Vector(rcvData[1:])

    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += " Get Group Info done"
    ui.log_TextBrowser.append(log)

    init_groupBox(ui)

    ui_context.update_group_info_cmn(clr_flag=True)
    for gr_idx in range(0,groupTotalInfo.numGroup):
        exec("ui.group%d_CheckBox.setChecked(%s)"%(gr_idx,"True"))

        chCfgType = groupTotalInfo.stGroupInfo[gr_idx].chCfgType
        if chCfgType in CH_CFG_TYPE_TO_STRING:
            exec("ui.group%d_%s_Radio.setChecked(%s)"%(gr_idx,CH_CFG_TYPE_TO_STRING[chCfgType][0],"True"))

        tpCfgType = groupTotalInfo.stGroupInfo[gr_idx].tpCfgType
        if tpCfgType in TP_CFG_TYPE_TO_STRING:
            exec("ui.group%d_%s_Radio.setChecked(%s)" % (gr_idx, TP_CFG_TYPE_TO_STRING[tpCfgType][0], "True"))

        tmp = groupTotalInfo.stGroupInfo[gr_idx].groupName
        groupName = ""
        for id in range(0,20):
            if(tmp[id]!='\x00'):
                groupName += tmp[id]
            else:
                break;

        print(len(groupName),groupName,type(groupName))
        exec("ui.group%d_Name_LineEdit.setText(\"%s\")"%(gr_idx, groupName))

        ui_context.update_group_info_cmn(gr_id=gr_idx,ch_cfg=chCfgType,topology=tpCfgType,group_name=groupName)

        for dev_idx in range(0,groupTotalInfo.stGroupInfo[gr_idx].numSpeaker):
            exec("ui.group%d_Device%d_CheckBox.setChecked(%s)"%(gr_idx, dev_idx, "True"))

            channel = groupTotalInfo.stGroupInfo[gr_idx].stGroupElement[dev_idx].channel
            exec("ui.group%d_Device%d_Channel_LineEdit.setText(\"%02x\")"%(gr_idx, dev_idx, channel))

            role = str(groupTotalInfo.stGroupInfo[gr_idx].stGroupElement[dev_idx].role)
            exec("ui.group%d_Device%d_Role_LineEdit.setText(\"%s\")" % (gr_idx, dev_idx, role))

            macAddr = []
            for addr_Idx in range(0, 6):
                addrPart = groupTotalInfo.stGroupInfo[gr_idx].stGroupElement[dev_idx].macAddr[addr_Idx]
                macAddr.append(addrPart)
                exec("ui.group%d_Device%d_Mac%d_lineEdit.setText(\"%02x\")"%(gr_idx, dev_idx, addr_Idx, addrPart))

            ui_context.Update_dev_info_in_group(sel_flag=True, gr_id=gr_idx, dev_id=dev_idx,
                                                macAddr=macAddr, role=role, ch=channel, vol='')

    # if groupTotalInfo.numGroup >= 1:
    #     ui.group0_CheckBox.setChecked(True)
    #
    #     if groupTotalInfo.stGroupInfo[0].chCfgType == CH_CFG_TYPE_MONO:
    #         ui.group0_Mono_Radio.setChecked(True)
    #     elif groupTotalInfo.stGroupInfo[0].chCfgType == CH_CFG_TYPE_STEREO:
    #         ui.group0_Stereo_Radio.setChecked(True)
    #     elif groupTotalInfo.stGroupInfo[0].chCfgType == CH_CFG_TYPE_3_1_2:
    #         ui.group0_312_Radio.setChecked(True)
    #     elif groupTotalInfo.stGroupInfo[0].chCfgType == CH_CFG_TYPE_5_1:
    #         ui.group0_51_Radio.setChecked(True)
    #     elif groupTotalInfo.stGroupInfo[0].chCfgType == CH_CFG_TYPE_5_1_2:
    #         ui.group0_512_Radio.setChecked(True)
    #     elif groupTotalInfo.stGroupInfo[0].chCfgType == CH_CFG_TYPE_7_1:
    #         ui.group0_71_Radio.setChecked(True)
    #     elif groupTotalInfo.stGroupInfo[0].chCfgType == CH_CFG_TYPE_7_1_2:
    #         ui.group0_712_Radio.setChecked(True)
    #     elif groupTotalInfo.stGroupInfo[0].chCfgType == CH_CFG_TYPE_7_1_4:
    #         ui.group0_714_Radio.setChecked(True)
    #
    #     if groupTotalInfo.stGroupInfo[0].tpCfgType == TP_CFG_MULTI_CHANNEL:
    #         ui.group0_MultiCh_Radio.setChecked(True)
    #     elif groupTotalInfo.stGroupInfo[0].tpCfgType == TP_CFG_MULTI_ROOM:
    #         ui.group0_MultiRo_Radio.setChecked(True)
    #     elif groupTotalInfo.stGroupInfo[0].tpCfgType == TP_CFG_CONCURRENT:
    #         ui.group0_Concurr_Radio.setChecked(True)
    #
    #     ui.group0_Name_LineEdit.setText(groupTotalInfo.stGroupInfo[0].groupName)
    #
    #     i = groupTotalInfo.stGroupInfo[0].numSpeaker
    #     if i > 0:
    #         ui.group0_Device0_CheckBox.setChecked(True)
    #         ui.group0_Device0_Channel_LineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[0].channel)
    #         ui.group0_Device0_Role_LineEdit.setText(str(groupTotalInfo.stGroupInfo[0].stGroupElement[0].role))
    #         ui.group0_Device0_Mac0_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[0].macAddr[0])
    #         ui.group0_Device0_Mac1_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[0].macAddr[1])
    #         ui.group0_Device0_Mac2_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[0].macAddr[2])
    #         ui.group0_Device0_Mac3_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[0].macAddr[3])
    #         ui.group0_Device0_Mac4_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[0].macAddr[4])
    #         ui.group0_Device0_Mac5_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[0].macAddr[5])
    #         i -= 1
    #     if i > 0:
    #         ui.group0_Device1_CheckBox.setChecked(True)
    #         ui.group0_Device1_Channel_LineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[1].channel)
    #         ui.group0_Device1_Role_LineEdit.setText(str(groupTotalInfo.stGroupInfo[0].stGroupElement[1].role))
    #         ui.group0_Device1_Mac0_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[1].macAddr[0])
    #         ui.group0_Device1_Mac1_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[1].macAddr[1])
    #         ui.group0_Device1_Mac2_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[1].macAddr[2])
    #         ui.group0_Device1_Mac3_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[1].macAddr[3])
    #         ui.group0_Device1_Mac4_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[1].macAddr[4])
    #         ui.group0_Device1_Mac5_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[1].macAddr[5])
    #         i -= 1
    #     if i > 0:
    #         ui.group0_Device2_CheckBox.setChecked(True)
    #         ui.group0_Device2_Channel_LineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[2].channel)
    #         ui.group0_Device2_Role_LineEdit.setText(str(groupTotalInfo.stGroupInfo[0].stGroupElement[2].role))
    #         ui.group0_Device2_Mac0_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[2].macAddr[0])
    #         ui.group0_Device2_Mac1_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[2].macAddr[1])
    #         ui.group0_Device2_Mac2_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[2].macAddr[2])
    #         ui.group0_Device2_Mac3_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[2].macAddr[3])
    #         ui.group0_Device2_Mac4_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[2].macAddr[4])
    #         ui.group0_Device2_Mac5_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[2].macAddr[5])
    #         i -= 1
    #     if i > 0:
    #         ui.group0_Device3_CheckBox.setChecked(True)
    #         ui.group0_Device3_Channel_LineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[3].channel)
    #         ui.group0_Device3_Role_LineEdit.setText(str(groupTotalInfo.stGroupInfo[0].stGroupElement[3].role))
    #         ui.group0_Device3_Mac0_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[3].macAddr[0])
    #         ui.group0_Device3_Mac1_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[3].macAddr[1])
    #         ui.group0_Device3_Mac2_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[3].macAddr[2])
    #         ui.group0_Device3_Mac3_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[3].macAddr[3])
    #         ui.group0_Device3_Mac4_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[3].macAddr[4])
    #         ui.group0_Device3_Mac5_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[3].macAddr[5])
    #         i -= 1
    #     if i > 0:
    #         ui.group0_Device4_CheckBox.setChecked(True)
    #         ui.group0_Device4_Channel_LineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[4].channel)
    #         ui.group0_Device4_Role_LineEdit.setText(str(groupTotalInfo.stGroupInfo[0].stGroupElement[4].role))
    #         ui.group0_Device4_Mac0_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[4].macAddr[0])
    #         ui.group0_Device4_Mac1_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[4].macAddr[1])
    #         ui.group0_Device4_Mac2_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[4].macAddr[2])
    #         ui.group0_Device4_Mac3_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[4].macAddr[3])
    #         ui.group0_Device4_Mac4_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[4].macAddr[4])
    #         ui.group0_Device4_Mac5_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[4].macAddr[5])
    #         i -= 1
    #     if i > 0:
    #         ui.group0_Device5_CheckBox.setChecked(True)
    #         ui.group0_Device5_Channel_LineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[5].channel)
    #         ui.group0_Device5_Role_LineEdit.setText(str(groupTotalInfo.stGroupInfo[0].stGroupElement[5].role))
    #         ui.group0_Device5_Mac0_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[5].macAddr[0])
    #         ui.group0_Device5_Mac1_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[5].macAddr[1])
    #         ui.group0_Device5_Mac2_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[5].macAddr[2])
    #         ui.group0_Device5_Mac3_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[5].macAddr[3])
    #         ui.group0_Device5_Mac4_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[5].macAddr[4])
    #         ui.group0_Device5_Mac5_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[5].macAddr[5])
    #         i -= 1
    #     if i > 0:
    #         ui.group0_Device6_CheckBox.setChecked(True)
    #         ui.group0_Device6_Channel_LineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[6].channel)
    #         ui.group0_Device6_Role_LineEdit.setText(str(groupTotalInfo.stGroupInfo[0].stGroupElement[6].role))
    #         ui.group0_Device6_Mac0_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[6].macAddr[0])
    #         ui.group0_Device6_Mac1_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[6].macAddr[1])
    #         ui.group0_Device6_Mac2_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[6].macAddr[2])
    #         ui.group0_Device6_Mac3_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[6].macAddr[3])
    #         ui.group0_Device6_Mac4_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[6].macAddr[4])
    #         ui.group0_Device6_Mac5_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[6].macAddr[5])
    #         i -= 1
    #     if i > 0:
    #         ui.group0_Device7_CheckBox.setChecked(True)
    #         ui.group0_Device7_Channel_LineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[7].channel)
    #         ui.group0_Device7_Role_LineEdit.setText(str(groupTotalInfo.stGroupInfo[0].stGroupElement[7].role))
    #         ui.group0_Device7_Mac0_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[7].macAddr[0])
    #         ui.group0_Device7_Mac1_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[7].macAddr[1])
    #         ui.group0_Device7_Mac2_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[7].macAddr[2])
    #         ui.group0_Device7_Mac3_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[7].macAddr[3])
    #         ui.group0_Device7_Mac4_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[7].macAddr[4])
    #         ui.group0_Device7_Mac5_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[7].macAddr[5])
    #         i -= 1
    #     if i > 0:
    #         ui.group0_Device8_CheckBox.setChecked(True)
    #         ui.group0_Device8_Channel_LineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[8].channel)
    #         ui.group0_Device8_Role_LineEdit.setText(str(groupTotalInfo.stGroupInfo[0].stGroupElement[8].role))
    #         ui.group0_Device8_Mac0_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[8].macAddr[0])
    #         ui.group0_Device8_Mac1_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[8].macAddr[1])
    #         ui.group0_Device8_Mac2_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[8].macAddr[2])
    #         ui.group0_Device8_Mac3_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[8].macAddr[3])
    #         ui.group0_Device8_Mac4_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[8].macAddr[4])
    #         ui.group0_Device8_Mac5_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[0].stGroupElement[8].macAddr[5])
    #         i -= 1
    #
    # if groupTotalInfo.numGroup >= 2:
    #     ui.group1_CheckBox.setChecked(True)
    #
    #     if groupTotalInfo.stGroupInfo[1].chCfgType == CH_CFG_TYPE_MONO:
    #         ui.group1_Mono_Radio.setChecked(True)
    #     elif groupTotalInfo.stGroupInfo[1].chCfgType == CH_CFG_TYPE_STEREO:
    #         ui.group1_Stereo_Radio.setChecked(True)
    #     elif groupTotalInfo.stGroupInfo[1].chCfgType == CH_CFG_TYPE_3_1_2:
    #         ui.group1_312_Radio.setChecked(True)
    #     elif groupTotalInfo.stGroupInfo[1].chCfgType == CH_CFG_TYPE_5_1:
    #         ui.group1_51_Radio.setChecked(True)
    #     elif groupTotalInfo.stGroupInfo[0].chCfgType == CH_CFG_TYPE_5_1_2:
    #         ui.group1_512_Radio.setChecked(True)
    #     elif groupTotalInfo.stGroupInfo[1].chCfgType == CH_CFG_TYPE_7_1:
    #         ui.group1_71_Radio.setChecked(True)
    #     elif groupTotalInfo.stGroupInfo[1].chCfgType == CH_CFG_TYPE_7_1_2:
    #         ui.group1_712_Radio.setChecked(True)
    #     elif groupTotalInfo.stGroupInfo[1].chCfgType == CH_CFG_TYPE_7_1_4:
    #         ui.group1_714_Radio.setChecked(True)
    #
    #     if groupTotalInfo.stGroupInfo[1].tpCfgType == TP_CFG_MULTI_CHANNEL:
    #         ui.group1_MultiCh_Radio.setChecked(True)
    #     elif groupTotalInfo.stGroupInfo[1].tpCfgType == TP_CFG_MULTI_ROOM:
    #         ui.group1_MultiRo_Radio.setChecked(True)
    #     elif groupTotalInfo.stGroupInfo[1].tpCfgType == TP_CFG_CONCURRENT:
    #         ui.group1_Concurr_Radio.setChecked(True)
    #
    #     ui.group1_Name_LineEdit.setText(groupTotalInfo.stGroupInfo[1].groupName)
    #
    #     i = groupTotalInfo.stGroupInfo[1].numSpeaker
    #     if i > 0:
    #         ui.group1_Device0_CheckBox.setChecked(True)
    #         ui.group1_Device0_Channel_LineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[0].channel)
    #         ui.group1_Device0_Role_LineEdit.setText(str(groupTotalInfo.stGroupInfo[1].stGroupElement[0].role))
    #         ui.group1_Device0_Mac0_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[0].macAddr[0])
    #         ui.group1_Device0_Mac1_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[0].macAddr[1])
    #         ui.group1_Device0_Mac2_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[0].macAddr[2])
    #         ui.group1_Device0_Mac3_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[0].macAddr[3])
    #         ui.group1_Device0_Mac4_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[0].macAddr[4])
    #         ui.group1_Device0_Mac5_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[0].macAddr[5])
    #         i -= 1
    #     if i > 0:
    #         ui.group1_Device1_CheckBox.setChecked(True)
    #         ui.group1_Device1_Channel_LineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[1].channel)
    #         ui.group1_Device1_Role_LineEdit.setText(str(groupTotalInfo.stGroupInfo[1].stGroupElement[1].role))
    #         ui.group1_Device1_Mac0_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[1].macAddr[0])
    #         ui.group1_Device1_Mac1_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[1].macAddr[1])
    #         ui.group1_Device1_Mac2_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[1].macAddr[2])
    #         ui.group1_Device1_Mac3_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[1].macAddr[3])
    #         ui.group1_Device1_Mac4_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[1].macAddr[4])
    #         ui.group1_Device1_Mac5_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[1].macAddr[5])
    #         i -= 1
    #     if i > 0:
    #         ui.group1_Device2_CheckBox.setChecked(True)
    #         ui.group1_Device2_Channel_LineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[2].channel)
    #         ui.group1_Device2_Role_LineEdit.setText(str(groupTotalInfo.stGroupInfo[1].stGroupElement[2].role))
    #         ui.group1_Device2_Mac0_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[2].macAddr[0])
    #         ui.group1_Device2_Mac1_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[2].macAddr[1])
    #         ui.group1_Device2_Mac2_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[2].macAddr[2])
    #         ui.group1_Device2_Mac3_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[2].macAddr[3])
    #         ui.group1_Device2_Mac4_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[2].macAddr[4])
    #         ui.group1_Device2_Mac5_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[2].macAddr[5])
    #         i -= 1
    #     if i > 0:
    #         ui.group1_Device3_CheckBox.setChecked(True)
    #         ui.group1_Device3_Channel_LineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[3].channel)
    #         ui.group1_Device3_Role_LineEdit.setText(str(groupTotalInfo.stGroupInfo[1].stGroupElement[3].role))
    #         ui.group1_Device3_Mac0_lineEdit.setText(str("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[3].macAddr[0]))
    #         ui.group1_Device3_Mac1_lineEdit.setText(str("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[3].macAddr[1]))
    #         ui.group1_Device3_Mac2_lineEdit.setText(str("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[3].macAddr[2]))
    #         ui.group1_Device3_Mac3_lineEdit.setText(str("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[3].macAddr[3]))
    #         ui.group1_Device3_Mac4_lineEdit.setText(str("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[3].macAddr[4]))
    #         ui.group1_Device3_Mac5_lineEdit.setText(str("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[3].macAddr[5]))
    #         i -= 1
    #     if i > 0:
    #         ui.group1_Device4_CheckBox.setChecked(True)
    #         ui.group1_Device4_Channel_LineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[4].channel)
    #         ui.group1_Device4_Role_LineEdit.setText(str(groupTotalInfo.stGroupInfo[1].stGroupElement[4].role))
    #         ui.group1_Device4_Mac0_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[4].macAddr[0])
    #         ui.group1_Device4_Mac1_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[4].macAddr[1])
    #         ui.group1_Device4_Mac2_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[4].macAddr[2])
    #         ui.group1_Device4_Mac3_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[4].macAddr[3])
    #         ui.group1_Device4_Mac4_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[4].macAddr[4])
    #         ui.group1_Device4_Mac5_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[4].macAddr[5])
    #         i -= 1
    #     if i > 0:
    #         ui.group1_Device5_CheckBox.setChecked(True)
    #         ui.group1_Device5_Channel_LineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[5].channel)
    #         ui.group1_Device5_Role_LineEdit.setText(str(groupTotalInfo.stGroupInfo[1].stGroupElement[5].role))
    #         ui.group1_Device5_Mac0_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[5].macAddr[0])
    #         ui.group1_Device5_Mac1_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[5].macAddr[1])
    #         ui.group1_Device5_Mac2_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[5].macAddr[2])
    #         ui.group1_Device5_Mac3_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[5].macAddr[3])
    #         ui.group1_Device5_Mac4_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[5].macAddr[4])
    #         ui.group1_Device5_Mac5_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[5].macAddr[5])
    #         i -= 1
    #     if i > 0:
    #         ui.group1_Device6_CheckBox.setChecked(True)
    #         ui.group1_Device6_Channel_LineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[6].channel)
    #         ui.group1_Device6_Role_LineEdit.setText(str(groupTotalInfo.stGroupInfo[1].stGroupElement[6].role))
    #         ui.group1_Device6_Mac0_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[6].macAddr[0])
    #         ui.group1_Device6_Mac1_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[6].macAddr[1])
    #         ui.group1_Device6_Mac2_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[6].macAddr[2])
    #         ui.group1_Device6_Mac3_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[6].macAddr[3])
    #         ui.group1_Device6_Mac4_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[6].macAddr[4])
    #         ui.group1_Device6_Mac5_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[6].macAddr[5])
    #         i -= 1
    #     if i > 0:
    #         ui.group1_Device7_CheckBox.setChecked(True)
    #         ui.group1_Device7_Channel_LineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[7].channel)
    #         ui.group1_Device7_Role_LineEdit.setText(str(groupTotalInfo.stGroupInfo[1].stGroupElement[7].role))
    #         ui.group1_Device7_Mac0_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[7].macAddr[0])
    #         ui.group1_Device7_Mac1_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[7].macAddr[1])
    #         ui.group1_Device7_Mac2_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[7].macAddr[2])
    #         ui.group1_Device7_Mac3_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[7].macAddr[3])
    #         ui.group1_Device7_Mac4_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[7].macAddr[4])
    #         ui.group1_Device7_Mac5_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[7].macAddr[5])
    #         i -= 1
    #     if i > 0:
    #         ui.group1_Device8_CheckBox.setChecked(True)
    #         ui.group1_Device8_Channel_LineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[8].channel)
    #         ui.group1_Device8_Role_LineEdit.setText(str(groupTotalInfo.stGroupInfo[1].stGroupElement[8].role))
    #         ui.group1_Device8_Mac0_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[8].macAddr[0])
    #         ui.group1_Device8_Mac1_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[8].macAddr[1])
    #         ui.group1_Device8_Mac2_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[8].macAddr[2])
    #         ui.group1_Device8_Mac3_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[8].macAddr[3])
    #         ui.group1_Device8_Mac4_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[8].macAddr[4])
    #         ui.group1_Device8_Mac5_lineEdit.setText("%02x"%groupTotalInfo.stGroupInfo[1].stGroupElement[8].macAddr[5])
    #         i -= 1


def get_GroupVolumeRet_Handler(ui, rcvData):
    groupVolumeInfo = getGroupVolumeInfo_from_Vector(rcvData[1:])
    activateIdx = getActivateIdx()

    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += "Get Group Volume done"
    ui.log_TextBrowser.append(log)

    init_groupVolume(ui)
    exec("ui.group%d_groupVolume_LineEdit.setText(\"%s\")"%(activateIdx,str(groupVolumeInfo.groupVolume)))
    ui_context.update_group_info_group_vol(activateIdx,groupVolumeInfo.groupVolume)

    gr_context = ui_context.Get_active_group_info(getActivateIdx())

    row_idx = 0
    for devIdx in range(0,groupVolumeInfo.numSpeaker):
        exec("ui.group%d_Device%d_Vol_LineEdit.setText(\"%s\")"%(activateIdx, devIdx, str(groupVolumeInfo.volume[devIdx])))
        ui_context.Update_dev_info_in_group(gr_id=activateIdx,dev_id=devIdx ,vol=groupVolumeInfo.volume[devIdx])
        # Update Table
        str_ch = ""
        for ch in gr_context['dev_info'][devIdx]['ch']:
            str_ch += ch.upper() +'/'
        ui.WoWIF.TBL_UI.Update_AudioPlay_Speaker(row=row_idx, id=devIdx, str_ch=str_ch[:-1],
                                           bit=None, samp = None, str_vol=str(groupVolumeInfo.volume[devIdx]))
        row_idx += 1

    # if activateIdx == 0x00:
    #     ui.group0_groupVolume_LineEdit.setText(str(groupVolumeInfo.groupVolume))
    #
    #     i = 0
    #     if i < groupVolumeInfo.numSpeaker:
    #         ui.group0_Device0_Vol_LineEdit.setText(str(groupVolumeInfo.volume[0]))
    #         i += 1
    #     if i < groupVolumeInfo.numSpeaker:
    #         ui.group0_Device1_Vol_LineEdit.setText(str(groupVolumeInfo.volume[1]))
    #         i += 1
    #     if i < groupVolumeInfo.numSpeaker:
    #         ui.group0_Device2_Vol_LineEdit.setText(str(groupVolumeInfo.volume[2]))
    #         i += 1
    #     if i < groupVolumeInfo.numSpeaker:
    #         ui.group0_Device3_Vol_LineEdit.setText(str(groupVolumeInfo.volume[3]))
    #         i += 1
    #     if i < groupVolumeInfo.numSpeaker:
    #         ui.group0_Device4_Vol_LineEdit.setText(str(groupVolumeInfo.volume[4]))
    #         i += 1
    #     if i < groupVolumeInfo.numSpeaker:
    #         ui.group0_Device5_Vol_LineEdit.setText(str(groupVolumeInfo.volume[5]))
    #         i += 1
    #     if i < groupVolumeInfo.numSpeaker:
    #         ui.group0_Device6_Vol_LineEdit.setText(str(groupVolumeInfo.volume[6]))
    #         i += 1
    #     if i < groupVolumeInfo.numSpeaker:
    #         ui.group0_Device7_Vol_LineEdit.setText(str(groupVolumeInfo.volume[7]))
    #         i += 1
    #     if i < groupVolumeInfo.numSpeaker:
    #         ui.group0_Device8_Vol_LineEdit.setText(str(groupVolumeInfo.volume[8]))
    #         i += 1
    #
    # else:
    #     ui.group1_groupVolume_LineEdit.setText(str(groupVolumeInfo.groupVolume))
    #
    #     i = 0
    #     if i < groupVolumeInfo.numSpeaker:
    #         ui.group1_Device0_Vol_LineEdit.setText(str(groupVolumeInfo.volume[0]))
    #         i += 1
    #     if i < groupVolumeInfo.numSpeaker:
    #         ui.group1_Device1_Vol_LineEdit.setText(str(groupVolumeInfo.volume[1]))
    #         i += 1
    #     if i < groupVolumeInfo.numSpeaker:
    #         ui.group1_Device2_Vol_LineEdit.setText(str(groupVolumeInfo.volume[2]))
    #         i += 1
    #     if i < groupVolumeInfo.numSpeaker:
    #         ui.group1_Device3_Vol_LineEdit.setText(str(groupVolumeInfo.volume[3]))
    #         i += 1
    #     if i < groupVolumeInfo.numSpeaker:
    #         ui.group1_Device4_Vol_LineEdit.setText(str(groupVolumeInfo.volume[4]))
    #         i += 1
    #     if i < groupVolumeInfo.numSpeaker:
    #         ui.group1_Device5_Vol_LineEdit.setText(str(groupVolumeInfo.volume[5]))
    #         i += 1
    #     if i < groupVolumeInfo.numSpeaker:
    #         ui.group1_Device6_Vol_LineEdit.setText(str(groupVolumeInfo.volume[6]))
    #         i += 1
    #     if i < groupVolumeInfo.numSpeaker:
    #         ui.group1_Device7_Vol_LineEdit.setText(str(groupVolumeInfo.volume[7]))
    #         i += 1
    #     if i < groupVolumeInfo.numSpeaker:
    #         ui.group1_Device8_Vol_LineEdit.setText(str(groupVolumeInfo.volume[8]))
    #         i += 1

def get_WirelessInfoRet_Handler(ui, rcvData):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += "Wireless Info Ret received"
    ui.log_TextBrowser.append(log)

    ui_context.Update_active_group_meas_info(clr_flag=True)
    gr_context = ui_context.Get_active_group_info(getActivateIdx())
    offset = 1
    totalRssi = []
    totalnPlayback = []
    totalnDrop = []
    totalnRcv = []
    totalnLoss = []
    totalsrtt = []
    totalLoss = []
    totalDrop = []
    print(rcvData)
    for dev_id in gr_context['dev_info']:
        rssi = int.from_bytes(rcvData[offset:offset+4], 'little', signed=True)
        offset += 4
        nPlayback = int.from_bytes(rcvData[offset:offset + 4], 'little')
        offset += 4
        nDrop = int.from_bytes(rcvData[offset:offset + 4], 'little')
        offset += 4
        nRcv = int.from_bytes(rcvData[offset:offset + 4], 'little')
        offset += 4
        nLoss = int.from_bytes(rcvData[offset:offset + 4], 'little')
        offset += 4
        srtt = int.from_bytes(rcvData[offset:offset + 4], 'little')
        offset += 4

        [dropPercent, lossPercent] = ui_context.Update_active_group_meas_info(dev_id=dev_id, rssi=rssi,
                                          nPlayback=nPlayback, nDrop=nDrop, nRcv=nRcv, nLoss=nLoss, srtt=srtt)

        # Update SPK_UI for each speaker
        if gr_context['dev_info'][dev_id]['role'] != '0':
            for ch in gr_context['dev_info'][dev_id]['ch']:
                ui.WoWIF.SPK_UI.Update_Latency_Value(ch,srtt)
                ui.WoWIF.SPK_UI.Update_RSSI_Value(ch,rssi)
                ui.WoWIF.SPK_UI.Update_Loss_Value(ch,lossPercent)
                ui.WoWIF.SPK_UI.Update_Drop_Value(ch,dropPercent)

                totalRssi.append(rssi)
                totalnPlayback.append(nPlayback)
                totalnDrop.append(nDrop)
                totalnRcv.append(nRcv)
                totalnLoss.append(nLoss)
                totalsrtt.append(srtt)
                if lossPercent is not -1 : totalLoss.append(lossPercent)
                if dropPercent is not -1 : totalDrop.append(dropPercent)

    # print("[RSSI at Slaves]")
    # print(totalRssi)
    # print("[Number of Playback at Slaves]")
    # print(totalnPlayback)
    # print("[Number of Playback Drop at Slaves]")
    # print(totalnDrop)
    # print("[Number of Received Packet at Slaves]")
    # print(totalnRcv)
    # print("[Number of Loss Packet at Slaves]")
    # print(totalnLoss)
    # print("[SRTT at Slaves]")
    # print(totalsrtt)
    # print("[Percentage of packet loss at Slaves]")
    # print(totalLoss)
    # print("[Percentage of Playback drop at Slaves]")
    # print(totalDrop)

    # Update TBL_UI
    if len(totalRssi)>0:
        ui.WoWIF.TBL_UI.Update_NetworkStat(RSSI = [min(totalRssi), mean(totalRssi),max(totalRssi)])
    if len(totalLoss)>0:
        ui.WoWIF.TBL_UI.Update_NetworkStat(LossRate= [min(totalLoss), mean(totalLoss),max(totalLoss)])
    if len(totalDrop)>0:
        ui.WoWIF.TBL_UI.Update_WoWPlay(Drop = [min(totalDrop), mean(totalDrop), max(totalDrop)])


def set_GroupInfoRsp_Handler(ui, rcvData):
    if rcvData[1] == 0x00:
        log = datetime.datetime.now().strftime("[%H:%M:%S]")
        log += " Set Group Info done"
        ui.log_TextBrowser.append(log)
        groupTotalInfo = getSetGroupInfo()

        ui_context.update_group_info_cmn(clr_flag=True)
        gr_bitmap = groupTotalInfo.numGroup
        for idx in range(0, 2):
            if gr_bitmap & (1<<idx):
                gr_idx = idx
            else:
                continue

            chCfgType = groupTotalInfo.stGroupInfo[gr_idx].chCfgType
            tpCfgType = groupTotalInfo.stGroupInfo[gr_idx].tpCfgType
            groupName = groupTotalInfo.stGroupInfo[gr_idx].groupName

            ui_context.update_group_info_cmn(gr_id=gr_idx, ch_cfg=chCfgType, topology=tpCfgType, group_name=groupName)

            ui_context.Update_dev_info_in_group(clr_flag=True,gr_id=gr_idx)
            for dev_idx in range(0, groupTotalInfo.stGroupInfo[gr_idx].numSpeaker):
                channel = groupTotalInfo.stGroupInfo[gr_idx].stGroupElement[dev_idx].channel
                role = str(groupTotalInfo.stGroupInfo[gr_idx].stGroupElement[dev_idx].role)

                macAddr = []
                for addr_Idx in range(0, 6):
                    addrPart = groupTotalInfo.stGroupInfo[gr_idx].stGroupElement[dev_idx].macAddr[addr_Idx]
                    macAddr.append(addrPart)

                ui_context.Update_dev_info_in_group(sel_flag=True, gr_id=gr_idx, dev_id=dev_idx, macAddr=macAddr,
                                                    role=role, ch=channel)
    else:
        log = datetime.datetime.now().strftime("[%H:%M:%S]")
        log += " Set Group Info failed. Reason: "
        log += str(rcvData[1])
        ui.log_TextBrowser.append(log)


def groupActivateRsp_Handler(ui, rcvData):
    if rcvData[1] == 0x00:
        log = datetime.datetime.now().strftime("[%H:%M:%S]")
        log += " Group Activation done "
        ui.log_TextBrowser.append(log)

        # Update GUI
        gr_context = ui_context.Get_active_group_info(getActivateIdx())
        ui.WoWIF.SPK_UI.Update_Slave_Status(True)
        for dev in gr_context['dev_info'].values():
            if dev['role'] == '0':
                txt = 'Master - '
                for ch in dev['ch']:
                    txt += ch
                    txt += '/'
                ui.WoWIF.SPK_UI.Master_Role.setText(txt[:-1])
                ui.WoWIF.SPK_UI.Update_Group_WiFi('Master', 'start')
                continue
            else:
                # Speaker Group Enable
                for ch in dev['ch']:
                    ui.WoWIF.SPK_UI.Update_Group_Status(ch, True)
                    # Initialize Values
                    ui.WoWIF.SPK_UI.Update_Latency_Value(ch, '-')
                    ui.WoWIF.SPK_UI.Update_RSSI_Value(ch, '-')
                    ui.WoWIF.SPK_UI.Update_Loss_Value(ch, '-')
                    ui.WoWIF.SPK_UI.Update_Group_WiFi(ch, 'start')
        ui.WoWIF.SPK_UI.Update_Comment('Activated')
        ui.WoWIF.TBL_UI.Update_WoWPlay(state='Activation')
        ui.Timer.start(Timeout_Time)
    else:
        log = datetime.datetime.now().strftime("[%H:%M:%S]")
        log += " Group Activation failed. Reason: "
        log += str(rcvData[1])
        ui.log_TextBrowser.append(log)

def groupDeactivateRsp_Handler(ui, rcvData):
    activateInfo = S_GROUP_ACTIVATE_INFO()

    if rcvData[1] == 0x00:
        activateInfo = S_GROUP_ACTIVATE_INFO()

        log = datetime.datetime.now().strftime("[%H:%M:%S]")
        log += " Group Deactivation done"
        ui.log_TextBrowser.append(log)

        # Update GUI
        gr_context = ui_context.Get_active_group_info(getActivateIdx())
        ui.WoWIF.SPK_UI.Update_Group_WiFi('Master','disable')
        for dev in gr_context['dev_info'].values():
            # Speaker Group Enable
            for ch in dev['ch']:
                ui.WoWIF.SPK_UI.Update_Group_Status(ch, 0)
                # Initialize Values
                # ui.WoWIF.SPK_UI.Update_Latency_Value(ch, '-')
                # ui.WoWIF.SPK_UI.Update_RSSI_Value(ch, '-')
                # ui.WoWIF.SPK_UI.Update_Loss_Value(ch, '-')
                # ui.WoWIF.SPK_UI.Update_Drop_Value(ch, '-')
                ui.WoWIF.SPK_UI.Update_Group_EQ(ch,'disable')
                ui.WoWIF.SPK_UI.Update_Group_WiFi(ch,'disable')
        ui.WoWIF.SPK_UI.Update_Slave_Status(0)
        ui.WoWIF.SPK_UI.Update_Comment("Deactivated")
        ui.WoWIF.SPK_UI.Master_Role.setText("Master")
        ui.WoWIF.SPK_UI.Update_Group_EQ('Master', 'disable')
        ui.WoWIF.TBL_UI.Update_WoWPlay(state="Deactivation")
    else:
        log = datetime.datetime.now().strftime("[%H:%M:%S]")
        log += " Group Deactivation failed. Reason: "
        log += str(rcvData[1])
        ui.log_TextBrowser.append(log)

def groupPlayRsp_Handler(ui, rcvData):
    if rcvData[1] == 0x00:
        log = datetime.datetime.now().strftime("[%H:%M:%S]")
        log += " Group Play/Pause done"
        ui.log_TextBrowser.append(log)

        PlayPause = getPlayPauseInfo()
        print(PlayPause)
        ui_context.update_play_status(PlayPause)
        if PlayPause >= 1:
            ui.WoWIF.TBL_UI.Update_WoWPlay(state="Play")
        else:
            ui.WoWIF.TBL_UI.Update_WoWPlay(state="Pause")
            ui.WoWIF.SPK_UI.Update_Comment("Pause")
            # Update GUI - EQ Mark
            gr_context = ui_context.Get_active_group_info(getActivateIdx())
            if ui.WoWIF.SPK_UI.Slaves.isEnabled() is True:
                for dev in gr_context['dev_info'].values():
                    if dev['role'] == '0':
                        ui.WoWIF.SPK_UI.Update_Group_EQ('Master', 'stop')
                    else:
                        for ch in dev['ch']:
                            ui.WoWIF.SPK_UI.Update_Group_EQ(ch, 'stop')

    else:
        log = datetime.datetime.now().strftime("[%H:%M:%S]")
        log += " Group Play/Pause failed. Reason: "
        log += str(rcvData[1])
        ui.log_TextBrowser.append(log)

def set_GroupAbsVolumeRsp_Handler(ui, rcvData):
    if rcvData[1] == 0x00:
        log = datetime.datetime.now().strftime("[%H:%M:%S]")
        log += " Set Group Abs Volume done"
        ui.log_TextBrowser.append(log)
    else:
        log = datetime.datetime.now().strftime("[%H:%M:%S]")
        log += " Set Group Abs Volume failed. Reason: "
        log += str(rcvData[1])
        ui.log_TextBrowser.append(log)
    ui.send_remain_volume_req()

    # TODO: To Update Volume in the GUI, get_GroupVolume is sent automatically


def set_GroupRelVolumeRsp_Handler(ui, rcvData):
    if rcvData[1] == 0x00:
        log = datetime.datetime.now().strftime("[%H:%M:%S]")
        log += " Set Group Rel Volume done"
        ui.log_TextBrowser.append(log)
    else:
        log = datetime.datetime.now().strftime("[%H:%M:%S]")
        log += " Set Group Rel Volume failed. Reason: "
        log += str(rcvData[1])
        ui.log_TextBrowser.append(log)

    # TODO: To Update Volume in the GUI, get_GroupVolume is sent automatically

def set_GroupMuteRsp_Handler(ui, rcvData):
    mute_status = getMuteUnMuteInfo()
    if rcvData[1] == 0x00:
        log = datetime.datetime.now().strftime("[%H:%M:%S]")
        log += "Set Group Mute done" if mute_status is 0 else "Set Group Unmute done"
        ui.log_TextBrowser.append(log)

        ui_context.update_mute_status(mute_status)

        # Update GUI
        # Mute - Update Table - Volume = Mute , DB is not updated
        gr_context = ui_context.Get_active_group_info(getActivateIdx())
        row_idx = 0
        if mute_status is 0:
            # Update Table
            for devIdx in gr_context['dev_info']:
                str_ch = ""
                for ch in gr_context['dev_info'][devIdx]['ch']:
                    str_ch += ch.upper() + '/'
                ui.WoWIF.TBL_UI.Update_AudioPlay_Speaker(row=row_idx, id=devIdx, str_ch=str_ch[:-1],
                                                       bit=None, samp=None,
                                                       str_vol='Mute')
                row_idx += 1
        else:
            # Unmute - Update Table - Volume is restored by DB
            # Update Table
            for devIdx in gr_context['dev_info']:
                str_ch = ""
                for ch in gr_context['dev_info'][devIdx]['ch']:
                    str_ch += ch.upper() + '/'
                ui.WoWIF.TBL_UI.Update_AudioPlay_Speaker(row=row_idx, id=devIdx, str_ch=str_ch[:-1],
                                                         bit=None, samp=None,
                                                         str_vol=str(gr_context['dev_info'][devIdx]['vol']) )
                row_idx += 1
    else:
        log = datetime.datetime.now().strftime("[%H:%M:%S]")
        log += " Set Group Mute/Unmute failed. Reason: "
        log += str(rcvData[1])
        ui.log_TextBrowser.append(log)


def volumeChangeInd_Handler(ui, rcvData):
    activateInfo = S_GROUP_ACTIVATE_INFO()

    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += " Group Volume Changed by speaker index "
    log += str(rcvData[1])
    log += ". Volume is "
    log += str(rcvData[2])
    ui.log_TextBrowser.append(log)

    vol = int.from_bytes(rcvData[2],'little')
    dev_id = int.from_bytes(rcvData[1],'little')

    exec("ui.group%d_Device%d_Vol_LineEdit.setText(\"%s\")"%(activateInfo.groupIdx,dev_id,str(vol)))
    # Update ui_context
    ui_context.Update_dev_info_in_group(vol=vol, gr_id=activateInfo.groupIdx, dev_id=dev_id)

    # Update GUI
    gr_context = ui_context.Get_active_group_info(getActivateIdx())
    row_idx = 0
    for dev_id in gr_context['dev_info']:
        # Update Table
        gr_context['dev_info'][dev_id]['ch']    # need to convert bitmap to channel info
        ui.WoWIF.TBL_UI.Update_AudioPlay_Speaker(row=row_idx, id=dev_id, str_ch=None, bit=None, samp = None, str_vol=None)
        row_idx += 1


def groupPlayInd_Handler(ui, rcvData):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    cmd = []
    if rcvData[1] == 0x00:  # Pause triggered by Slave device
        log += "Group Play Ind received - Pause"
        ui_context.update_play_status(0)
        cmd = 'stop'
        ui.WoWIF.SPK_UI.Update_Comment('Pause')
    elif rcvData[1] == 0x01:   # Play triggered by Slave device
        log += "Group Play Ind received - Play"
        ui_context.update_play_status(1)
        cmd = 'start'
        ui.WoWIF.SPK_UI.Update_Comment('Play')
    else:
        log += "Group Play Ind received - Unknown Command"
        log += str(rcvData[1])

    ui.log_TextBrowser.append(log)

    # Update GUI - EQ Mark
    if cmd is not None:
        gr_context = ui_context.Get_active_group_info(getActivateIdx())
        if ui.WoWIF.SPK_UI.Slaves.isEnabled() is True:
            for dev in gr_context['dev_info'].values():
                for ch in dev['ch']:
                    ui.WoWIF.SPK_UI.Update_Group_EQ(ch, cmd)

def groupStatusInd_Handler(ui, rcvData):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += "Group Status Ind received. Code: "
    log += str(rcvData[1])
    log += ". Speaker Index: "
    log += str(rcvData[2])
    ui.log_TextBrowser.append(log)

def audioPlaybackInfoInd_Handler(ui, rcvData):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += "Audio Playback Info Ind received "
    ui.log_TextBrowser.append(log)

    # Update GUI - EQ Mark
    gr_context = ui_context.Get_active_group_info(getActivateIdx())
    if ui.WoWIF.SPK_UI.Slaves.isEnabled() is True:
        for dev in gr_context['dev_info'].values():
            if dev['role'] == '0':
                ui.WoWIF.SPK_UI.Update_Group_EQ('Master','start')
            else:
                for ch in dev['ch']:
                    ui.WoWIF.SPK_UI.Update_Group_EQ(ch, 'start')

    bitDepth        = int.from_bytes(rcvData[1:5], 'little')
    enum_sampleRate = int.from_bytes(rcvData[5:9], 'little')
    totalAudioCh    = int.from_bytes(rcvData[9:13], 'little')
    playbackLatency = int.from_bytes(rcvData[13:17], 'little')
    sampleRate = AUDIO_SAMPLE_ENUM_TO_KHZ[enum_sampleRate]

    ui.WoWIF.TBL_UI.Update_AudioSource(bitDepth, sampleRate, CH_CFG_TYPE_TO_STRING[totalAudioCh][1])
    ui.WoWIF.TBL_UI.Update_WoWPlay(state='Play', latency=playbackLatency)
    ui.WoWIF.SPK_UI.Update_Comment('Playback Latency\n%d ms'%(playbackLatency))

    # Update Channel Information in the Audio Play Information
    row = 0
    IDs = {"0":"","1":""}
    for devid in gr_context['dev_info']:
        IDs[gr_context['dev_info'][devid]['role']] += str(devid)+(" / ")
        str_ch = ""
        for ch in gr_context['dev_info'][devid]['ch']:
            str_ch += ch.upper() + '/'
        ui.WoWIF.TBL_UI.Update_AudioPlay_Speaker(row=row, id=devid, str_ch=str_ch[:-1],
                                                 bit=bitDepth, samp = sampleRate,
                                                 str_vol=str(gr_context['dev_info'][devid]['vol']) )
        row += 1

    ui.WoWIF.TBL_UI.Update_AudioPlay_Config(CH_CFG      = CH_CFG_TYPE_TO_STRING[totalAudioCh][1],
                                            Local_CH    =IDs["0"][:-3],
                                            Wireless_CH =IDs["1"][:-3] )


def wifiChannelInfoInd_Handler(ui, rcvData):
    log = datetime.datetime.now().strftime("[%H:%M:%S]")
    log += "WiFi Channel Info Ind received "
    ui.log_TextBrowser.append(log)
    wifiChannel = int.from_bytes(rcvData[1:4], 'little')
    ui.WoWIF.TBL_UI.Update_NetworkStat(WiFi_Ch=wifiChannel)
    ui.WoWIF.TBL_UI.Update_PrintDebugView(log)
