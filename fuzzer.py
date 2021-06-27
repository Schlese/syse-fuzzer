import argparse
import socket
import time

# https://github.com/samyoyo/SFTPfuzzer/blob/master/SFTPfuzzer.py
# https://blog.modpr0.be/2010/09/20/very-simple-ftp-fuzzer/
# https://stackoverflow.com/questions/50117522/how-to-connect-to-an-ftp-server-with-sockets
# https://stackoverflow.com/questions/30965512/my-simple-client-crash-everytime-it-tries-to-connect-to-my-python-socket-server

def fuzzUsername(host , port):
	try:
		print("Create socket and connect to server")
		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		connect = s.connect((host,port))
		time.sleep(0.5)
		output = s.recv(1024)
		print("Recieved: "+(output.decode('utf-8')))
		time.sleep(0.5)

		print("Send 'USER' command")
		s.send(("USER\r\n").encode('utf-8'))		
		output = s.recv(1024)
		print("Recieved: "+(output.decode('utf-8')))
		time.sleep(0.5)

		print("Send 'PASS' command")
		s.send(("PASS network\r\n").encode('utf-8'))	
		output = s.recv(1024)
		print("Recieved: "+(output.decode('utf-8')))
		time.sleep(0.5)

		print("Send 'PWD' command")
		s.send(("PWD\r\n").encode('utf-8'))	
		output = s.recv(1024)
		print("Recieved: "+(output.decode('utf-8')))
		time.sleep(0.5)

		print("Send 'QUIT' command")
		s.send(("QUIT\r\n").encode('utf-8'))	
		output = s.recv(1024)
		print("Recieved: "+(output.decode('utf-8')))
		time.sleep(0.5)

		print("Close connection")
		s.close()
	except:
		print("Error: Connection refused or server crashed")	


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
	args = parser.parse_args()

	if args.fuzz_user:
		fuzzUsername(args.host, args.port)

if  __name__ =='__main__':
    main()
