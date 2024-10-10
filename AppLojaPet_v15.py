import tkinter as tk
from PIL import Image, ImageTk
import threading
import socket
import time  # Importando a biblioteca time para o sleep
import re  # Importando a biblioteca re para expressões regulares

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Meu App")
        
        # Lista de itens no carrinho
        self.cart = []  # Lista para armazenar os itens do carrinho
        
        # Criar frames
        self.main_frame = tk.Frame(root)
        self.chat_frame = tk.Frame(root)
        self.store_frame = tk.Frame(root)
        self.cart_frame = tk.Frame(root)  # Frame para o carrinho

        # Criar telas
        self.create_main_screen()
        self.create_chat_screen()
        self.create_store_screen()
        self.create_cart_screen()  # Tela do carrinho

        # Mostrar a tela principal ao iniciar
        self.show_frame(self.main_frame)

        # Configurações do chat
        self.client = None
        self.username = None

    def create_main_screen(self):
        label = tk.Label(self.main_frame, text="Bem Vindo!", font=("Arial", 24))
        label.pack(pady=20)

        chat_button = tk.Button(self.main_frame, text="CHAT", command=lambda: self.show_frame(self.chat_frame))
        chat_button.pack(side=tk.LEFT, padx=20)

        store_button = tk.Button(self.main_frame, text="LOJA", command=lambda: self.show_frame(self.store_frame))
        store_button.pack(side=tk.RIGHT, padx=20)

    def create_chat_screen(self):
        chat_label = tk.Label(self.chat_frame, text="Tela de CHAT", font=("Arial", 24))
        chat_label.pack(pady=20)

        # Campo para nome de usuário
        tk.Label(self.chat_frame, text="Digite seu nome de usuário:").pack(pady=5)
        self.username_entry = tk.Entry(self.chat_frame, width=30)
        self.username_entry.pack(pady=5)

        # Área de texto para mostrar mensagens
        self.chat_display = tk.Text(self.chat_frame, height=15, width=50, state='disabled')
        self.chat_display.pack(pady=10)

        # Campo de entrada para digitar mensagens
        self.chat_input = tk.Entry(self.chat_frame, width=50)
        self.chat_input.pack(pady=10)

        # Botão para enviar a mensagem
        send_button = tk.Button(self.chat_frame, text="Enviar", command=self.send_message)
        send_button.pack(pady=5)

        main_button = tk.Button(self.chat_frame, text="Tela Principal", command=lambda: self.show_frame(self.main_frame))
        main_button.pack(side=tk.LEFT, padx=20)

        store_button = tk.Button(self.chat_frame, text="Loja", command=lambda: self.show_frame(self.store_frame))
        store_button.pack(side=tk.RIGHT, padx=20)

        # Botão para conectar ao servidor
        connect_button = tk.Button(self.chat_frame, text="Conectar", command=self.connect_to_server)
        connect_button.pack(pady=10)

    # Função de validação do nome de usuário
    def is_valid_username(self, username):
        # Verifica se o nome de usuário tem no máximo 10 caracteres
        if len(username) > 10:
            return False
        # Verifica se contém caracteres especiais
        if not re.match("^[A-Za-z0-9]*$", username):
            return False
        return True

    def connect_to_server(self):
        self.username = self.username_entry.get()  # Obtém o nome de usuário da entrada
        # Verifica se o nome de usuário é válido
        if not self.username or not self.is_valid_username(self.username):
            self.chat_display.config(state='normal')
            # Mensagem de erro se o nome de usuário for inválido
            self.chat_display.insert(tk.END, "Nome de usuário inválido! Deve ter no máximo 10 caracteres e não pode conter caracteres especiais.\n")
            self.chat_display.config(state='disabled')
            return

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.client.connect(('LAPTOP-QJPBL1RC', 7777))  # Conectando ao servidor local ESSE ENDEREÇO DEVE SER ALTERADO DE ACORDO COM O ENDEREÇO DO SERVIDOR
            self.chat_display.config(state='normal')
            self.chat_display.insert(tk.END, f'\nVocê está conectado no grupo Amigos de Pet como {self.username}!\n')
            self.chat_display.config(state='disabled')
            threading.Thread(target=self.receive_messages, daemon=True).start()  # Inicia a thread para receber mensagens
            threading.Thread(target=self.keep_alive, daemon=True).start()  # Inicia a thread para enviar Keep Alive
        except:
            self.chat_display.config(state='normal')
            self.chat_display.insert(tk.END, '\nNão foi possível se conectar ao servidor!\n')
            self.chat_display.config(state='disabled')

    def keep_alive(self):
        while True:
            time.sleep(30)  # Envia a cada 30 segundos
            try:
                if self.client:
                    # Envia uma mensagem Keep Alive ao servidor
                    self.client.send(f'KEEP_ALIVE'.encode('utf-8'))
                    print("Keep Alive sent")  # Log para ver que está enviando
            except:
                self.chat_display.config(state='normal')
                self.chat_display.insert(tk.END, '\nFalha no envio de Keep Alive!\n')
                self.chat_display.config(state='disabled')
                break

    def receive_messages(self):
        while True: 
            try: 
                msg = self.client.recv(2048).decode('utf-8')
                self.chat_display.config(state='normal')
                self.chat_display.insert(tk.END, msg + '\n')
                self.chat_display.config(state='disabled')
            except:
                self.chat_display.config(state='normal')
                self.chat_display.insert(tk.END, '\nNão foi possível permanecer conectado no servidor!\n')
                self.chat_display.config(state='disabled')
                self.client.close()
                break

    def send_message(self):
        msg = self.chat_input.get()
        if msg and self.client and self.username:
            try:
                # Exibe a mensagem no campo de chat
                self.chat_display.config(state='normal')
                self.chat_display.insert(tk.END, f'Você: {msg}\n')
                self.chat_display.config(state='disabled')
                self.chat_display.see(tk.END)  # Rola o chat para a última mensagem

                # Envia a mensagem ao servidor
                self.client.send(f'<{self.username}> {msg}'.encode('utf-8'))
                self.chat_input.delete(0, tk.END)  # Limpa a entrada
            except:
                self.chat_display.config(state='normal')
                self.chat_display.insert(tk.END, '\nErro ao enviar a mensagem!\n')
                self.chat_display.config(state='disabled')

    # Função para adicionar itens ao carrinho
    def add_to_cart(self, item):
        self.cart.append(item)
        self.show_frame(self.cart_frame)  # Exibe o carrinho atualizado

    def create_cart_screen(self):
        cart_label = tk.Label(self.cart_frame, text="Carrinho de Compras", font=("Arial", 24))
        cart_label.pack(pady=20)

        self.cart_display = tk.Text(self.cart_frame, height=15, width=50, state='disabled')
        self.cart_display.pack(pady=10)

        main_button = tk.Button(self.cart_frame, text="Tela Principal", command=lambda: self.show_frame(self.main_frame))
        main_button.pack(side=tk.LEFT, padx=20)

        store_button = tk.Button(self.cart_frame, text="Loja", command=lambda: self.show_frame(self.store_frame))
        store_button.pack(side=tk.RIGHT, padx=20)

    def update_cart_display(self):
        self.cart_display.config(state='normal')
        self.cart_display.delete(1.0, tk.END)  # Limpa o campo de exibição do carrinho
        if not self.cart:
            self.cart_display.insert(tk.END, "Seu carrinho está vazio!\n")
        else:
            self.cart_display.insert(tk.END, "Itens no carrinho:\n")
            for item in self.cart:
                self.cart_display.insert(tk.END, f'- {item}\n')
        self.cart_display.config(state='disabled')

    def create_store_screen(self):
        store_label = tk.Label(self.store_frame, text="Tela de LOJA", font=("Arial", 24))
        store_label.pack(pady=20)

        # Exibir imagem da Cama para Gato
        img1_path = "imagens\CAMADEGATO.jpeg"  # Caminho da imagem da cama para gato #ALTERANDO AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII!!!!!!!!!!!!!!
        img1 = Image.open(img1_path)
        img1 = img1.resize((100, 100), Image.LANCZOS)  # Redimensiona a imagem
        img1_tk = ImageTk.PhotoImage(img1)

        img1_label = tk.Label(self.store_frame, image=img1_tk)
        img1_label.image = img1_tk  # Mantém uma referência à imagem
        img1_label.pack(pady=10)

        desc1 = tk.Label(self.store_frame, text="Cama para Gato")
        desc1.pack(pady=5)

        add_to_cart_button1 = tk.Button(self.store_frame, text="Adicionar ao Carrinho", command=lambda: self.add_to_cart("Cama para Gato"))
        add_to_cart_button1.pack(pady=5)

        # Exibir imagem do Mordedor para Cachorro
        img2_path = "imagens\mordedor.jpg"  # Caminho da imagem do mordedor para cachorro ALTERANDO AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII!!!!!!!!!!!!!!!
        img2 = Image.open(img2_path)
        img2 = img2.resize((100, 100), Image.LANCZOS)  # Redimensiona a imagem
        img2_tk = ImageTk.PhotoImage(img2)

        img2_label = tk.Label(self.store_frame, image=img2_tk)
        img2_label.image = img2_tk  # Mantém uma referência à imagem
        img2_label.pack(pady=10)

        desc2 = tk.Label(self.store_frame, text="Mordedor para Cachorro")
        desc2.pack(pady=5)

        add_to_cart_button2 = tk.Button(self.store_frame, text="Adicionar ao Carrinho", command=lambda: self.add_to_cart("Mordedor para Cachorro"))
        add_to_cart_button2.pack(pady=5)

        # Botão para ver o carrinho
        cart_button = tk.Button(self.store_frame, text="Ver Carrinho", command=lambda: [self.update_cart_display(), self.show_frame(self.cart_frame)])
        cart_button.pack(pady=20)

        main_button = tk.Button(self.store_frame, text="Tela Principal", command=lambda: self.show_frame(self.main_frame))
        main_button.pack(side=tk.LEFT, padx=20)

        chat_button = tk.Button(self.store_frame, text="CHAT", command=lambda: self.show_frame(self.chat_frame))
        chat_button.pack(side=tk.RIGHT, padx=20)

    def show_frame(self, frame):
        # Limpa a tela atual
        for widget in self.root.winfo_children():
            widget.pack_forget()

        # Mostra o novo frame
        frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.geometry("400x400")  # Define o tamanho da janela
    root.mainloop()
