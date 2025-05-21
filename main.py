import csv
import os
import re

# IMPORTANTE encabezar el archivo fuente.csv con la siguiente estructura:
# nombre;apellido;nro_doc;mail 

# Configuración
ROL = 'rol'
NOMBRE_INSTITUCION = 'institucion'
CURSO = 'Curso de Python'

# Ruta del archivo de entrada y salida
ENTRADA = os.path.abspath('fuente/fuente.csv')
SALIDA = 'usuarios_moodle.csv'

# Estructura requerida por Moodle
ENCABEZADO = ["lastname", "firstname", "email", "username", "password", "sysrole1"]

EMAIL_REGEX = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')

def limpiar(valor):
    if not valor or valor.strip().upper() == 'NULL':
        return ''
    return valor.strip().title()

def es_correo_valido(correo):
    return bool(EMAIL_REGEX.match(correo))

def es_doc_valido(doc):
    return doc.isdigit() and 7 <= len(doc) <= 11

def procesar_archivo(entrada, salida, con_institucion=False):
    total = 0
    validos = 0
    invalidos = 0
    list_errores = []

    with open(entrada, newline='') as archivo_entrada, \
         open(salida, mode='w', newline='', encoding='utf-8') as archivo_salida:

        lector = csv.DictReader(archivo_entrada, delimiter=';')

        escritor = csv.writer(archivo_salida)

        escritor.writerow(ENCABEZADO)

        for fila in lector:
            total += 1

            apellido = limpiar(fila.get('apellido', ''))
            nombre = limpiar(fila.get('nombre', ''))
            correo = fila.get('mail', '').strip().lower()
            doc = fila.get('nro_doc', '').strip()

            if not es_correo_valido(correo):
                print(f"[INVALIDO] Correo inválido: {correo} (fila {total})")
                invalidos += 1
                list_errores.append(fila)
                continue

            if not es_doc_valido(doc):
                print(f"[INVALIDO] Documento inválido: {doc} (fila {total})")
                invalidos += 1
                list_errores.append(fila)
                continue

            if con_institucion:
                nombre_completo = f"{apellido}, {nombre}"
                escritor.writerow([NOMBRE_INSTITUCION, nombre_completo, correo, doc, doc, ROL])
            else:
                escritor.writerow([apellido, nombre, correo, doc, doc, ROL])

            validos += 1

    print(f"\nProceso completado. Total: {total}, Válidos: {validos}, Inválidos: {invalidos}")
    print(f"Archivo generado correctamente en: {salida}")

    if invalidos > 0:
        with open('errores.csv', mode='w', newline='', encoding='utf-8') as archivo_errores:
            escritor_errores = csv.DictWriter(archivo_errores, fieldnames=lector.fieldnames)
            escritor_errores.writeheader()
            for error in list_errores:
                escritor_errores.writerow(error)

if __name__ == '__main__':
    if not os.path.exists(ENTRADA):
        print(f"No se encontró el archivo: {ENTRADA}")
    else:
        procesar_archivo(ENTRADA, SALIDA, con_institucion=False)
