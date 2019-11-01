import sys
import socket
import datetime
from remote_context import *
from remote_data_convert import *
from remote_server_handler import *

ui_signal = None

def setUiSignal(signal) :
    global ui_signal, server_status
    ui_signal = signal
    server_status = True

def stopPythonServer() :
    global server_status
    server_status = False

def pythonServer(ui):
    global sock, ui_signal,server_status

    print("Python Server Starts")

    while server_status:
        rcvData, cppAddr = sock.recvfrom(BUF_SIZE)
        print("rcv: ", rcvData)
        ui_signal.emit(rcvData)