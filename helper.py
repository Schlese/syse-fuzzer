import os
import socket
import time

from file_exchange import upload_file, FILE_JUNK, download_file
from utils import calculate_port


def create_authenticated_connection(host, port):
    print("Create socket and connect to server")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect = s.connect((host, port))
    time.sleep(0.5)
    output = s.recv(FILE_JUNK)
    print("Recieved: " + (output.decode('utf-8')))
    time.sleep(0.5)

    print("Send 'USER' command")
    s.send(("USER Schlese\r\n").encode('utf-8'))
    output = s.recv(FILE_JUNK)
    print("Recieved: " + (output.decode('utf-8')))
    time.sleep(0.5)

    print("Send 'PASS' command")
    s.send(("PASS network\r\n").encode('utf-8'))
    output = s.recv(FILE_JUNK)
    print("Recieved: " + (output.decode('utf-8')))
    time.sleep(0.5)

    return s


def create_connection_and_upload_file(host, port, directory, filename):
    filesize = os.path.getsize(directory + "/" + filename)
    command_socket = create_authenticated_connection(host, port)

    print("Send 'TYPE' command")
    command_socket.send(("TYPE I\r\n").encode('utf-8'))
    output = command_socket.recv(FILE_JUNK)
    print("Recieved: " + (output.decode('utf-8')))
    time.sleep(0.5)

    print("Send 'PASV' command")
    command_socket.send(("PASV\r\n").encode('utf-8'))
    output = command_socket.recv(FILE_JUNK)
    print("Recieved: " + (output.decode('utf-8')))
    output = command_socket.recv(FILE_JUNK)
    print("Recieved: " + (output.decode('utf-8')))
    message = output.decode('utf-8');
    data_port = calculate_port(message)
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.connect((host, data_port))

    upload_file(command_socket, data_socket, directory, filename, filesize)

    print("Send 'QUIT' command")
    command_socket.send(("QUIT\r\n").encode('utf-8'))
    output = command_socket.recv(FILE_JUNK)
    print("Recieved: " + (output.decode('utf-8')))
    time.sleep(0.5)

    print("Close connection")
    command_socket.close()
    # close the socket


def create_connection_and_download_file(host, port, directory, filename):
    command_socket = create_authenticated_connection(host, port)

    print("Send 'TYPE' command")
    command_socket.send(("TYPE I\r\n").encode('utf-8'))
    output = command_socket.recv(FILE_JUNK)
    print("Recieved: " + (output.decode('utf-8')))
    time.sleep(0.5)

    print("Send 'PASV' command")
    command_socket.send(("PASV\r\n").encode('utf-8'))
    output = command_socket.recv(FILE_JUNK)
    print("Recieved: " + (output.decode('utf-8')))
    output = command_socket.recv(FILE_JUNK)
    print("Recieved: " + (output.decode('utf-8')))
    message = output.decode('utf-8');
    data_port = calculate_port(message)
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.connect((host, data_port))

    download_file(command_socket, data_socket, directory, filename)

    print("Send 'QUIT' command")
    command_socket.send(("QUIT\r\n").encode('utf-8'))
    output = command_socket.recv(FILE_JUNK)
    print("Recieved: " + (output.decode('utf-8')))
    time.sleep(0.5)

    print("Close connection")
    command_socket.close()
    # close the socket
