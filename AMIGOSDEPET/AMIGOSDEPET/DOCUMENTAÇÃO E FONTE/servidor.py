#######################################################################
# Primeiro Exercício-Programa da Disciplina de Redes de Computadores  #
# Alunos:Mariana Borges Araujo da Silva, NUSP: 14596342               #
#        Pedro Serrano Buscaglione, NUSP: 14603652                    #
# Turma: 04                                                           #
# Docente: Prof. Dr. João Bernardes                                   #
#######################################################################

#ATUALIZAÇÃO
    # 202416102353 inclusãode leitura de arquivo externo com os dados do servidor do chat
    
#importação do módulo threading que permite a criação e o gerenciamento de threads em Python. 
#isso é essencial para permitir que o servidor trate várias conexões de clientes simultaneamente
#sem bloquear a execução de outras tarefas.
import threading 
#importação do módulo socket fornece a interface para comunicação de rede. 
#Ele é fundamental para a criação de sockets de rede, 
#que são usados para enviar e receber dados entre o servidor e os clientes.
import socket

clients = [] # Lista para armazenar os clientes conectados

def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket TCP

    #try:
        # Associa o socket a um endereço e porta específicos
        #server.bind(('LAPTOP-QJPBL1RC', 7777)) #TROCAR PARA O ENDEREÇO DA MÁQUINA QUE ESTÁ SERVINDO COMO SERVIDOR!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #server.listen() # O servidor começa a escutar (receber) conexões

    #except:
        #return print('\nNão foi possível iniciar o servidor!\n') # Caso haja um erro na inicialização do servidor, imprime uma mensagem de erro

        # Lê o arquivo de configuração para obter o endereço do servidor e a porta
    with open('nomeservidor.txt', 'r') as config_file:
        config = config_file.read().strip().split('|')
        server_address = config[0]
        server_port = int(config[1])  # Converte a porta para um inteiro

    try:
    # Associa o socket a um endereço e porta específicos
        server.bind((server_address, server_port))  # Usa o endereço e a porta lidos do arquivo
        server.listen()  # O servidor começa a escutar (receber) conexões

    except Exception as e:
        print(f'\nNão foi possível iniciar o servidor! Erro: {e}\n')  # Imprime uma mensagem de erro com detalhes
    
    while True:
        # Loop infinito para aceitar conexões de clientes
        client, addr = server.accept() # Aceita uma nova conexão
        clients.append(client) # Adiciona o cliente à lista de clientes conectados

        # Cria uma nova thread para tratar as mensagens do cliente
        thread = threading.Thread(target = messagesTreatment, args=[client])
        thread.start() # Inicia a thread

def messagesTreatment(client):
    while True:
        try:
            msg = client.recv(2048) # Recebe mensagens do cliente
            broadcast(msg, client) # Chama a função para enviar a mensagem para todos os outros clientes
        except:
               deleteClient(client) # Se houver um erro (ex: cliente desconectado), remove o cliente da lista
               break

def broadcast(msg, client):
    # Envia a mensagem recebida para todos os clientes conectados, exceto o que enviou
    for clientItem in clients:
        if  clientItem != client:
            try:
                clientItem.send(msg) # Envia a mensagem
            except:
                deleteClient(clientItem) # Se houver um erro ao enviar, remove o cliente da lista


def deleteClient(client): # Remove um cliente da lista de clientes
    clients.remove(client)


main() # Inicia a função principal que configura e executa o servidor
