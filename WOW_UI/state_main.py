from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import UI_Placement
import UI_Table
import datetime

class state_main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('WoWPlay Info')
        self.setGeometry(0,0,1600,900)
        self.SPK_GUI = QtWidgets.QWidget()
        self.SPK_UI = UI_Placement.Ui_SPK_GUI()
        self.SPK_UI.setupUi(self.SPK_GUI)
        self.SPK_GUI.show()

        self.TBL_GUI = QtWidgets.QWidget()
        self.TBL_UI = UI_Table.Ui_Form()
        self.TBL_UI.setupUi(self.TBL_GUI)
        self.TBL_GUI.show()

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.SPK_GUI)
        hbox.addWidget(self.TBL_GUI)

        self.setLayout(hbox)
        self.show()

    def UpdateUI_Comment(self,txt):
        self.SPK_UI.Update_Comment(txt)
    def UpdateUI_WiFi_GIF(self,role,cmd):
        cmds = ["start", "stop", "disable"]
        if cmd in cmds:
            self.SPK_UI.Update_Group_WiFi(role,cmd)
    def UpdateUI_Status(self,role,value):
        if role is 'Slave':
            self.SPK_UI.Update_Slave_Status(value)
        else:
            self.SPK_UI.Update_Group_Status(role,value)
    def UpdateUI_Value(self,item,role,value):
        if item is 'Latency':
            self.SPK_UI.Update_Latency_Value(role,value)
        elif item is 'RSSI':
            self.SPK_UI.Update_RSSI_Value(role, value)
        elif item is 'Loss':
            self.SPK_UI.Update_Loss_Value(role, value)
        else:
            print("Invalid Input")
    def UpdateUI_EQ_GIF(self,role,cmd):
        cmds = ["start" , "stop" , "disable"]
        if cmd in cmds:
            self.SPK_UI.Update_Group_EQ(role, cmd)

    def UpdateTBL_AudioSourceInfo(self,bit_depth,sampling_rate,Total_Ch):
        self.TBL_UI.Update_AudioSource(bit_depth,sampling_rate,Total_Ch)
    def UpdateTBL_AudioPlayConfig(self,Total_Ch, Local_Ch, Remote_Ch):
        self.TBL_UI.Update_AudioPlay_Config(Total_Ch,Local_Ch,Remote_Ch)
    def UpdateTBL_WoWPlayInfo(self,CurState,Latency):
        self.TBL_UI.Update_WoWPlay(CurState,Latency)
    def UpdateTBL_NetworkStatus(self,WiFi_Ch, RSSI, LossRate):
        self.TBL_UI.Update_NetworkStat(WiFi_Ch,RSSI,LossRate)
    def UpdateTBL_PrintDebugView(self,log):
        self.TBL_UI.Update_PrintDebugView(log)
    def UpdateTBL_AudioSpkaerInfo(self):
        pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = state_main()
    sys.exit(app.exec_())