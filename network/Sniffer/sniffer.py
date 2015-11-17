import socket, sys
from struct import *

#TODO: Hat noch keine Funktion
class sniffer:
    def __init__(self):
        self.s = None
        #create a AF_PACKET type raw socket (thats basically packet level)
        #define ETH_P_ALL    0x0003          /* Every packet (be careful!!!) */
        try:
            self.s = socket.socket( socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(0x0003))
        except socket.error as msg:
            print('Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

    #Convert a string of 6 characters of ethernet address into a dash separated hex string
    def eth_addr(s):
        b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (s[0] , s[1] , s[2], s[3], s[4] , s[5])
        return b

    def get_mac(self, vlan_id):
        while True:
            packet = self.s.recvfrom(65565)
            packet = packet[0]

            eth_length = 14

            eth_header = packet[:eth_length]
            eth = unpack('!6s6sH' , eth_header)
            eth_type = eth[2];

            if eth_type == 0x8100:
                eth_vlan_header = packet[:(eth_length+2)]
                eth_vlan = unpack('!6s6sHH' , eth_vlan_header)
                eth_vlan_id = socket.ntohs(eth_vlan[3])
                if eth_vlan_id == vlan_id:
                    return self.eth_addr(packet[0:6])
