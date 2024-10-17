#######################################################################
# Primeiro Exercício-Programa da Disciplina de Redes de Computadores  #
# Alunos:Mariana Borges Araujo da Silva, NUSP: 14596342               #
#        Pedro Serrano Buscaglione, NUSP: 14603652                    #
# Turma: 04                                                           #
# Docente: Prof. Dr. João Bernardes                                   #
#######################################################################

#O exercício-programa desenvolvido tem como objetivo criar um aplicativo, chamado Amigos de Pet, voltado para amantes de animais de estimação, 
#Que permite que os usuários interajam através de um chat integrado. Além da funcionalidade de comunicação, 
#O aplicativo conta com uma loja virtual, onde os usuários podem explorar e simular a compra de produtos para seus pets 
#Em uma interface intuitiva.
#A linguagem utilizada para desenvolver esse aplicativo foi Python

import tkinter as tk # Importa a biblioteca Tkinter para criar a interface gráfica
from PIL import Image, ImageTk # Importa classes para manipulação de imagens da biblioteca PIL
import threading # Importa o threading para permitir a execução de múltiplas threads
import socket # Importa o módulo socket para comunicação em rede
import time # Importa o módulo time para manipulação de tempo
import re # Importa o re para operações com strings 

#ALTERAÇÕES REALIZADAS: 
#VERSÃO 18
    # 202410160046 inclusão de preço no sprodutos da loja 
    # 202410160046 mudança na mensagem de servidor referente ao nome inválido de usuário
    # 202410160047 mudança na mensagem de servidor quando finaliza a compra 
    # 202410160115 adição de comentários ao longo dos primeiros trechos de código
    # 202410160122 Mudança de Meu App para Amigos de Pet 
#VERSÃO 19
    # 202410162036 continuação da inserçao de comentários no código 
#VERSÃO 20
    # 202416102310 inclusãode leitura de arquivo externo com os dados do servidor do chat

class App: #principal classe do aplicativo
    def __init__(self, root): # Método construtor que inicializa o aplicativo
        self.root = root # Armazena a referência da janela principal
        self.root.title("Amigos de Pet") #título da janela e nome da aplicação

        self.root.state('zoomed') #faz com que o app abra em tela cheia

        # Lista de itens no carrinho
        self.cart = []

        # Criar frames para diferentes seções do app
        self.main_frame = tk.Frame(root) #tela principal
        self.chat_frame = tk.Frame(root) #tela de chat
        self.store_frame = tk.Frame(root) #tela de loja 
        self.cart_frame = tk.Frame(root) #tela do carrinho de compras 

        # Criar telas chamando métodos para cada seção 
        self.create_main_screen() #tela principal
        self.create_chat_screen() #tela de chat
        self.create_store_screen() #tela de loja
        self.create_cart_screen() #tela de carrinho de compras 

        # Mensagem de boas-vindas que é escrita quando o aplicativo é iniciado pela primeira vez
        self.welcome_message = [
            "Olá,", "seja", "bem-vindo(a)", "ao", "AMIGOS", "DE", "PET!", 
            "Aqui,", "você", "pode", "se", "conectar", "com", "outros", 
            "amantes", "de", "pets", "e", "fazer", "compras", "para", 
            "seu", "fiel", "companheiro.", "Esperamos", "que", "sua", 
            "experiência", "seja", "CÃOtástica", "e", "GATOvante!"
        ]
        #PADY REFERE-SE A QUANTIDADE DE PIXELS QUE SERÃO (MARGEM VERTICAL) QUE SERÁ APLICADO ACIMA E ABAIXO DO WIDGET (JANELA DE TEXTO)
        self.current_word_index = 0
        self.welcome_label = tk.Label(self.main_frame, text="", font=("Arial", 14), wraplength=350, justify="center")
        self.welcome_label.pack(pady=20)
        self.display_welcome_message()

    def display_welcome_message(self):
        if self.current_word_index < len(self.welcome_message):
           self.welcome_label.config(text=self.welcome_label.cget("text") + " " + self.welcome_message[self.current_word_index])
           self.current_word_index += 1
           self.root.after(250, self.display_welcome_message)  # A cada 250 ms, mostra a próxima palavra

        # Mostrar a tela principal ao iniciar
        self.show_frame(self.main_frame)

        # Configurações do chat
        self.client = None
        self.username = None

    def update_status(self, message):
        self.status_label.config(text=message)

    def create_main_screen(self): #Cria um rótulo com o título do aplicativo "AMIGOS DE PET" e define a fonte e o tamanho
        label = tk.Label(self.main_frame, text="AMIGOS DE PET", font=("Arial", 24))
        label.pack(pady=20) # Adiciona o rótulo à tela principal com espaçamento vertical de 20 pixels
        # Cria um rótulo adicional com uma descrição do aplicativo
        label = tk.Label(self.main_frame, text="O app do seu melhor amigo!", font=("Arial", 24))
        label.pack(pady=20)

         # Cria um botão para acessar a tela de chat
        chat_button = tk.Button(self.main_frame, text="CHAT", command=lambda: self.show_frame(self.chat_frame))
        chat_button.pack(side=tk.LEFT, padx=20) # Adiciona o botão à esquerda com espaçamento horizontal de 20 pixels

        store_button = tk.Button(self.main_frame, text="LOJA", command=lambda: self.show_frame(self.store_frame))
        store_button.pack(side=tk.RIGHT, padx=20)

    def create_chat_screen(self): # Cria um rótulo para a tela de chat com um título
        chat_label = tk.Label(self.chat_frame, text="Tela de CHAT", font=("Arial", 24))
        chat_label.pack(pady=20) # Adiciona o rótulo com espaçamento vertical de 20 pixels

         # Rótulo e campo de entrada para o nome de usuário
        tk.Label(self.chat_frame, text="Digite seu nome de usuário:").pack(pady=5)
        self.username_entry = tk.Entry(self.chat_frame, width=30) # Cria um campo de entrada para o nome de usuário
        self.username_entry.pack(pady=5)

        self.chat_display = tk.Text(self.chat_frame, height=15, width=50, state='disabled')
        self.chat_display.pack(pady=10)

        self.chat_input = tk.Entry(self.chat_frame, width=50)
        self.chat_input.pack(pady=10)

        send_button = tk.Button(self.chat_frame, text="Enviar", command=self.send_message)
        send_button.pack(pady=5)

        main_button = tk.Button(self.chat_frame, text="Tela Principal", command=lambda: self.show_frame(self.main_frame))
        main_button.pack(side=tk.LEFT, padx=20)

        store_button = tk.Button(self.chat_frame, text="Loja", command=lambda: self.show_frame(self.store_frame))
        store_button.pack(side=tk.RIGHT, padx=20)

        connect_button = tk.Button(self.chat_frame, text="Conectar", command=self.connect_to_server)
        connect_button.pack(pady=10)

        # Barra de status no chat
        self.status_label = tk.Label(self.chat_frame, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def is_valid_username(self, username):
        #verificações do nome de usuário 
        if len(username) > 10: # Verifica se o comprimento do nome de usuário excede 10 caracteres
            return False #se for, retorna falso
        if not re.match("^[A-Za-z0-9]*$", username): # Verifica se o nome de usuário contém apenas letras e números
            return False #retorna falso se o nome do usuário tiver caracteres especiais
        return True #retorna true se o nome for válido

    def connect_to_server(self):
        self.username = self.username_entry.get() #obtém o nome de usuário inserido na entrada
        if not self.username or not self.is_valid_username(self.username): #verifica se o nome de usuário é vazio ou inválido
            self.chat_display.config(state='normal') #habilita a exibição do chat para permitir inserção de texto
            #mensagem de erro caso o nome de usuário descumpra as restriçõs 
            self.chat_display.insert(tk.END, "Nome de usuário inválido! Seu nome não pode ter mais de 10 caracteres ou ter caracteres especiais\n")
            self.chat_display.config(state='disabled') # deesabilita a edição na exibição do chat
            return #encerra a função se o nome de usuário for inválido

        #Cria um objeto de socket para comunicação em rede usando o protocolo IPv4 (AF_INET) e TCP (SOCK_STREAM)
        #Essa linha é responsável por estabelecer a conexão do cliente com o servidor, permitindo que as mensagens sejam enviadas e recebidas
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        
        # Tenta conectar ao servidor usando o endereço IP e a porta especificados
        #try:
            #self.client.connect(('LAPTOP-QJPBL1RC', 7777)) #MUDAR AQUI COM O NOME DA MÁQUINA QUE ESTÁ SERVINDO COMO SERVIDOR!!!!!!!!!
            #self.chat_display.config(state='normal') # Habilita a exibição do chat para inserir texto
            #self.chat_display.insert(tk.END, f'\nVocê está conectado como {self.username}!\n') # Informa ao usuário que a conexão foi feita
            #self.chat_display.config(state='disabled') #Desabilita a edição na exibição do chat
            #self.update_status("Conectado!") # Atualiza a barra de status para indicar que está conectado MENSAGEM DO SERVIDOR
            #threading.Thread(target=self.receive_messages, daemon=True).start()  # Inicia uma thread para receber mensagens do servidor
            #threading.Thread(target=self.keep_alive, daemon=True).start() # Inicia uma thread para enviar mensagens de keep-alive ao servidor
        #except:
            # Se a conexão falhar, informa o usuário
            #self.chat_display.config(state='normal') # Habilita a exibição do chat
            #self.chat_display.insert(tk.END, '\nNão foi possível se conectar ao servidor!\n') #mensagem de erro
            #self.chat_display.config(state='disabled') # Desabilita a edição na exibição do chat
        
        try:
    # Lê o nome do servidor e a porta a partir do arquivo TXT (É NESSE ARQUIVO QUE DEVE SER COLOCADO O NOME DA MÁQUINA QU ESTÁ SERVINDO COMO SERVIDOR)
            with open('nomeservidor.txt', 'r') as f:
                server_info = f.read().strip()  # Lê o conteúdo do arquivo e remove espaços em branco
                server_name, port = server_info.split('|')  # Divide o conteúdo pelo delimitador '|' 
                port = int(port)  

                # Tenta se conectar ao servidor usando as informações lidas
                self.client.connect((server_name, port))  

                 # Habilita a exibição do chat para que o usuário possa ver mensagens
                self.chat_display.config(state='normal')  
                 # Informa ao usuário que a conexão foi bem-sucedida
                self.chat_display.insert(tk.END, f'\nVocê está conectado como {self.username}!\n')  
                 # Desabilita a edição na exibição do chat para evitar que o usuário altere as mensagens
                self.chat_display.config(state='disabled')  
    
             # Atualiza a barra de status para indicar que a conexão foi estabelecida com sucesso
                self.update_status("Conectado!")  
    
                 # Inicia uma thread para receber mensagens do servidor
                threading.Thread(target=self.receive_messages, daemon=True).start()  
                 # Inicia uma thread para enviar mensagens de keep-alive ao servidor, mantendo a conexão ativa
                threading.Thread(target=self.keep_alive, daemon=True).start()  
        except Exception as e:
            # Se a conexão falhar, informa o usuário com uma mensagem de erro
            self.chat_display.config(state='normal')  
            self.chat_display.insert(tk.END, f'\nNão foi possível se conectar ao servidor: {e}\n') 
            self.chat_display.config(state='disabled')  

    def keep_alive(self):
        #Esse método é importante para garantir que a conexão com o servidor permaneça ativa, evitando desconexões inesperadas
        while True:  #Loop infinito para enviar mensagens de keep-alive
            time.sleep(30) #tempo de 30 segundos entre as mensagens 
            try:
                if self.client: #verifica se o cliente está conectado 
                    self.client.send('KEEP_ALIVE'.encode('utf-8')) # Envia uma mensagem 'KEEP_ALIVE' para o servidor
                    print("Keep Alive sent") #no prompt, imprime que a mensagem foi enviada 
            except:
                #caso ocorra algum erro ao enviar a mensagem 
                self.chat_display.config(state='normal') # Habilita a exibição do chat
                self.chat_display.insert(tk.END, '\nFalha no envio de Keep Alive!\n') # Informa o usuário sobre a falha (MENSAGEM DE SERVIDOR) 
                self.chat_display.config(state='disabled') 
                break 

    #método que garante a funcionalidade do chat, pois permite que o aplicativo receba e exiba mensagens do servidor em tempo real
    def receive_messages(self): 
        while True:
            try:
                msg = self.client.recv(2048).decode('utf-8') # Recebe até 2048 bytes de dados do servidor e decodifica para UTF-8
                if msg == 'KEEP_ALIVE': #ignora mensagens de keep alive para que elas não apareçam na tela de chat a cada 30 segundos
                    continue
                self.chat_display.config(state='normal')  # Habilita a exibição do chat para mostrar a nova mensagem
                self.chat_display.insert(tk.END, msg + '\n') # Adiciona a mensagem recebida à exibição do chat
                self.chat_display.config(state='disabled') # Desabilita a edição na exibição do chat
            except: # Se ocorrer um erro ao receber a mensagem
                self.chat_display.config(state='normal')
                self.chat_display.insert(tk.END, '\nDesconectado do servidor!\n') #mensagem do servidor 
                self.chat_display.config(state='disabled')
                self.update_status("Desconectado")
                self.client.close()  # Fecha o socket do cliente
                break #encerra o loop

    def send_message(self): #método que permite a interação do usuário no chat, permitindo que mensagens sejam enviadas e exibidas.
        msg = self.chat_input.get() # Obtém a mensagem digitada pelo usuário na entrada de texto
        # Verifica se a mensagem não está vazia, se o cliente está conectado e se o usuário tem um nome
        if msg and self.client and self.username:
            try:
                self.chat_display.config(state='normal') # Habilita a exibição do chat para inserir texto
                self.chat_display.insert(tk.END, f'Você: {msg}\n') # Exibe a mensagem enviada pelo usuário
                self.chat_display.config(state='disabled') #Desabilita a edição na exibição do chat
                self.chat_display.see(tk.END) #Rola para baixo para mostrar a última mensagem

                self.client.send(f'<{self.username}> {msg}'.encode('utf-8')) # Envia a mensagem formatada com o nome de usuário para o servidor
                self.chat_input.delete(0, tk.END) # Limpa a entrada de texto após o envio
                self.update_status("Mensagem Enviada") # Atualiza a barra de status para indicar que a mensagem foi enviada
            except:
                self.chat_display.config(state='normal')
                self.chat_display.insert(tk.END, '\nErro ao enviar a mensagem!\n')  # Informa o usuário sobre o erro
                self.chat_display.config(state='disabled') # Desabilita a edição na exibição do chat

    #método que gerencia o carrinho de compras do usuário, permitindo a adição de itens e recebimento de feedback visual sobre suas ações. 
    def add_to_cart(self, item):
        self.cart.append(item) #Adiciona o item à lista de itens no carrinho
        self.update_cart_display() #Atualiza a exibição do carrinho para refletir a nova adição
        item_count = len(self.cart)  #Conta o total de itens no carrinho
        self.store_message_display.config(state='normal') #Habilita a exibição da mensagem da loja
        self.store_message_display.delete(1.0, tk.END)  #Limpa qualquer mensagem anterior
        # Informa ao usuário que o item foi adicionado e mostra o total de itens no carrinho
        self.store_message_display.insert(tk.END, f'Você adicionou "{item}" ao carrinho. Total de itens: {item_count}.\n')
        self.store_message_display.config(state='disabled') #Desabilita a edição na exibição da mensagem da loja

    # método que permite que o usuário remova itens e receba atualizações sobre o status do carrinho.
    def remove_from_cart(self, item):
        if item in self.cart: # Verifica se o item está no carrinho
            self.cart.remove(item) # Remove o item da lista de itens no carrinho
            self.update_cart_display() # Atualiza a exibição do carrinho para refletir a remoção
            self.update_cart_status("Item removido") #Atualiza a mensagem de status para informar sobre a remoção


    def update_cart_status(self, message):  # atualiza o rotulo de status do carrinho com a mensagem fornecida
        #configura o texto do rótulo de status para informar o usuário sobre o estado atual do carrinho
        self.status_cart_label.config(text=message) 

    def create_cart_screen(self): # Cria a interface da tela do carrinho de compras
        cart_label = tk.Label(self.cart_frame, text="Carrinho de Compras", font=("Arial", 24))
        cart_label.pack(pady=20) # Adiciona um rótulo para o título do carrinho com um espaçamento vertical
        # Cria uma área de texto para exibir os itens no carrinho, inicialmente desabilitada para edição
        self.cart_display = tk.Text(self.cart_frame, height=15, width=50, state='disabled')
        self.cart_display.pack(pady=10) # Adiciona a área de texto com espaçamento

        #campo de entrada para que o usuário digite o item a ser removido do carrinho
        #O ITEM SÓ É REMOVIDO DO CARRINHO SE O NOME DELE FOR DIGITADO EXATAMENTE COMO NA TELA DA LOJINHA DE COMPRAS                                                    
        self.remove_entry = tk.Entry(self.cart_frame, width=30)
        self.remove_entry.pack(pady=5)   
        # Botão que chama a função para remover o item do carrinho ao ser clicado                      
        self.remove_button = tk.Button(self.cart_frame, text="Remover do Carrinho", command=self.remove_item) 
        self.remove_button.pack(pady=5)

        # Botão para finalizar compra
        self.checkout_button = tk.Button(self.cart_frame, text="Finalizar Compra", command=self.finalize_purchase)
        self.checkout_button.pack(pady=5) #adiciona o botão à tela do carrinho com um espaçamento vertical de 5 pixels

        main_button = tk.Button(self.cart_frame, text="Tela Principal", command=lambda: self.show_frame(self.main_frame))
        main_button.pack(side=tk.LEFT, padx=20)

        #botao para acessar a loja
        store_button = tk.Button(self.cart_frame, text="Loja", command=lambda: self.show_frame(self.store_frame))
        store_button.pack(side=tk.RIGHT, padx=20) 

        # Barra de status no carrinho
        self.status_cart_label = tk.Label(self.cart_frame, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        # Cria um rótulo para mostrar o status do carrinho, com borda e efeito de afundamento (SUNKEN)
        # Adiciona a barra de status na parte inferior da tela, a barra de status é atualizada
        self.status_cart_label.pack(side=tk.BOTTOM, fill=tk.X)  

    def remove_item(self):
        # Obtém o nome do item a ser removido a partir da entrada do usuário
        item = self.remove_entry.get()
        # Chama o método que remove o item do carrinho
        self.remove_from_cart(item)
        # Limpa a entrada de texto após a remoção para permitir uma nova entrada
        self.remove_entry.delete(0, tk.END)

    def update_cart_display(self):
        # Habilita a edição no campo de exibição do carrinho para permitir atualizações
        self.cart_display.config(state='normal')
        self.cart_display.delete(1.0, tk.END) # Limpa o conteúdo atual do campo de exibição
        if not self.cart: # Verifica se o carrinho está vazio
            # Informa ao usuário que o carrinho está vazio e sugere comprar algo
            self.cart_display.insert(tk.END, "Seu carrinho está vazio!Que tal comprar algo para o seu pet?\n")
        else:
            self.cart_display.insert(tk.END, "Itens no carrinho:\n") # Informa que há itens no carrinho
            for item in self.cart: # Itera sobre cada item no carrinho e o adiciona à exibição
                self.cart_display.insert(tk.END, f'- {item}\n') # Insere o nome do item na exibição com separação por hífen
         # Desabilita a edição no campo de exibição após a atualização para evitar alterações acidentais        
        self.cart_display.config(state='disabled') 

    def finalize_purchase(self):
        if not self.cart: # Verifica se o carrinho de compras está vazio
            # Se o carrinho estiver vazio, atualiza a barra de status com uma mensagem informativa
            self.update_cart_status("Seu carrinho está vazio!")
        else:
            # Se o carrinho não estiver vazio, junta os itens em uma única string com quebras de linha
            items = "\n".join(self.cart)
            #atualiza a barra de status com uma mensagem de confirmação da compra, incluindo os itens comprados
            self.update_cart_status(f"Sua CÃOpra foi finalizada! Seu pet agora tem:\n{items}")
            self.cart.clear()  # Limpa o carrinho após finalizar a compra
            self.update_cart_display()  # Atualiza a exibição do carrinho

    def create_store_screen(self):
        # Cria a tela da loja com o título "PETLOJA"
        store_label = tk.Label(self.store_frame, text="PETLOJA", font=("Arial", 24))
        store_label.pack(pady=20)

        # Exibir imagem da Cama para Gato
        img1_path = "imagens\CAMADEGATO.jpeg"  # Caminho da imagem da cama para gato na pasta 
        img1 = Image.open(img1_path)
        img1 = img1.resize((100, 100), Image.LANCZOS)  # Redimensiona a imagem
        img1_tk = ImageTk.PhotoImage(img1)

        img1_label = tk.Label(self.store_frame, image=img1_tk)
        img1_label.image = img1_tk  # Mantém uma referência à imagem
        img1_label.pack(pady=10)

        desc1 = tk.Label(self.store_frame, text="Produto Artesanal - Cama para Gato | R$ 850,00")
        desc1.pack(pady=5)
        
        #BOTÃO PARA ADICIONAR A CAMA DO GATO NO CARRINHO
        add_to_cart_button1 = tk.Button(self.store_frame, text="Adicionar ao Carrinho", command=lambda: self.add_to_cart("Cama para Gato"))
        add_to_cart_button1.pack(pady=5)

        # Exibir imagem do Mordedor para Cachorro
        img2_path = "imagens\mordedor.jpg"  # Caminho da imagem do mordedor para cachorro ALTERANDO AQUIIIIIIII!!!!!!!!!!!!!!!
        img2 = Image.open(img2_path)
        img2 = img2.resize((100, 100), Image.LANCZOS)  # Redimensiona a imagem
        img2_tk = ImageTk.PhotoImage(img2)

        img2_label = tk.Label(self.store_frame, image=img2_tk)
        img2_label.image = img2_tk  # Mantém uma referência à imagem
        img2_label.pack(pady=10)

        desc2 = tk.Label(self.store_frame, text="Mordedor para Cachorro | R$ 75,00")
        desc2.pack(pady=5)

        #BOTÃO PARA ADICIONAR O MORDEDOR PARA CACHORRO NO CARRINHO
        add_to_cart_button2 = tk.Button(self.store_frame, text="Adicionar ao Carrinho", command=lambda: self.add_to_cart("Mordedor para Cachorro"))
        add_to_cart_button2.pack(pady=5)

        self.store_message_display = tk.Text(self.store_frame, height=5, width=50, state='disabled')
        self.store_message_display.pack(pady=10)

        cart_button = tk.Button(self.store_frame, text="Ver Carrinho", command=lambda: [self.update_cart_display(), self.show_frame(self.cart_frame)])
        cart_button.pack(pady=20)

        main_button = tk.Button(self.store_frame, text="Tela Principal", command=lambda: self.show_frame(self.main_frame))
        main_button.pack(side=tk.LEFT, padx=20)

        chat_button = tk.Button(self.store_frame, text="CHAT", command=lambda: self.show_frame(self.chat_frame))
        chat_button.pack(side=tk.RIGHT, padx=20)

    def show_frame(self, frame):
        # Esconde todos os widgets atualmente visíveis na janela principal, contribuindo para a limpeza da interface
        for widget in self.root.winfo_children(): 
            widget.pack_forget()
        frame.pack(fill="both", expand=True) 

if __name__ == "__main__": 
    root = tk.Tk()  #Cria a janela principal da aplicação usando Tkinter
    app = App(root) # Inicializa a aplicação com a instância da classe App
    root.geometry("400x600") # Define o tamanho inicial da janela (largura x altura)
    root.mainloop() # Inicia o LOOP PRINCIPAL da interface gráfica, aguardando interações do usuário
