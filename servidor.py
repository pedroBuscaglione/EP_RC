import threading
import socket

clients = []

def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind(('0.0.0.0', 7777))  # Escuta em todas as interfaces de rede
        server.listen()
        print('Servidor iniciado com sucesso!')

    except:
        return print('\nNão foi possível iniciar o servidor!\n')
    
    while True:
        client, addr = server.accept()
        print(f"Conexão estabelecida com {addr}")
        clients.append(client)

        thread = threading.Thread(target=messagesTreatment, args=[client])
        thread.start()

def messagesTreatment(client):
    while True:
        try:
            msg = client.recv(2048)
            if not msg:
                break
            broadcast(msg, client)
        except Exception as e:
            print(f"Erro: {e}")
            break
    deleteClient(client)

def broadcast(msg, sender_client):
    for client in clients:
        if client != sender_client:
            try:
                client.send(msg)
            except:
                deleteClient(client)

def deleteClient(client):
    if client in clients:
        clients.remove(client)
        client.close()
        print(f"Cliente desconectado e removido: {client}")

if __name__ == "__main__":
    main()
