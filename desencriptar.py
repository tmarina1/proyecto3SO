from Crypto.Cipher import AES
import json
import os
import socket
import platform
from datetime import datetime
import particionar_archivo_img

class FileDecryptor:
    def __init__(self, encrypted_filename, key, output_filename, second_key, carpeta_fragmentos, num_particiones):
        self.encrypted_filename = encrypted_filename
        self.key = key
        self.output_filename = output_filename
        self.second_key = second_key
        self.carpeta_fragmentos = carpeta_fragmentos
        self.num_particiones = num_particiones

    def decrypt(self):
        archivos_disponibles = os.listdir(self.carpeta_fragmentos)
        contador = 0
        for archivo in archivos_disponibles:
            contador += 1
            with open(f'{self.carpeta_fragmentos}/{archivo}', 'rb') as file:
                nonce = file.read(16)
                tag = file.read(16)
                ciphertext = file.read()
            cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
            plaintext = cipher.decrypt(ciphertext)

            with open(f'archivosDescomprimidos/{self.output_filename}_{contador}.jpg', 'wb') as file:
                file.write(plaintext)
        self.log_activity()

    def log_activity(self):
        ip = socket.gethostbyname(socket.gethostname())
        computer_name = platform.node()
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        log_data = {
            'activity': 'DESENCRYPTOR',
            'ip': ip,
            'computer_name': computer_name,
            'timestamp': timestamp,
            'second_key': self.second_key,
        }

        with open('activity_log.json', 'a') as log_file:
            log_file.write(json.dumps(log_data, indent=4) + "\n")
    
    def quitarPalabra(self):
        archivos_disponibles = os.listdir('archivosSalida')
        for archivo in archivos_disponibles:
            with open(f'archivosSalida/{archivo}', 'rb+') as f:
                clave = bytes(self.second_key, 'utf-8')
                f.seek(0, 2)
                tamano_palabra = len(clave)

                while True:
                    f.seek(-tamano_palabra, 1)
                    contenido = f.read(tamano_palabra)
                    if contenido == clave:
                        f.seek(-tamano_palabra, 1)
                        f.write(b' ' * tamano_palabra)
                        break
                    elif f.tell() <= tamano_palabra:
                        break

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 6:
        print("Uso: python decryption.py <archivo_encriptado> <archivo_desencriptado> <clave> <segunda_llave>")
        sys.exit(1)

    encrypted_filename = sys.argv[1]
    output_filename = sys.argv[2]
    key = bytes.fromhex(sys.argv[3])  # Convertir la clave en bytes desde una representación hexadecimal
    second_key = sys.argv[4]
    carpeta_fragmentos = 'archivosSalida'
    carpeta_archivos_defragmentar = 'archivosDescomprimidos'
    num_particiones = sys.argv[5]

    decryptor = FileDecryptor(encrypted_filename, key, output_filename, second_key, carpeta_fragmentos, num_particiones)
    decryptor.quitarPalabra()
    decryptor.decrypt()
    desparticionar = particionar_archivo_img.recontruirImg(output_filename, int(num_particiones), carpeta_archivos_defragmentar)