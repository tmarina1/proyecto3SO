from PIL import Image
import os

def particionarImg(archivoImg, numParticiones, carpeta_fragmentos):
    try:
        imagen = Image.open(archivoImg)
    except FileNotFoundError:
        print(f"El archivo {archivoImg} no se encontró.")
        return

    ancho, alto = imagen.size
    tamanoParticion = ancho // numParticiones
    particiones = []

    for i in range(numParticiones):
        izquierda = i * tamanoParticion
        derecha = (i + 1) * tamanoParticion

        particion = imagen.crop((izquierda, 0, derecha, alto))
        particiones.append(particion)

        nombreParticion = f"{archivoImg}_parte_{i + 1}.jpg"
        particion.save(f'{carpeta_fragmentos}/{nombreParticion}')

def recontruirImg(archivoImg, numParticiones, carpeta_fragmentos):
    try:
        particiones = []
        for i in range(numParticiones):
            nombreParticion = f"{archivoImg}_{i + 1}.jpg"
            particion = Image.open(f'{carpeta_fragmentos}/{nombreParticion}')
            particiones.append(particion)

        ancho_total = sum([particion.width for particion in particiones])
        alto = particiones[0].height
        imgRecontruida = Image.new("RGB", (ancho_total, alto))

        x_offset = 0
        for particion in particiones:
            imgRecontruida.paste(particion, (x_offset, 0))
            x_offset += particion.width
        imgRecontruida.save(f'recreado-{archivoImg}.jpg')

        for i in range(numParticiones):
            nombreParticion = f"{archivoImg}_{i + 1}.jpg"
            os.remove(f'{carpeta_fragmentos}/{nombreParticion}')
    except FileNotFoundError:
        print(f"Alguna(s) partición(es) no se encontraron. Asegúrate de que todas las particiones estén presentes.")