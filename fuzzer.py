import argparse
import os
import re
import socket
import threading
import time

from helper import *


def fuzzFileAccess(host, port):
    pdf_file = "TestPdf.pdf"
    rtf_file = "TestRtf.rtf"
    directory = "files/"

    # try concurrent file writing to the same file at the server
    file_up_thread1 = threading.Thread(target=create_connection_and_upload_file, args=(host, port, directory, pdf_file))
    file_up_thread2 = threading.Thread(target=create_connection_and_upload_file, args=(host, port, directory, pdf_file))
    file_up_thread1.start()
    file_up_thread2.start()

    # upload rtf file to download it again later
    create_connection_and_upload_file(host, port, directory, rtf_file)
    # try concurrent file download to the same file at the server
    file_down_thread1 = threading.Thread(target=create_connection_and_download_file,
                                         args=(host, port, directory, rtf_file))
    file_down_thread2 = threading.Thread(target=create_connection_and_download_file,
                                         args=(host, port, directory, rtf_file))
    file_down_thread1.start()
    file_down_thread2.start()


def ddos(host , port, username, password, number_connections):
	socket_list = []

	print("Execute DDOS command with {} simultaneous connections".format(number_connections))
	print("Open connections to server and authenticate with the passed username and password\n")
	for index in range(number_connections):
		try:
			s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			s.settimeout(10)
			connect = s.connect((host,port))
			socket_list.append(s)
			time.sleep(0.1)
			output = s.recv(1024)
			time.sleep(0.1)
			s.send(("USER {}\r\n".format(username)).encode('utf-8'))		
			output = s.recv(1024)
			time.sleep(0.1)
			s.send(("PASS {}\r\n".format(password)).encode('utf-8'))	
			output = s.recv(1024)
			time.sleep(0.1)
		except socket.error as e:
			print("Caught exception socket.error: {} at connection {}".format(e, index))


def commandsWithoutArguments(host, port):	
	commands = ['ABOR','ACCT','ALLO','APPE','AUTH','CWD','CDUP','DELE','FEAT','HELP','HOST','LANG','LIST',
				'MDTM','MKD','MLST','MODE','NLST','NLST -al','NOOP','OPTS','PORT','PROT','PWD','REIN',
				'REST','RETR','RMD','RNFR','RNTO','SIZE','SITE','SITE CHMOD','SITE CHOWN','SITE EXEC','SITE MSG',
				'SITE PSWD','SITE ZONE','SITE WHO','SMNT','STAT','STOR','STOU','STRU','SYST','TYPE','USER','XCUP',
				'XCRC','XCWD','XMKD','XPWD','XRMD']

	print("Executing the following commands without arguments:\n{}".format(commands))

	for command in commands:
		try:
			s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			connect = s.connect((host,port))
			time.sleep(1)
			s.recv(1024)
			time.sleep(0.1)

			s.send(("{}\r\n".format(command)).encode('utf-8'))		
			s.recv(1024)
			time.sleep(0.1)

			s.send(("PWD\r\n").encode('utf-8'))	
			s.recv(1024)
			time.sleep(0.1)

			s.send(("QUIT\r\n").encode('utf-8'))	
			s.recv(1024)
			time.sleep(0.1)
			s.close()
		except:
			print("Server crashed while executing '{}'".format(command))

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',
                        default='localhost',
                        dest='host',
                        help='Destination host. Default is localhost.',
                        type=str
                        )
    parser.add_argument('--port',
                        default='1025',
                        dest='port',
                        help='Destination port. Default is 1025.',
                        type=int
                        )
    parser.add_argument('--username',
                        default='comp4621',
                        dest='username',
                        help='Username to connect to the FTP Server. Default is comp4621.',
                        type=str
                        )
    parser.add_argument('--password',
                        default='network',
                        dest='password',
                        help='Password to connect to the FTP Server. Default is network.',
                        type=str
                        )
    parser.add_argument('--fuzz_user',
                        action='store_true',
                        dest='fuzz_user',
                        help='Fuzz the USER command.'
                        )
    parser.add_argument('--fuzz-file-access',
                        action='store_true',
                        dest='fuzz_file_access',
                        help='Command to fuzz concurrent access to files.'
                        )
    parser.add_argument('--ddos',
		                default=argparse.SUPPRESS,
                        dest='ddos',
                        help='Open many simultaneous connections to the FTP Server.',
                        type=check_positive
    )
    parser.add_argument('--commands-no-args',
                        action='store_true',
                        dest='commandsNoArgs',
                        help='Execute many FTP commands without arguments.'
    )
    args = parser.parse_args()

    if args.fuzz_file_access:
        fuzzFileAccess(args.host, args.port)
    if args.commandsNoArgs:
        commandsWithoutArguments(args.host, args.port)
    if hasattr(args, 'ddos'):
        ddos(args.host, args.port, args.username, args.password, args.ddos)

if __name__ == '__main__':
    main()