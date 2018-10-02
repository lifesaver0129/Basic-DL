# -*- coding=utf8 -*-
import socket
import struct

def WOL(macaddress):
    if len(macaddress) == 12:
        pass
    elif len(macaddress) == 12 + 5:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, '')
    else:
        raise ValueError('Incorrect MAC address format')
    data = ''.join(['FFFFFFFFFFFF', macaddress * 16])
    send_data = b''
    for i in range(0, len(data), 2):
        byte_dat = struct.pack('B', int(data[i: i + 2], 16))
        send_data = send_data + byte_dat
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, ('255.255.255.255', 7))
    sock.close()

if __name__ == '__main__':
    #input your mac adress
    #9C5C8E87C056
    WOL('001FD04D0CB9')
