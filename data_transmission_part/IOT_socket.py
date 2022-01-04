import socket

def socket_conn_PC():
    HOST = '0.0.0.0'
    PORT = 7000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)

    print('server start at: %s:%s' % (HOST, PORT))
    print('wait for connection...')

    return s

def socket_conn_Pi():
    HOST = '0.0.0.0'
    PORT = 7000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((HOST, PORT))
    
    return s
