import time

from tqdm import tqdm

from utils import get_random_string

FILE_JUNK = 1024

def upload_file(command_socket, data_socket, directory, filename, filesize):
    print("Send 'STOR' command")
    command_socket.send(("STOR " + filename + "\r\n").encode('utf-8'))
    output = command_socket.recv(FILE_JUNK)
    print("Recieved: " + (output.decode('utf-8')))
    # start sending the file

    progress = tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=FILE_JUNK)
    with open(directory + filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(FILE_JUNK)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in
            # busy networks
            data_socket.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))

    progress.close()
    time.sleep(2)
    data_socket.close()
    print("File transfer finished\r\n")
    output = command_socket.recv(FILE_JUNK)
    print("Recieved: " + (output.decode('utf-8')))


def download_file(command_socket, data_socket, directory, filename):
    print("Send 'RETR' command")
    command_socket.send(("RETR " + filename + "\r\n").encode('utf-8'))
    output = command_socket.recv(FILE_JUNK)
    print("Recieved: " + (output.decode('utf-8')))
    fileSplit = filename.split('.')

    with open(directory + fileSplit[0] + "-" + get_random_string() + "." + fileSplit[1], "wb") as f:
        while True:
            bytes_read = data_socket.recv(FILE_JUNK)
            if not bytes_read:
                break
            f.write(bytes_read)

    time.sleep(2)
    data_socket.close()
    print("File transfer finished\r\n")
    output = command_socket.recv(FILE_JUNK)
    print("Recieved: " + (output.decode('utf-8')))
