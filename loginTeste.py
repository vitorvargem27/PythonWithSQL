import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pymysql.cursors

# Configuração da conexão com o banco de dados
conection = pymysql.connect(
    host='localhost',
    user='root',
    passwd='Mavi1234#',
    db='pizzaria',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# Configuração de estilo customizado
def configurar_estilos():
    style = ttk.Style()
    style.theme_use("clam")

    # Estilo de botões
    style.configure(
        "TButton",
        font=("Segoe UI", 14),
        padding=10,
        relief="flat",
        background="#FF5722",  # Laranja vibrante
        foreground="white",
        focuscolor="#FF7043"
    )
    style.map(
        "TButton",
        background=[("active", "#FF7043")],
        foreground=[("active", "white")]
    )

    # Estilo de entradas
    style.configure(
        "TEntry",
        font=("Segoe UI", 12),
        padding=8,
        relief="flat",
        fieldbackground="#E1F5FE",  # Azul claro de fundo
        bordercolor="#FF5722"
    )

    # Estilo de labels
    style.configure(
        "TLabel",
        font=("Segoe UI", 14),
        padding=5,
        foreground="#333333"
    )

    # Estilo de Toplevel (janela secundária)
    style.configure(
        "Toplevel",
        background="#F5F5F5"
    )

# Função de autenticação
def autenticar():
    username = entrada_usuario.get()
    senha = entrada_senha.get()

    if not username or not senha:
        messagebox.showwarning("Atenção", "Preencha todos os campos!")
        return

    try:
        with conection.cursor() as cursor:
            cursor.execute("SELECT * FROM clientes WHERE username_cliente = %s AND password_cliente = %s",
                           (username, senha))
            user = cursor.fetchone()
            if user:
                messagebox.showinfo("Sucesso", f"Bem-vindo(a), {user['nome_cliente']}!")
                abrir_menu(user)
            else:
                messagebox.showerror("Erro", "Usuário ou senha incorretos.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")

# Função para abrir o menu principal
def abrir_menu(user):
    janela_login.destroy()

    # Janela do menu principal
    janela_menu = tk.Tk()
    janela_menu.title("Menu Principal")
    janela_menu.geometry("800x650")
    janela_menu.configure(bg="#FFEBEE")  # Fundo suave e elegante (rosa claro)

    # Título do menu
    ttk.Label(janela_menu, text=f"Bem-vindo(a), {user['nome_cliente']}!", font=("Segoe UI", 18, "bold"), anchor="center", background="#FFEBEE").pack(pady=20)

    # Botões com estilos
    ttk.Button(janela_menu, text="Adicionar Usuário", command=create, style="TButton").pack(pady=15, fill="x", padx=30)
    ttk.Button(janela_menu, text="Ver Dados", command=readData, style="TButton").pack(pady=15, fill="x", padx=30)
    ttk.Button(janela_menu, text="Editar Dados", command=updateData, style="TButton").pack(pady=15, fill="x", padx=30)
    ttk.Button(janela_menu, text="Excluir Usuário", command=delete, style="TButton").pack(pady=15, fill="x", padx=30)
    ttk.Button(janela_menu, text="Sair", command=janela_menu.destroy, style="TButton").pack(pady=20, fill="x", padx=30)

    janela_menu.mainloop()

# Função para adicionar um usuário
def create():
    janela_create = tk.Toplevel()
    janela_create.title("Adicionar Usuário")
    janela_create.geometry("400x350")
    janela_create.configure(bg="#FFEBEE")

    campos = ["Nome", "CPF", "Usuário", "Senha"]
    entradas = {}

    for i, campo in enumerate(campos):
        ttk.Label(janela_create, text=f"{campo}:", font=("Segoe UI", 12), background="#FFEBEE").grid(row=i, column=0, padx=10, pady=10, sticky=tk.W)
        entrada = ttk.Entry(janela_create, width=30, style="TEntry", show="*" if campo == "Senha" else "")
        entrada.grid(row=i, column=1, padx=10, pady=10)
        entradas[campo] = entrada

    def salvar():
        nome = entradas["Nome"].get()
        cpf = entradas["CPF"].get()
        username = entradas["Usuário"].get()
        senha = entradas["Senha"].get()

        if not nome or not cpf or not username or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        try:
            with conection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO clientes (nome_cliente, cpf_cliente, username_cliente, password_cliente) "
                    "VALUES (%s, %s, %s, %s)", (nome, cpf, username, senha))
                conection.commit()
                messagebox.showinfo("Sucesso", "Usuário criado com sucesso!")
                janela_create.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar no banco de dados: {e}")

    ttk.Button(janela_create, text="Salvar", command=salvar, style="TButton").grid(row=4, column=0, columnspan=2, pady=20)

# Função para visualizar dados
def readData():
    janela_read = tk.Toplevel()
    janela_read.title("Ver Dados")
    janela_read.geometry("400x300")
    janela_read.configure(bg="#FFEBEE")

    ttk.Label(janela_read, text="Digite o CPF do Usuário:", font=("Segoe UI", 12), background="#FFEBEE").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
    entrada_cpf = ttk.Entry(janela_read, width=30, style="TEntry")
    entrada_cpf.grid(row=0, column=1, padx=10, pady=10)

    def buscar():
        cpf = entrada_cpf.get()

        if not cpf:
            messagebox.showwarning("Atenção", "Digite o CPF!")
            return

        try:
            with conection.cursor() as cursor:
                cursor.execute("SELECT * FROM clientes WHERE cpf_cliente = %s", (cpf,))
                dados = cursor.fetchall()

                if not dados:
                    messagebox.showinfo("Aviso", "Nenhum usuário encontrado!")
                    return

                for idx, data in enumerate(dados, start=1):
                    ttk.Label(janela_read, text=f"Usuário {idx}: Nome - {data['nome_cliente']}", font=("Segoe UI", 12), background="#FFEBEE").grid(row=idx, column=0, padx=10, pady=5)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar dados: {e}")

    ttk.Button(janela_read, text="Buscar", command=buscar, style="TButton").grid(row=1, column=0, columnspan=2, pady=10)

# Função para editar dados
def updateData():
    janela_update = tk.Toplevel()
    janela_update.title("Editar Usuário")
    janela_update.geometry("400x350")
    janela_update.configure(bg="#FFEBEE")

    ttk.Label(janela_update, text="CPF do Usuário a ser editado:", font=("Segoe UI", 12), background="#FFEBEE").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
    entrada_cpf = ttk.Entry(janela_update, width=30, style="TEntry")
    entrada_cpf.grid(row=0, column=1, padx=10, pady=10)

    def buscar_usuario():
        cpf = entrada_cpf.get()

        if not cpf:
            messagebox.showwarning("Atenção", "Digite o CPF do usuário!")
            return

        try:
            with conection.cursor() as cursor:
                cursor.execute("SELECT * FROM clientes WHERE cpf_cliente = %s", (cpf,))
                usuario = cursor.fetchone()

                if not usuario:
                    messagebox.showinfo("Aviso", "Usuário não encontrado!")
                    return

                ttk.Label(janela_update, text="Novo Nome:", font=("Segoe UI", 12), background="#FFEBEE").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
                entrada_nome = ttk.Entry(janela_update, width=30, style="TEntry")
                entrada_nome.grid(row=1, column=1, padx=10, pady=10)
                entrada_nome.insert(0, usuario['nome_cliente'])

                ttk.Label(janela_update, text="Novo Username:", font=("Segoe UI", 12), background="#FFEBEE").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
                entrada_username = ttk.Entry(janela_update, width=30, style="TEntry")
                entrada_username.grid(row=2, column=1, padx=10, pady=10)
                entrada_username.insert(0, usuario['username_cliente'])

                def salvar_alteracoes():
                    novo_nome = entrada_nome.get()
                    novo_username = entrada_username.get()

                    if not novo_nome or not novo_username:
                        messagebox.showwarning("Atenção", "Preencha todos os campos!")
                        return

                    try:
                        with conection.cursor() as cursor:
                            cursor.execute(
                                "UPDATE clientes SET nome_cliente = %s, username_cliente = %s WHERE cpf_cliente = %s",
                                (novo_nome, novo_username, cpf)
                            )
                            conection.commit()
                            messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
                            janela_update.destroy()
                    except Exception as e:
                        messagebox.showerror("Erro", f"Erro ao atualizar dados: {e}")

                ttk.Button(janela_update, text="Salvar Alterações", command=salvar_alteracoes, style="TButton").grid(row=3, column=0, columnspan=2, pady=20)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar usuário: {e}")

    ttk.Button(janela_update, text="Buscar", command=buscar_usuario, style="TButton").grid(row=1, column=0, columnspan=2, pady=10)

# Função para excluir um usuário
def delete():
    janela_delete = tk.Toplevel()
    janela_delete.title("Excluir Usuário")
    janela_delete.geometry("400x200")
    janela_delete.configure(bg="#FFEBEE")

    ttk.Label(janela_delete, text="Digite o CPF do Usuário a ser excluído:", font=("Segoe UI", 12), background="#FFEBEE").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
    entrada_cpf = ttk.Entry(janela_delete, width=30, style="TEntry")
    entrada_cpf.grid(row=0, column=1, padx=10, pady=10)

    def excluir_usuario():
        cpf = entrada_cpf.get()

        if not cpf:
            messagebox.showwarning("Atenção", "Digite o CPF!")
            return

        try:
            with conection.cursor() as cursor:
                cursor.execute("DELETE FROM clientes WHERE cpf_cliente = %s", (cpf,))
                conection.commit()
                messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
                janela_delete.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir usuário: {e}")

    ttk.Button(janela_delete, text="Excluir", command=excluir_usuario, style="TButton").grid(row=1, column=0, columnspan=2, pady=10)

# Janela de Login
janela_login = tk.Tk()
janela_login.title("Login")
janela_login.geometry("300x250")
janela_login.configure(bg="#FFEBEE")

configurar_estilos()

ttk.Label(janela_login, text="Usuário:", font=("Segoe UI", 12), background="#FFEBEE").pack(pady=10)
entrada_usuario = ttk.Entry(janela_login, width=30, style="TEntry")
entrada_usuario.pack()

ttk.Label(janela_login, text="Senha:", font=("Segoe UI", 12), background="#FFEBEE").pack(pady=10)
entrada_senha = ttk.Entry(janela_login, width=30, style="TEntry", show="*")
entrada_senha.pack()

ttk.Button(janela_login, text="Entrar", command=autenticar, style="TButton").pack(pady=20)

janela_login.mainloop()
