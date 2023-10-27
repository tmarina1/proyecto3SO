import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import json
import socket
import platform
from datetime import datetime
import particionar_archivo_img

class FileEncryptor:
    def __init__(self, filename, key, output_filename, second_key, carpeta_fragmentos, num_particiones):
        self.filename = filename
        self.key = key
        self.output_filename = output_filename
        self.second_key = second_key
        self.carpeta_fragmentos = carpeta_fragmentos
        self.num_particiones = num_particiones

    def encrypt(self):
        archivos_disponibles = os.listdir(self.carpeta_fragmentos)
        contador = 0
        for i in archivos_disponibles:
            contador += 1
            cipher = AES.new(self.key, AES.MODE_EAX)
            with open(f'{self.carpeta_fragmentos}/{i}', 'rb') as file:
                plaintext = file.read()
            ciphertext, tag = cipher.encrypt_and_digest(plaintext)
            
            with open(f'archivosSalida/{self.output_filename}_{contador}', 'wb') as file:
                file.write(cipher.nonce)
                file.write(tag)
                file.write(ciphertext)
        self.log_activity()

    def adicionSegundaClave(self):
        archivos_disponibles = os.listdir('archivosSalida')
        for archivo in archivos_disponibles:
            with open(f'archivosSalida/{archivo}', 'ab') as f:
                clave = bytes(self.second_key, 'utf-8')
                f.write(clave)

    def log_activity(self):
        ip = socket.gethostbyname(socket.gethostname())
        computer_name = platform.node()
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        key_hex = self.key.hex()
        
        log_data = {
            'activity': 'ENCRYPTOR',
            'ip': ip,
            'computer_name': computer_name,
            'timestamp': timestamp,
            'key': key_hex,
            'second_key': self.second_key,
        }

        with open('activity_log.json', 'a') as log_file:
            log_file.write(json.dumps(log_data, indent=4) + "\n")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 5:
        print("Uso: py encryption.py <archivo_a_encriptar> <archivo_encriptado> <segunda_llave> <num_particiones>")
        sys.exit(1)

    filename = sys.argv[1]
    output_filename = sys.argv[2]
    key = get_random_bytes(16)
    second_key = sys.argv[3]
    carpeta_fragmentos = 'archivosPartidos'
    num_particiones = sys.argv[4]

    encryptor = FileEncryptor(filename, key, output_filename, second_key, carpeta_fragmentos, num_particiones)
    fragmentar = particionar_archivo_img.particionarImg(filename, int(num_particiones), carpeta_fragmentos)
    encryptor.encrypt()
    encryptor.adicionSegundaClave()