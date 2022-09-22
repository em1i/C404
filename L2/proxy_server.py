#!/usr/bin/env python3
import socket
import time
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#create a tcp socket
def create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET is for ipv4, SOCK_STREAM is for tcp
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def main():
    proxy_host = 'www.google.com'   #moved to inside echo_handeler
    proxy_port = 80                 #moved to inside echo_handeler
    #higher_buffer_size = 4096      #added, moved inside echo_handeler

    #s is for server and client
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            
            # #create a new socket, proxy_socket for google
            # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_socket:


            #     #recieve data, wait a bit, then send it back
            #     full_data = conn.recv(BUFFER_SIZE)
            #     time.sleep(0.5)

            #     #send the requst to google
            #     google_ip = get_remote_ip(proxy_host)
            #     proxy_socket.connect((google_ip , proxy_port))
            #     print (f'Socket Connected to {proxy_host} on ip {google_ip}')

            #     #send the data and shutdown
            #     send_data(proxy_socket, full_data.decode("utf-8")) #full_data is in bytes, convert it
            #     proxy_socket.shutdown(socket.SHUT_WR)

            #     #continue accepting data until no more left
                
            #     response_data = b"" #byte string type

            #     while True:
            #         data = proxy_socket.recv(higher_buffer_size)
            #         if not data:
            #             break
            #         response_data += data
                
            #     conn.sendall(response_data) #send all data to the client


            #make the processes
            p = Process(target = echo_handler, args=(conn, addr))
            p.start()
            conn.close()


def echo_handler(conn, addr):

    proxy_host = 'www.google.com'
    proxy_port = 80
    higher_buffer_size = 4096   #added

    #create a new socket, proxy_socket for google
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_socket:


        #recieve data, wait a bit, then send it back
        full_data = conn.recv(BUFFER_SIZE)
        time.sleep(0.5)

        #send the requst to google
        google_ip = get_remote_ip(proxy_host)
        proxy_socket.connect((google_ip , proxy_port))
        print (f'Socket Connected to {proxy_host} on ip {google_ip}')

        #send the data and shutdown
        send_data(proxy_socket, full_data.decode("utf-8")) #full_data is in bytes, convert it
        proxy_socket.shutdown(socket.SHUT_WR)

        #continue accepting data until no more left
        
        response_data = b"" #byte string type

        while True:
            data = proxy_socket.recv(higher_buffer_size)
            if not data:
                break
            response_data += data
        
        conn.sendall(response_data) #send all data to the client
        conn.close()

if __name__ == "__main__":
    main()
