import tkinter as tk
from PIL import Image, ImageTk
import threading
import socket
import time
import re

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Meu App")

        # Lista de itens no carrinho
        self.cart = []

        # Criar frames
        self.main_frame = tk.Frame(root)
        self.chat_frame = tk.Frame(root)
        self.store_frame = tk.Frame(root)
        self.cart_frame = tk.Frame(root)

        # Criar telas
        self.create_main_screen()
        self.create_chat_screen()
        self.create_store_screen()
        self.create_cart_screen()

        # Mensagem de boas-vindas que é escrita quando o aplicativo é iniciado pela primeira vez
        self.welcome_message = [
            "Olá,", "seja", "bem-vindo(a)", "ao", "AMIGOS", "DE", "PET!", 
            "Aqui,", "você", "pode", "se", "conectar", "com", "outros", 
            "amantes", "de", "pets", "e", "fazer", "compras", "para", 
            "seu", "fiel", "companheiro.", "Esperamos", "que", "sua", 
            "experiência", "seja", "CÃOtástica", "e", "GATOvante!"
        ]
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

    def create_main_screen(self):
        label = tk.Label(self.main_frame, text="AMIGOS DE PET", font=("Arial", 24))
        label.pack(pady=20)
        label = tk.Label(self.main_frame, text="O app do seu melhor amigo!", font=("Arial", 24))
        label.pack(pady=20)

        chat_button = tk.Button(self.main_frame, text="CHAT", command=lambda: self.show_frame(self.chat_frame))
        chat_button.pack(side=tk.LEFT, padx=20)

        store_button = tk.Button(self.main_frame, text="LOJA", command=lambda: self.show_frame(self.store_frame))
        store_button.pack(side=tk.RIGHT, padx=20)

    def create_chat_screen(self):
        chat_label = tk.Label(self.chat_frame, text="Tela de CHAT", font=("Arial", 24))
        chat_label.pack(pady=20)

        tk.Label(self.chat_frame, text="Digite seu nome de usuário:").pack(pady=5)
        self.username_entry = tk.Entry(self.chat_frame, width=30)
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
        if len(username) > 10:
            return False
        if not re.match("^[A-Za-z0-9]*$", username):
            return False
        return True

    def connect_to_server(self):
        self.username = self.username_entry.get()
        if not self.username or not self.is_valid_username(self.username):
            self.chat_display.config(state='normal')
            self.chat_display.insert(tk.END, "Nome de usuário inválido!\n")
            self.chat_display.config(state='disabled')
            return

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client.connect(('172.115.10.106', 7777))
            self.chat_display.config(state='normal')
            self.chat_display.insert(tk.END, f'\nVocê está conectado como {self.username}!\n')
            self.chat_display.config(state='disabled')
            self.update_status("Conectado!")
            threading.Thread(target=self.receive_messages, daemon=True).start()
            threading.Thread(target=self.keep_alive, daemon=True).start()
        except:
            self.chat_display.config(state='normal')
            self.chat_display.insert(tk.END, '\nNão foi possível se conectar ao servidor!\n')
            self.chat_display.config(state='disabled')

    def keep_alive(self):
        while True:
            time.sleep(30)
            try:
                if self.client:
                    self.client.send('KEEP_ALIVE'.encode('utf-8'))
                    print("Keep Alive sent")
            except:
                self.chat_display.config(state='normal')
                self.chat_display.insert(tk.END, '\nFalha no envio de Keep Alive!\n')
                self.chat_display.config(state='disabled')
                break

    def receive_messages(self):
        while True:
            try:
                msg = self.client.recv(2048).decode('utf-8')
                if msg == 'KEEP_ALIVE':
                    continue
                self.chat_display.config(state='normal')
                self.chat_display.insert(tk.END, msg + '\n')
                self.chat_display.config(state='disabled')
            except:
                self.chat_display.config(state='normal')
                self.chat_display.insert(tk.END, '\nDesconectado do servidor!\n')
                self.chat_display.config(state='disabled')
                self.update_status("Desconectado")
                self.client.close()
                break

    def send_message(self):
        msg = self.chat_input.get()
        if msg and self.client and self.username:
            try:
                self.chat_display.config(state='normal')
                self.chat_display.insert(tk.END, f'Você: {msg}\n')
                self.chat_display.config(state='disabled')
                self.chat_display.see(tk.END)

                self.client.send(f'<{self.username}> {msg}'.encode('utf-8'))
                self.chat_input.delete(0, tk.END)
                self.update_status("Mensagem Enviada")
            except:
                self.chat_display.config(state='normal')
                self.chat_display.insert(tk.END, '\nErro ao enviar a mensagem!\n')
                self.chat_display.config(state='disabled')

    def add_to_cart(self, item):
        self.cart.append(item)
        self.update_cart_display()
        item_count = len(self.cart)
        self.store_message_display.config(state='normal')
        self.store_message_display.delete(1.0, tk.END)
        self.store_message_display.insert(tk.END, f'Você adicionou "{item}" ao carrinho. Total de itens: {item_count}.\n')
        self.store_message_display.config(state='disabled')

    def remove_from_cart(self, item):
        if item in self.cart:
            self.cart.remove(item)
            self.update_cart_display()
            self.update_cart_status("Item removido")

    def update_cart_status(self, message):
        self.status_cart_label.config(text=message)

    def create_cart_screen(self):
        cart_label = tk.Label(self.cart_frame, text="Carrinho de Compras", font=("Arial", 24))
        cart_label.pack(pady=20)

        self.cart_display = tk.Text(self.cart_frame, height=15, width=50, state='disabled')
        self.cart_display.pack(pady=10)

        self.remove_entry = tk.Entry(self.cart_frame, width=30)
        self.remove_entry.pack(pady=5)
        self.remove_button = tk.Button(self.cart_frame, text="Remover do Carrinho", command=self.remove_item)
        self.remove_button.pack(pady=5)

        # Botão para finalizar compra
        self.checkout_button = tk.Button(self.cart_frame, text="Finalizar Compra", command=self.finalize_purchase)
        self.checkout_button.pack(pady=5)

        main_button = tk.Button(self.cart_frame, text="Tela Principal", command=lambda: self.show_frame(self.main_frame))
        main_button.pack(side=tk.LEFT, padx=20)

        store_button = tk.Button(self.cart_frame, text="Loja", command=lambda: self.show_frame(self.store_frame))
        store_button.pack(side=tk.RIGHT, padx=20)

        # Barra de status no carrinho
        self.status_cart_label = tk.Label(self.cart_frame, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_cart_label.pack(side=tk.BOTTOM, fill=tk.X)

    def remove_item(self):
        item = self.remove_entry.get()
        self.remove_from_cart(item)
        self.remove_entry.delete(0, tk.END)

    def update_cart_display(self):
        self.cart_display.config(state='normal')
        self.cart_display.delete(1.0, tk.END)
        if not self.cart:
            self.cart_display.insert(tk.END, "Seu carrinho está vazio!Que tal comprar algo para o seu pet?\n")
        else:
            self.cart_display.insert(tk.END, "Itens no carrinho:\n")
            for item in self.cart:
                self.cart_display.insert(tk.END, f'- {item}\n')
        self.cart_display.config(state='disabled')

    def finalize_purchase(self):
        if not self.cart:
            self.update_cart_status("Seu carrinho está vazio!")
        else:
            items = "\n".join(self.cart)
            self.update_cart_status(f"Compra finalizada! Itens:\n{items}")
            self.cart.clear()  # Limpa o carrinho após finalizar a compra
            self.update_cart_display()  # Atualiza a exibição do carrinho

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
        
        #BOTÃO PARA ADICIONAR A CAMA DO GATO NO CARRINHO
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
        for widget in self.root.winfo_children():
            widget.pack_forget()
        frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.geometry("400x600")
    root.mainloop()
