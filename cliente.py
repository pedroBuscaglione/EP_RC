import threading
import socket
def main():
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM )

    
    try:
        client.connect(('DESKTOP-FL3NE14', 7777)) #localhost
    except:
        return print('\nNão foi possível se conectar ao servidor!\n')
    
    username = input('Usuário> ')
    print('\nVocê está conectado no grupo Amigos de Pet!')

    thread1 = threading.Thread(target=receiveMessages, args=[client])
    thread2 = threading.Thread(target=sendMessages, args=[client, username])

    thread1.start()
    thread2.start()    

def receiveMessages(client):
    while True: 
        try: 
            msg = client.recv(2048).decode('utf-8')
            print(msg+'\n')
        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> para continuar...')
            client.close()
            break


def sendMessages(client, username):
    while True:
        try:
            msg = input('\n')
            client.send(f'<{username}> {msg}'.encode('utf-8'))
        except:
            return


main()