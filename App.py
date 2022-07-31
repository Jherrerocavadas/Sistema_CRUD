import tkinter as tk
import tkinter.ttk as ttk
from time import sleep
from PIL import Image, ImageTk
from Data.modulos.aux_Funcs import Aux_func

Aux_Func = Aux_func()

# Modelo de classe que herda direto de tk.Tk()
class UI(tk.Tk):
    def __init__(self):
        super().__init__() # Inicializaçõo da biblioteca Tkinter
        self.Configuration() # Configurações iniciais
        self.estilos() # Aplicação de estilos
        self.menus(self) # Criação das abas de menu
        self.Login_screen() # Geração e redirecionamento para a tela de login


    def Configuration(self):
        cfg = Aux_Func.Carregar_config()

        # Configurações de versão e logo do aplicativo
        self.version = cfg["Version"]
        self.logo_path = cfg["Logo_path"]
        self.logo = Image.open(self.logo_path)
        self.logo1 = ImageTk.PhotoImage(self.logo.resize((500, 500)))#, Image.Resampling.LANCZOS))

        # Configurações da janela Tkinter
        self.title(f"Sistema CRUD - {self.version}")
        self.geometry("250x200")
        self.configure(bg = '#10172f')

        # Configurações de armazenamento de sessão
        self.User_session = [None, None]
        self.User_Perms = None
        self.All_perms = cfg["Perms"]

        #Criação dos elementos de Toplevel
        self.loading_screen = None
        self.main_screen = None
        self.insert_data = None
        self.edit_data = None
        self.exclude_data = None
        self.search_data = None
        self.import_file = None
        self.export_file = None
        self.new_budget = None

        # Configurações de textos das janelas
        self.Insert_data_type_value = cfg["Insert_data_type_value"]
        self.Edit_data_type_value = cfg["Edit_data_type_value"]
        self.Search_data_type_value = cfg["Search_data_type_value"]
        self.Delete_data_type_value = cfg["Delete_data_type_value"]


    #Seleção do Usuário
    def Login_screen(self):

        #Função de verificação do login
        def verify_login():
            status, self.User_session[0], self.User_session[1], self.User_Perms = Aux_Func.Login_verification(User.get(), Senha.get())
            Status_txt.configure(text = status)
            if(status == "Login bem-sucedido!"):
                self.Loading_screen()

        #Frames:
        frame_status = ttk.Frame(self)
        frame_user = ttk.Frame(self)
        frame_senha = ttk.Frame(self)
        frame_entra1 = ttk.Frame(self)

        frame_status.pack()
        frame_user.pack()
        frame_senha.pack()
        frame_entra1.pack()

        #Label de Status
        Status_txt = ttk.Label(frame_status)
        Status_txt.pack()

        #Label e Entry - Usuário
        User_txt = ttk.Label(frame_user, text = "Usuário:" )
        User = ttk.Entry(frame_user)
        User_txt.pack()
        User.pack()

        #Label e Entry - Senha
        Senha_txt = ttk.Label(frame_senha, text = "Senha:" )
        Senha = ttk.Entry(frame_senha)
        Senha_txt.pack()
        Senha.pack()

        #Botão de "submit"
        Entrar = ttk.Button(frame_entra1, text = 'Entrar', command = verify_login)
        self.bind('<Return>',lambda event : verify_login())
        Entrar.pack()


    def Loading_screen(self):
        status_janela, janela = self.withdraw_func(self.loading_screen, '500x500','Loading')
        # Dá pra atribuir self.Toplevel no lugar de janela, aqui acima
        self.loading_screen = janela

        def Loading_bar():
            for i in range(101):
                self.update_idletasks()
                loading_bar['value'] = i
                if(i == 0):
                    janela['background']='#10172f'

                sleep(0.03)
            else:
                self.Main()

        if(status_janela == 'Criar janela'):

            frame_logo = ttk.Frame(janela)
            frame_logo.pack()

            Logo = ttk.Label(janela, image=self.logo1)
            Logo.pack()

            Perms=ttk.Label(janela, text = f'Perms: {self.User_Perms}')
            Perms.place(relx=0.5, rely=0.5, anchor='center')

            loading_bar = ttk.Progressbar(janela, orient='horizontal', mode='determinate', length=500)
            loading_bar.place(relx =0, rely=0.96)

        Loading_bar()


#Editar
    def Main(self):
        status_janela, janela = self.withdraw_func(self.main_screen,'500x500','Main')
        self.loading_screen = janela

        if(status_janela == 'Criar janela'):
            pass

#Editar
    def Exportar_Arquivo(self):
        status_janela, janela = self.withdraw_func(self.export_file,'500x500','Exportar_Arquivo')
        self.export_file = janela
        if(status_janela == 'Criar janela'):
            pass
#Editar
    def Carregar_Arquivo(self):
        status_janela, janela = self.withdraw_func(self.import_file,'500x500','Importar_Arquivo')
        self.import_file = janela
        if(status_janela == 'Criar janela'):
            pass

    def Inserir_Dados(self):
        status_janela, janela = self.withdraw_func(self.insert_data,'500x500','Inserir_Dados')
        self.insert_data = janela
        if(status_janela == 'Criar janela'):

            #Frames
            frame_datatype = ttk.Frame(janela)
            frame_status = ttk.Frame(janela)
            frame_data = ttk.Frame(janela)
            frame_confirma = ttk.Frame(janela)

            frame_datatype.pack()
            frame_status.pack()
            frame_data.pack()
            frame_confirma.pack()

            #Checkbox - Tipo de dados
            Tipo_dado_txt = ttk.Label(frame_datatype, text = 'Selecione o tipo de dado:')
            Tipo_dado_txt.pack()
            Tipo_dado = ttk.Combobox(frame_datatype, values=self.Insert_data_type_value)
            janela.bind('<<ComboboxSelected>>',lambda event : generate_entry())
            Tipo_dado.pack()

            #Se mudar o texto nas configs, o código ainda vai funcionar
            # self.Insert_data_type_value[0] : Novo Usuário
            # self.Insert_data_type_value[1] : Novo Funcionário
            # self.Insert_data_type_value[2] : Nova Taxa
            # self.Insert_data_type_value[3] : Nova Tarefa

            #Status
            Status_txt = ttk.Label(frame_status)#, text = 'STATUS')
            Status_txt.pack()

            def generate_entry():
                for widget in frame_data.winfo_children():
                    widget.destroy()
                Status_txt['text'] = ""

                for widget in frame_confirma.winfo_children():
                    widget.destroy()


                if(Tipo_dado.get() == self.Insert_data_type_value[0]):
                    if(self.User_Perms == 'Admin'):

                        #Label e Entry - Usuário
                        User_txt = ttk.Label(frame_data, text = "Usuário:" )
                        User = ttk.Entry(frame_data)
                        User_txt.pack()
                        User.pack()

                        #Label e Entry - Senha
                        Senha_txt = ttk.Label(frame_data, text = "Senha:" )
                        Senha = ttk.Entry(frame_data)
                        Senha_txt.pack()
                        Senha.pack()

                        #Label e Entry - Permissões
                        Perms_txt = ttk.Label(frame_data, text='Permissões: ')
                        Perms = ttk.Entry(frame_data)
                        Perms_txt.pack()
                        Perms.pack()

                        dados = {
                        "Tipo_dado": Tipo_dado.get(),
                        "User": User,
                        "Senha" : Senha,
                        "Permissões" : Perms
                        }
                    else:
                        Status_txt['text'] = "Esse usuário não pode executar essa ação!"
                        for widget in frame_confirma.winfo_children():
                            widget.destroy()


                elif(Tipo_dado.get() == self.Insert_data_type_value[1]):
                    Area_que_atua_var = tk.StringVar()
                    #Nome e Cargo
                    Nome_txt = ttk.Label(frame_data, text='Nome: ')
                    Nome = ttk.Entry(frame_data)
                    Nome_txt.pack()
                    Nome.pack()

                    Cargo_txt = ttk.Label(frame_data, text='Cargo: ')
                    Cargo = ttk.Entry(frame_data)
                    Cargo_txt.pack()
                    Cargo.pack()

                    #Contatos
                    Telefone_txt = ttk.Label(frame_data, text='Telefone: ')
                    Telefone = ttk.Entry(frame_data)
                    Telefone_txt.pack()
                    Telefone.pack()

                    Telefone2_txt = ttk.Label(frame_data, text='Telefone2: ')
                    Telefone2 = ttk.Entry(frame_data)
                    Telefone2_txt.pack()
                    Telefone2.pack()

                    Email_txt = ttk.Label(frame_data, text='Email: ')
                    Email = ttk.Entry(frame_data)
                    Email_txt.pack()
                    Email.pack()

                    #Endereço
                    Endereco_txt = ttk.Label(frame_data, text='Endereço: ')
                    Endereco = ttk.Entry(frame_data)
                    Endereco_txt.pack()
                    Endereco.pack()

                    #Documentos
                    RG_txt = ttk.Label(frame_data, text='RG: ')
                    RG = ttk.Entry(frame_data)
                    RG_txt.pack()
                    RG.pack()

                    CPF_CNPJ_txt = ttk.Label(frame_data, text='CPF/CNPJ: ')
                    CPF_CNPJ = ttk.Entry(frame_data)
                    CPF_CNPJ_txt.pack()
                    CPF_CNPJ.pack()

                    if(self.User_Perms == 'Admin'):
                        Area_que_atua_txt = ttk.Label(frame_data, text='Escolha a Área de atuação: ')
                        Area_que_atua = ttk.Combobox(frame_data, values=self.All_perms)
                        janela.bind('<<ComboboxSelected>>',lambda event : Area_que_atua_var.set(Area_que_atua.get()))
                        Area_que_atua_txt.pack()
                        Area_que_atua.pack()
                    else:
                        Area_que_atua_var.set(self.User_Perms)

                    dados = {
                    "Tipo_dado": Tipo_dado.get(),
                    "Nome": Nome,
                    "Cargo" : Cargo,
                    "Telefone" : Telefone,
                    "Telefone2" : Telefone2,
                    "Email" : Email,
                    "Endereco" : Endereco,
                    "RG" : RG,
                    "CPF_CNPJ" : CPF_CNPJ,
                    "Cadastrado_por" : self.User_session[1],
                    "Area_que_atua" : Area_que_atua_var

                    }

                elif(Tipo_dado.get() == self.Insert_data_type_value[2]):

                    Taxa_txt = ttk.Label(frame_data, text='Nome da Taxa: ')
                    Taxa = ttk.Entry(frame_data)
                    Taxa_txt.pack()
                    Taxa.pack()

                    Valor_taxa_txt = ttk.Label(frame_data, text='Valor da taxa: ')
                    Valor_taxa = ttk.Entry(frame_data)
                    Valor_taxa_txt.pack()
                    Valor_taxa.pack()

                    dados = {
                    "Tipo_dado": Tipo_dado.get(),
                    "Taxa": Taxa,
                    "Valor_taxa" : Valor_taxa
                    }

                elif(Tipo_dado.get() == self.Insert_data_type_value[3]):

                    Tarefa_txt = ttk.Label(frame_data, text='Tarefa: ')
                    Tarefa = ttk.Entry(frame_data)
                    Tarefa_txt.pack()
                    Tarefa.pack()

                    Data_txt = ttk.Label(frame_data, text='Data: ')
                    Data = ttk.Entry(frame_data)
                    Data_txt.pack()
                    Data.pack()

                    Hora_txt = ttk.Label(frame_data, text='Hora: ')
                    Hora = ttk.Entry(frame_data)
                    Hora_txt.pack()
                    Hora.pack()

                    dados = {
                    "Tipo_dado": Tipo_dado.get(),
                    "Tarefa": Tarefa,
                    "Data" : Data,
                    "Hora" : Hora
                    }

                Confirma = tk.Button(frame_confirma, text="Enviar", command = lambda : Aux_Func.Inserir_Dados(**dados))
                janela.bind('<Return>',lambda event : Aux_Func.Inserir_Dados(**dados))
                Confirma.pack()

# Editar
    def Editar_Dados(self):
        status_janela, janela = self.withdraw_func(self.edit_data,'500x500','Editar_Dados')
        self.edit_data = janela
        if(status_janela == 'Criar janela'):
            pass


    def Excluir_Dados(self):
        status_janela, janela = self.withdraw_func(self.exclude_data,'500x500','Excluir_Dados')
        self.exclude_data = janela
        if(status_janela == 'Criar janela'):
            #Frames
            frame_datatype = ttk.Frame(janela)
            frame_status = ttk.Frame(janela)
            frame_data = ttk.Frame(janela)
            frame_excluir = ttk.Frame(janela)

            frame_datatype.pack()
            frame_status.pack()
            frame_data.pack()
            frame_excluir.pack()


            Tipo_dado_txt = ttk.Label(frame_datatype, text = 'Selecione o tipo de dado:')
            Tipo_dado_txt.pack()
            Tipo_dado = ttk.Combobox(frame_datatype, values=self.Delete_data_type_value)
            Tipo_dado.bind('<<ComboboxSelected>>',lambda event : generate_data_values())
            Tipo_dado.pack()

            dado_selecionado_txt = ttk.Label(frame_datatype, text = 'Selecione o dado:')
            dado_selecionado_txt.pack()
            dado_selecionado = ttk.Combobox(frame_datatype ,state='disabled')
            dado_selecionado.bind('<<ComboboxSelected>>',lambda event : generate_data_info())
            dado_selecionado.pack()

            def generate_data_values():

                for widget in frame_data.winfo_children():
                    widget.destroy()

                for widget in frame_excluir.winfo_children():
                    widget.destroy()

                dados_para_selecionar = Aux_Func.Pesquisar_infos(Tipo_dado.get(), 'deletar dados')
                dado_selecionado.configure(values= dados_para_selecionar, state = 'readonly')

            def generate_data_info():
                for widget in frame_data.winfo_children():
                    widget.destroy()

                dados = Aux_Func.get_dados(Tipo_dado, dado_selecionado, 'deletar dados')
                dado_selecionado.configure(state='readonly')

                for widget in frame_excluir.winfo_children():
                    widget.destroy()

                if(Tipo_dado.get() == self.Delete_data_type_value[0]):

                    User_txt = ttk.Label(frame_data, text = "Usuário:" )
                    User = ttk.Label(frame_data, text = dados['Username'])
                    User_txt.grid(column=0, row=0)
                    User.grid(column=1, row=0)

                    Perms_txt = ttk.Label(frame_data, text='Permissões: ')
                    Perms = ttk.Label(frame_data, text=dados['Permissions'])
                    Perms_txt.grid(column=0, row=1)
                    Perms.grid(column=1, row=1)


                elif(Tipo_dado.get() == self.Delete_data_type_value[1]):

                    #Nome e Cargo
                    Nome_txt = ttk.Label(frame_data, text='Nome: ')
                    Nome = ttk.Label(frame_data, text=dados['Nome'])
                    Nome_txt.grid(column=0, row=0)
                    Nome.grid(column=1, row=0)

                    Cargo_txt = ttk.Label(frame_data, text='Cargo: ')
                    Cargo = ttk.Label(frame_data, text=dados['Cargo'])
                    Cargo_txt.grid(column=0, row=1)
                    Cargo.grid(column=1, row=1)

                    Area_que_atua_txt = ttk.Label(frame_data, text='Area que atua: ')
                    Area_que_atua = ttk.Label(frame_data, text=dados['Area_que_atua'])
                    Area_que_atua_txt.grid(column=0, row=2)
                    Area_que_atua.grid(column=1, row=2)

                elif(Tipo_dado.get() == self.Delete_data_type_value[2]):

                    Taxa_txt = ttk.Label(frame_data, text='Nome da Taxa: ')
                    Taxa = ttk.Label(frame_data, text=dado_selecionado.get())
                    Taxa_txt.grid(column=0, row=0)
                    Taxa.grid(column=1, row=0)

                    #Documentos
                    Valor_taxa_txt = ttk.Label(frame_data, text='Valor da taxa: ')
                    Valor_taxa = ttk.Label(frame_data, text=dados)
                    Valor_taxa_txt.grid(column=0, row=1)
                    Valor_taxa.grid(column=1, row=1)

                elif(Tipo_dado.get() == self.Delete_data_type_value[3]):

                    Tarefa_txt = ttk.Label(frame_data, text='Tarefa: ')
                    Tarefa = ttk.Label(frame_data, text= dados['Tarefa'] )
                    Tarefa_txt.grid(column=0, row=0)
                    Tarefa.grid(column=1, row=0)

                    #Documentos
                    Data_txt = ttk.Label(frame_data, text='Data: ')
                    Data = ttk.Label(frame_data, text=dados['Data'])
                    Data_txt.grid(column=0, row=1)
                    Data.grid(column=1, row=1)

                    Hora_txt = ttk.Label(frame_data, text='Hora: ')
                    Hora = ttk.Label(frame_data, text=dados['Hora'])
                    Hora_txt.grid(column=0, row=2)
                    Hora.grid(column=1, row=2)

                Confirma = ttk.Button(frame_excluir, text="Excluir", command = lambda : Aux_Func.Excluir_Dados(Tipo_dado, dado_selecionado))
                janela.bind('<Return>',lambda event : Aux_Func.Excluir_Dados(Tipo_dado, dado_selecionado))
                Confirma.pack()


    def Pesquisar_Dados(self):
        status_janela, janela = self.withdraw_func(self.search_data,'350x350','Pesquisar_Dados')
        self.search_data = janela
        Search_value = ""
        if(status_janela == 'Criar janela'):

            #Frames
            frame_datatype = ttk.Frame(janela)
            frame_status = ttk.Frame(janela)
            frame_data = ttk.Frame(janela)
            frame_confirma = ttk.Frame(janela)

            frame_datatype.pack()
            frame_status.pack()
            frame_data.pack()
            frame_confirma.pack()

            Tipo_dado_txt = ttk.Label(frame_datatype, text = 'Selecione o tipo de dado:')
            Tipo_dado_txt.pack()
            Tipo_dado = ttk.Combobox(frame_datatype, values=self.Search_data_type_value)
            Tipo_dado.bind('<<ComboboxSelected>>',lambda event : generate_data_values())
            Tipo_dado.pack()

            dado_selecionado_txt = ttk.Label(frame_datatype, text = 'Selecione o dado:')
            dado_selecionado_txt.pack()
            dado_selecionado = ttk.Combobox(frame_datatype ,state='disabled')
            dado_selecionado.bind('<<ComboboxSelected>>',lambda event : generate_data_info())
            dado_selecionado.pack()

            #Se mudar o texto nas configs, o código ainda vai funcionar
            # self.Search_data_type_value[0] : Usuários
            # self.Search_data_type_value[1] : Funcionários
            # self.Search_data_type_value[2] : Taxas
            # self.Search_data_type_value[3] : Tarefas

            def generate_data_values():

                for widget in frame_data.winfo_children():
                    widget.destroy()
                dados_para_selecionar = Aux_Func.Pesquisar_infos(Tipo_dado.get(), 'pesquisar dados')
                dado_selecionado.configure(values= dados_para_selecionar, state = 'readonly')

            def generate_data_info():
                for widget in frame_data.winfo_children():
                    widget.destroy()

                dados = Aux_Func.get_dados(Tipo_dado, dado_selecionado, 'pesquisar dados')
                dado_selecionado.configure(state='readonly')

                if(Tipo_dado.get() == self.Search_data_type_value[0]):

                    User_txt = ttk.Label(frame_data, text = "Usuário:" )
                    User = ttk.Label(frame_data, text = dados['Username'])
                    User_txt.grid(column=0, row=0)
                    User.grid(column=1, row=0)


                    Perms_txt = ttk.Label(frame_data, text='Permissões: ')
                    Perms = ttk.Label(frame_data, text=dados['Permissions'])
                    Perms_txt.grid(column=0, row=1)
                    Perms.grid(column=1, row=1)


                elif(Tipo_dado.get() == self.Search_data_type_value[1]):

                    #Nome e Cargo
                    Nome_txt = ttk.Label(frame_data, text='Nome: ')
                    Nome = ttk.Label(frame_data, text=dados['Nome'])
                    Nome_txt.grid(column=0, row=0)
                    Nome.grid(column=1, row=0)

                    Cargo_txt = ttk.Label(frame_data, text='Cargo: ')
                    Cargo = ttk.Label(frame_data, text=dados['Cargo'])
                    Cargo_txt.grid(column=0, row=1)
                    Cargo.grid(column=1, row=1)

                    #Contatos
                    Telefone_txt = ttk.Label(frame_data, text='Telefone: ')
                    Telefone = ttk.Label(frame_data, text=dados['Telefone'])
                    Telefone_txt.grid(column=0, row=2)
                    Telefone.grid(column=1, row=2)

                    Telefone2_txt = ttk.Label(frame_data, text='Telefone2: ')
                    Telefone2 = ttk.Label(frame_data, text=dados['Telefone2'])
                    Telefone2_txt.grid(column=0, row=3)
                    Telefone2.grid(column=1, row=3)

                    Email_txt = ttk.Label(frame_data, text='Email: ')
                    Email = ttk.Label(frame_data, text=dados['Email'])
                    Email_txt.grid(column=0, row=4)
                    Email.grid(column=1, row=4)

                    #Endereço
                    Endereco_txt = ttk.Label(frame_data, text='Endereço: ')
                    Endereco = ttk.Label(frame_data, text=dados['Endereco'])
                    Endereco_txt.grid(column=0, row=5)
                    Endereco.grid(column=1, row=5)

                    #Documentos
                    RG_txt = ttk.Label(frame_data, text='RG: ')
                    RG = ttk.Label(frame_data, text=dados['RG'])
                    RG_txt.grid(column=0, row=6)
                    RG.grid(column=1, row=6)

                    CPF_CNPJ_txt = ttk.Label(frame_data, text='CPF/CNPJ: ')
                    CPF_CNPJ = ttk.Label(frame_data, text=dados['CPF_CNPJ'])
                    CPF_CNPJ_txt.grid(column=0, row=7)
                    CPF_CNPJ.grid(column=1, row=7)

                    Cadastrado_por_txt = ttk.Label(frame_data, text='Cadastrado por: ')
                    Cadastrado_por = ttk.Label(frame_data, text=dados['Cadastrado_por'])
                    Cadastrado_por_txt.grid(column=0, row=8)
                    Cadastrado_por.grid(column=1, row=8)

                    Area_que_atua_txt = ttk.Label(frame_data, text='Area que atua: ')
                    Area_que_atua = ttk.Label(frame_data, text=dados['Area_que_atua'])
                    Area_que_atua_txt.grid(column=0, row=9)
                    Area_que_atua.grid(column=1, row=9)

                elif(Tipo_dado.get() == self.Search_data_type_value[2]):

                    Taxa_txt = ttk.Label(frame_data, text='Nome da Taxa: ')
                    Taxa = ttk.Label(frame_data, text=dado_selecionado.get())
                    Taxa_txt.grid(column=0, row=0)
                    Taxa.grid(column=1, row=0)

                    #Documentos
                    Valor_taxa_txt = ttk.Label(frame_data, text='Valor da taxa: ')
                    Valor_taxa = ttk.Label(frame_data, text=dados)
                    Valor_taxa_txt.grid(column=0, row=1)
                    Valor_taxa.grid(column=1, row=1)



                elif(Tipo_dado.get() == self.Search_data_type_value[3]):


                    Tarefa_txt = ttk.Label(frame_data, text='Tarefa: ')
                    Tarefa = ttk.Label(frame_data, text= dados['Tarefa'] )
                    Tarefa_txt.grid(column=0, row=0)
                    Tarefa.grid(column=1, row=0)

                    #Documentos
                    Data_txt = ttk.Label(frame_data, text='Data: ')
                    Data = ttk.Label(frame_data, text=dados['Data'])
                    Data_txt.grid(column=0, row=1)
                    Data.grid(column=1, row=1)

                    Hora_txt = ttk.Label(frame_data, text='Hora: ')
                    Hora = ttk.Label(frame_data, text=dados['Hora'])
                    Hora_txt.grid(column=0, row=2)
                    Hora.grid(column=1, row=2)

    def Orcamento(self):
            status_janela, janela = self.withdraw_func(self.new_budget,'350x350','Novo Orçamento')
            self.new_budget = janela
            Search_value = ""
            if(status_janela == 'Criar janela'):


    def menus(self,window_menu):
        menu = tk.Menu(window_menu)
        arquivos_menu = tk.Menu(menu,tearoff=0)
        funcionarios_menu = tk.Menu(menu,tearoff=0)
        consulta_menu = tk.Menu(menu,tearoff=0)

        arquivos_menu.add_command(label = 'Inserir Dados', command = lambda: self.Inserir_Dados())#OK
        arquivos_menu.add_command(label = 'Editar Dados', command = lambda: self.Editar_Dados())
        arquivos_menu.add_command(label = 'Excluir Dados', command = lambda: self.Excluir_Dados())#OK
        arquivos_menu.add_command(label ='Carregar Arquivo', command=lambda: self.Carregar_Arquivo())
        arquivos_menu.add_command(label ='Exportar Arquivo', command=lambda: self.Exportar_Arquivo())

        consulta_menu.add_command(label = 'Pesquisar Dados', command = lambda: self.Pesquisar_Dados())#OK
        consulta_menu.add_command(label = 'Novo Orçamento', command = lambda: self.Orcamento())

        menu.add_cascade(label ='Arquivo', menu=arquivos_menu)
        menu.add_command(label = 'Funcionarios', command=lambda :print('funcionarios'))
        menu.add_cascade(label = 'Consulta', menu=consulta_menu)
        window_menu.config(menu=menu)

    def estilos(self):
        estilo = ttk.Style()
        estilo.configure('TEntry', padx = 5)
        estilo.configure('TLabel', font = ('Open Sans Light', 12), background = '#10172f', foreground='#fefefe')
        estilo.configure('TLabel.big_font', font = ('Open Sans Light', 12), background = '#10172f', foreground='#fefefe')
        estilo.configure('TFrame', background = '#10172f')


    def withdraw_func(self, aba_executada, Tamanho_janela='250x200', Titulo='JANELA'):

        #Os módulos são:
         # self (root)
         # self.loading_screen
         # self.main_screen
         # self.insert_data
         # self.edit_data
         # self.exclude_data
         # self.search_data
         # self.import_file
         # self.export_file
         # self.new_budget

         #tem que inserir todo módulo aqui manualmente
        abas = [self,
          self.loading_screen,
          self.main_screen,
          self.insert_data,
          self.edit_data,
          self.exclude_data,
          self.search_data,
          self.import_file,
          self.export_file,
          self.new_budget]
        abas.remove(aba_executada)

        for aba in abas:
            try:
                aba.withdraw()
            except AttributeError:
                pass

        if(aba_executada == None):
            aba_executada = tk.Toplevel(self)
            aba_executada.geometry(Tamanho_janela)
            self.menus(aba_executada)
            aba_executada.config(bg="#10172f")

            frame_title = ttk.Frame(aba_executada)
            frame_title.pack()

            Nome_janela = ttk.Label(frame_title, text = Titulo)
            Nome_janela.pack()
            status_janela = 'Criar janela'

        else:
            status_janela = 'Exibir janela criada'
        aba_executada.deiconify()

        aba_executada.lift()
        aba_executada.protocol("WM_DELETE_WINDOW", self.destroy)
        return [status_janela, aba_executada]


if __name__ == '__main__':

    app = UI()
    app.mainloop()
