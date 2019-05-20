# import socket programming library
import socket
import json

#Propuestas = Contenido de jsons traducido a strings, separado por \n
#Logs = Texto de mensajes separados por \n

# import thread module
from _thread import *
import threading

print_lock = threading.Lock()

def switcher():
    switch = {
        0: 'handshake',
        1: 'mensaje',
        2: 'propuesta de voto',
        3: 'listar usuarios',
        5: 'historial del chat',
        6: 'accept user',
        7: 'deny user'
    }


def handshake(connected, user):
    jhandshake = {"code": 200}
    if user in connected:
        jhandshake["id"] = str(connected.index(user))
        jhandshake["result"] = 0
    else:
        connected.append(user)
        jhandshake["id"] = str(connected.index(user))
        jhandshake["result"] = 0
    return jhandshake


def list(connected):
    return {"code": 203,
            "connected_users": connected}


def log(logs):
    return {"code": 205, "data": logs}


def p_vote(propuestas, nombre, respuestas):
    update(propuestas)
    jvote = {"code": 202,
             "info": {"id": len(propuestas) - 1,
                      "propuesta": nombre
                      }
             }
    answers = {}
    for x in respuestas:
        answers[x] = 0

    jvote["info"]["decisiones"] = answers
    propuestas.append(jvote)
    d = json.dumps(jvote)
    writeP(d)
    return jvote


def vote(propuestas, id, decision):

    for i in propuestas:
        if i["id"] == id:
            i["info"]["decisiones"][decision] = i["info"]["decisiones"][decision] + 1
            #Falta escribir la actualizacion de votaciones en el documento
            return i
    return "No votacion fue encontrada con ese ID "


def accept_deny(username, access):
    jad = {"code": 207, "username": username}

    if access:
        jad["respuesta"] = 1
    else:
        jad["respuesta"] = 0
    return jad


def update():
    propuestas = []
    f = open("propuestas.txt", "r")
    for x in f:
        propuestas.append(json.loads(x))
    return propuestas


def writeP(propuesta):
    f = open("propuestas.txt", "w")
    f.write(propuesta)
    return


def updatel():
    logs = ""
    f = open("logs.txt", "r")
    for x in f:
        logs = logs + x + "\n"
    return logs


# thread fuction
def threaded(c):
    while True:

        # data received from client
        data = c.recv(1024)
        if not data:
            print('Bye')

            # lock released on exit
            print_lock.release()
            break

        datos = data.decode('UTF-8')
        print(type(datos))
        print(datos)

        if datos.startswith('ACK') and datos.endswith('SYN'):
            jacinto = json.loads(datos[3:len(datos) - 3])


        else:
            print('El mensaje no lleva al estructura correcta. Usted no esta autorizado para enviar mensajes '
                  'en este chat')

        #send back reversed string to client
        c.send(data)

        # connection closed
    c.close()


def Main():
    host = ""

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 5050
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to post", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    #Listado de personas conectadas
    connected = []

    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()


if __name__ == '__main__':
    Main()
