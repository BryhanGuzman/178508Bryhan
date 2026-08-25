from pynput.keyboard import Key, Listener
from datetime import datetime

# Variable global que almacena la cantidad de eventos registrados
contador_eventos = 0

# Guarda el momento en que ocurrió el evento anterior
ultimo_evento = None


def generar_evento():
    global contador_eventos
    contador_eventos += 1
    return f"evento_{contador_eventos:03d}"

def obtener_tecla(key):
    try:
        return key.char
    except AttributeError:
        return str(key)

def guardar_evento(tipo_evento, tecla):

    global ultimo_evento
    ahora = datetime.now()
    fecha_hora = ahora.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    evento = generar_evento()
    if ultimo_evento is None:
        tiempo_transcurrido = 0.000
    else:
        tiempo_transcurrido = (ahora - ultimo_evento).total_seconds()

    ultimo_evento = ahora

    with open("Eventos.txt", "a", encoding="utf-8") as archivo:
        archivo.write(
            f"{fecha_hora} | "
            f"{tipo_evento:<7} | "
            f"{tecla:<12} | "
            f"{evento} | "
            f"{tiempo_transcurrido:.3f} s\n"
        )

def on_press(key):
    tecla = obtener_tecla(key)
    print(f"Tecla presionada: {tecla}")
    guardar_evento(
        "PRESS",
        tecla
    )

def on_release(key):
    tecla = obtener_tecla(key)
    print(f"Tecla liberada: {tecla}")
    guardar_evento(
        "RELEASE",
        tecla
    )

    if key == Key.esc:
        print("\nPrograma finalizado.")
        return False

print("========================================")
print(" REGISTRO DE EVENTOS DEL TECLADO")
print("========================================")
print("Presiona ESC para finalizar.\n")


with Listener(
    on_press=on_press,
    on_release=on_release
) as listener:

    listener.join()