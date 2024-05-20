import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from tkinter import *
import mysql.connector
from mysql.connector import errorcode

# Configuração inicial do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Banco de Dados
cnx = mysql.connector.connect(user="garotosdeprograma", password="Faculdade@157", host="faculdade-mysql.mysql.database.azure.com", port=3306, database="agenda", ssl_ca="{DigiCertGlobalRootG2.crt}", ssl_disabled=False)

config = {
  'host':'faculdade-mysql.mysql.database.azure.com',
  'user':'garotosdeprograma',
  'password':'Faculdade@157',
  'database':'agenda'
}

try:
   conn = mysql.connector.connect(**config)
   print("Connection established")
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with the user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cursor = conn.cursor()

# Configuração do banco de dados
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')
conn.commit()

# Funções para manipulação do banco de dados
def add_user(name, email, username, password):
    try:
        cursor.execute('INSERT INTO users (name, email, username, password) VALUES (?, ?, ?, ?)', 
                (name, email, username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def verify_user(username, password):
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    return cursor.fetchone()

# Funções da interface
def register():
    name = entry_name.get()
    email = entry_email.get()
    username = entry_username_reg.get()
    password = entry_password_reg.get()
    if add_user(name, email, username, password):
        messagebox.showinfo("Sucesso","Usuário registrado com sucesso!")
        register_frame.pack_forget()
        login_frame.pack(padx=100, pady=100)
    else:
        messagebox.showerror("Erro", "Nome de usuário ou e-mail já existe.")

def login():
    username = entry_username.get()
    password = entry_password.get()
    if verify_user(username, password):
        entry_username.delete(0, END)     
        entry_password.delete(0, END)
        messagebox.showinfo("Sucesso", "Login bem-sucedido!")
    else:
        messagebox.showerror("Erro", "Credenciais inválidas.")

def show_login_frame():
    register_frame.pack_forget()
    login_frame.pack(padx=100, pady=100)

def show_register_frame():
    login_frame.pack_forget()
    register_frame.pack(padx=100, pady=100)

# Janela principal
root = ctk.CTk()
root.title("Sistema de Login")
root.geometry("500x600")
# Frame de Login
login_frame = ctk.CTkFrame(root)
login_frame.pack()
label = ctk.CTkLabel(master=login_frame, text='Login', font = ('Roboto', 50, 'bold'), text_color= ('white')  ).pack(pady=20)
ctk.CTkLabel(login_frame, text="Usuário", font = ('Roboto', 20, 'bold')).pack()
entry_username = ctk.CTkEntry(login_frame,width=250,  font= ('Roboto', 17))
entry_username.pack()

ctk.CTkLabel(login_frame, text="Senha", font = ('Roboto', 20, 'bold')).pack()
entry_password = ctk.CTkEntry(login_frame, show="*",width=250,  font= ('Roboto', 17))
entry_password.pack()
checkbox = ctk.CTkCheckBox(master=login_frame, text="Lembrar-se de mim").pack(pady=10)

ctk.CTkButton(login_frame, text="Login", command=login, width=250).pack(padx=70,pady=10 )
ctk.CTkButton(login_frame, text="Não tenho conta/Cadastrar", command=show_register_frame, fg_color="transparent",hover="none").pack()

# Frame de Registro
register_frame = ctk.CTkFrame(root,)

label = ctk.CTkLabel(master=register_frame, text='Cadastro', font = ('Roboto', 50, 'bold'), text_color= ('white'),width=200, ).pack()
ctk.CTkLabel(register_frame, text="Nome").pack()
entry_name = ctk.CTkEntry(register_frame, width=250,  font= ('Roboto', 17))
entry_name.pack(padx=20)

ctk.CTkLabel(register_frame, text="Email").pack()
entry_email = ctk.CTkEntry(register_frame ,width=250,  font= ('Roboto', 17))
entry_email.pack(padx=20)

ctk.CTkLabel(register_frame, text="Usuário").pack()
entry_username_reg = ctk.CTkEntry(register_frame, width=250,  font= ('Roboto', 17))
entry_username_reg.pack(padx=20)

ctk.CTkLabel(register_frame, text="Senha").pack()
entry_password_reg = ctk.CTkEntry(register_frame, show="*", width=250,  font= ('Roboto', 17))
entry_password_reg.pack(padx=20)

ctk.CTkButton(register_frame, text="Cadastrar", command=register, hover_color="darkblue",fg_color="green",width=250).pack(pady=10)
ctk.CTkButton(register_frame, text="Voltar",command=show_login_frame, hover_color="#010101", fg_color="gray", width=250).pack(pady=5)


show_login_frame()

root.mainloop()