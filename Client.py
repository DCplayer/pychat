# Import socket module
import socket
import json
import copy



def menu():
    return "Comandos:\n" \
           "list            List of connected users\n" \
           "log             Returns history of past chats\n" \
           "pvote           Propose a statement for voting\n" \
           "vote            Vote for an existing statement\n" \
           "accept          Accept a new user to the chat\n" \
           "deny            Deny acess to a new user\n"


def handshake():
    jhandshake = {"code": 0}
    info = {}
    username = input("username>>")
    password = input("password>>")
    info["username"] = username
    info["password"] = password
    jhandshake["info"] = info

    return jhandshake, username


def list():
    jlist = {"code" : 3}
    return jlist


def log():
    jlog = {"code": 5}
    return jlog


def present_vote():
    jvote = {"code": 2}
    info = {}
    propuesta = input("Propuesta de Votación>>: ")
    num_opciones = int(input("Cuantas opciones tendra la propuesta? : "))
    opciones = {}
    for i in range(num_opciones):
        opcion = input("Ingrese la opcion No." + str(i+1) + ": ")
        opciones[str(i + 1)] = opcion
    info["propuesta"] = propuesta
    info["decisiones"] = opciones
    jvote["info"] = info
    return jvote


def vote():
    jvote = {"code": 6}
    id_votacion = int(input("Cual es la propuesta por la que desea votar? : "))
    resultados = int(input("Ingrese la opcion que desea: "))
    jvote["id_votacion"] = id_votacion
    jvote["respuesta"] = resultados
    return jvote


def accept_deny(booleano):
    jentry = {"code": 7}
    if booleano:
        jentry["respuesta"] = 1
    else:
        jentry["respuesta"] = 0
    return jentry


def switcher(argument):
    switcher = {
         "": menu,
         "list": list,
         "log": log,
         "pvote": present_vote,
         "vote": vote,
         "accept": accept_deny,
         "deny": accept_deny
     }

    return switcher[argument]


def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'

    # Define the port on which you want to connect
    port = 5050

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server on local computer
    s.connect((host, port))

    message, localusername = handshake()
    #crypt = c.AESCipher('choc0lates3cret0')
    # message you send to server
    while True:

        # message sent to server
        msg = json.dumps(message)
        msg = "ACK" + msg + "SYN"
        #encrypt_msg = crypt.encrypt(msg)
        s.send(msg.encode('UTF-8'))

        # messaga received from server
        data = s.recv(1024)

        # print the received message
        # here it would be a reverse of sent message
        print('Received from the server :', str(data.decode('UTF-8')))

        # ask the client whether he wants to continue
        ans = input('\n> ')
        answer = ""
        if ans.startswith("/"):
            command = ans[1:]
            if command == "quit":
                break
            else:
                if command == "accept" or command == "deny":
                    if command == "accept":
                        answer = switcher(command)(1)
                    else:
                        answer = switcher(command)(0)

                answer = switcher(command)()
                print(answer)
        else:
            answer = {"code": 1,
                      "info": {"username": localusername,
                               "message": ans}}

        message = answer
    # close the connection
    s.close()


if __name__ == '__main__':
    Main()
