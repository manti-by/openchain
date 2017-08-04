from socket import *

from app.utils import get_address, string_to_bytes


if __name__ == "__main__":
    tracker_address = ('127.0.0.1', 8112)
    client_address = get_address()

    udp_socket = socket(AF_INET, SOCK_DGRAM)
    udp_socket.bind(client_address)

    request = string_to_bytes('X-Client-STUN-Address:%s' % client_address[0])
    udp_socket.sendto(request, tracker_address)
    data = udp_socket.recvfrom(1024)
    print(data)

    udp_socket.close()