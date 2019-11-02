import sys
import socket
from select import select
import datetime
from threading import Thread
from remote_context import *


class WowPlayRemoteServer(Thread) :
    def __init__(self, server_port):
        Thread.__init__(self)
        self.running = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('0.0.0.0', server_port))
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.read_handler = {
            SET_GROUP_ABS_VOLUME_REQ : self.group_volume_req,
            GET_GROUP_VOLUME : self.get_group_volume
        }

    def group_volume_req(self, recv_data, from_addr):
        if len(recv_data) < 3 :
            return

        device_id, volume = recv_data[1], recv_data[2]
        print('Read Volume Req - Device Id(%d), Volume(%d)' % (device_id, volume))
        send_byte = bytes([SET_GROUP_ABS_VOLUME_RSP, 0x00])
        self.socket.sendto(send_byte, from_addr)

    def get_group_volume(self, recv_data, from_addr):
        if len(recv_data) < 1 :
            return

        print('Get Volume Req')
        #send_byte = bytes([SET_GROUP_ABS_VOLUME_RSP, 0x00])
        #self.socket.sendto(send_byte, from_addr)

    def server_stop(self):
        self.running = False

    def run(self):
        while self.running:
            read_sock_list, write_sock, err_sock = select([self.socket], [], [], 1)
            for read_sock in read_sock_list :

                rcvData, addr = read_sock.recvfrom(BUF_SIZE)
                if len(rcvData) < 1 : continue

                data_type =rcvData[0]
                print('Read Data : %s'%("".join(["%02X"%v for v in rcvData])))

                if data_type in self.read_handler :
                    self.read_handler[data_type](rcvData, addr)

        self.socket.close()