import json

class Aux_func():
    """docstring for Aux_func."""

    def Carregar_config(self):
            with open('Orçamentos/Data/config.json', 'r+', encoding ='utf8') as Data_config:
                configs = json.load(Data_config)
                # print(configs)
                return configs


    def Abrir_Json(self):
        with open('Orçamentos\Data\Data.json', 'r+', encoding ='utf8') as Data_json:
            Data = json.load(Data_json)
            return Data


    def Editar_Json(self, Dados_alterados):
        with open('Orçamentos\Data\Data.json', 'w', encoding ='utf8') as Data_json:
            json.dump(Dados_alterados, Data_json, indent=3)


    def Inserir_Dados(self, **dados):
        cfg = self.Carregar_config()
        data_type = cfg["Insert_data_type_value"]
        print(dados['Tipo_dado'])

        Database = self.Abrir_Json()
        if(dados['Tipo_dado'] == data_type[0]):

            User_index = str(len(Database["Usuarios"]))
            Database["Usuarios"][User_index] = {}
            Database["Usuarios"][User_index]["Username"]= dados['User'].get()
            Database["Usuarios"][User_index]["Password"]= dados['Senha'].get()
            Database["Usuarios"][User_index]["Permissions"]= dados['Perms'].get()

        elif(dados['Tipo_dado'] == data_type[1]):

            Func_index = str(len(Database["Funcionarios"]))
            Database["Funcionarios"][Func_index] = {}
            Database["Funcionarios"][Func_index]["Nome"]= dados['Nome'].get()
            Database["Funcionarios"][Func_index]["Cargo"]= dados['Cargo'].get()
            Database["Funcionarios"][Func_index]["Telefone"]= dados['Telefone'].get()
            Database["Funcionarios"][Func_index]["Telefone2"]= dados['Telefone2'].get()
            Database["Funcionarios"][Func_index]["Email"]= dados['Email'].get()
            Database["Funcionarios"][Func_index]["Endereco"]= dados['Endereco'].get()
            Database["Funcionarios"][Func_index]["RG"]= dados['RG'].get()
            Database["Funcionarios"][Func_index]["CPF_CNPJ"]= dados['CPF_CNPJ'].get()
            Database["Funcionarios"][Func_index]["Cadastrado_por"]= dados['Cadastrado_por']
            Database["Funcionarios"][Func_index]["Area_que_atua"]= dados['Area_que_atua'].get()


        elif(dados['Tipo_dado'] == data_type[2]):
            # Database["Taxas"]dados['Taxa'].get()
            Database["Taxas"][dados['Taxa'].get()]= dados['Valor_taxa'].get()


        elif(dados['Tipo_dado'] == data_type[3]):

            #
            # "Tarefa": Tarefa
            # "Data" : Data
            # "Hora" : Hora
            pass
        self.Editar_Json(Database)

    def Excluir_Dados(self, tipo_dado, dado_selecionado):
        cfg = self.Carregar_config()
        data_type = cfg["Delete_data_type_value"]

        Database = self.Abrir_Json()
        if(tipo_dado.get() == data_type[0]):
            del Database["Usuarios"][str(dado_selecionado.current())]

        elif(tipo_dado.get() == data_type[1]):

            del Database["Funcionarios"][str(dado_selecionado.current())]

        elif(tipo_dado.get() == data_type[2]):
            del Database["Taxas"][dado_selecionado.get()]


        elif(tipo_dado.get() == data_type[3]):

            #
            # "Tarefa": Tarefa
            # "Data" : Data
            # "Hora" : Hora
            pass

        self.Editar_Json(Database)

    def Pesquisar_infos(self, tipo_info, modo):
        cfg = self.Carregar_config()

        if(modo == 'pesquisar dados'):
            data_type = cfg["Search_data_type_value"]
        elif(modo == 'deletar dados'):
            data_type = cfg["Delete_data_type_value"]


        Database = self.Abrir_Json()
        if(tipo_info == data_type[0]):
            Usuarios_list = []
            for Usuario in Database["Usuarios"]:
                Usuarios_list.append(Database["Usuarios"][Usuario]["Username"])

            return Usuarios_list

        elif(tipo_info == data_type[1]):

            Func_list = []
            for Func in Database["Funcionarios"]:
                Func_list.append(Database["Funcionarios"][Func]["Nome"])

            return Func_list

        elif(tipo_info == data_type[2]):

            Taxas_list = []
            for Taxa in Database["Taxas"]:
                Taxas_list.append(Taxa)

            return Taxas_list

        elif(tipo_info == data_type[3]):
            print(Database["Tarefas"])
            return Database["Tarefas"]



    def get_dados(self, tipo_info, tipo_dado, modo):
            cfg = self.Carregar_config()

            if(modo == 'pesquisar dados'):
                data_type = cfg["Search_data_type_value"]
            elif(modo == 'deletar dados'):
                data_type = cfg["Delete_data_type_value"]
            Database = self.Abrir_Json()


            if(tipo_info.get() == data_type[0]):

                return Database["Usuarios"][str(tipo_dado.current())]

            elif(tipo_info.get() == data_type[1]):

                return Database["Funcionarios"][str(tipo_dado.current())]

            elif(tipo_info.get() == data_type[2]):

                return Database["Taxas"][tipo_dado.get()]

            elif(tipo_info.get() == data_type[3]):
                print(Database["Tarefas"])
                return Database["Tarefas"]





    def Login_verification(self, User, Senha):
        Data = self.Abrir_Json()
        for User_index in Data["Usuarios"]:
            if(User == Data["Usuarios"][User_index]["Username"]):
                if(Senha == Data["Usuarios"][User_index]["Password"]):
                    return ['Login bem-sucedido!',
                    Data["Usuarios"][User_index],
                    Data["Usuarios"][User_index]["Username"],
                    Data["Usuarios"][User_index]["Permissions"]]
                else:
                    return ['Senha Incorreta!',None, None, None]
            else:
                return ['Usuário incorreto!',None, None, None]
