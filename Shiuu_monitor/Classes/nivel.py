class Nivel:
    def __init__(self, nome, limite, alerta):
        self.nome = nome
        self.limite = limite
        self.alerta = alerta
        from FacadeSingleton.FacadeSingletonManager import FacadeManager
        self.__facade = FacadeManager()


    def deletar_nivel(self):
            confirma = input(f"Deseja deletar o ambiente: {self.nome}? [Y/N]").upper()
            if confirma == "Y":
                self.__facade.db.delete("niveis", "nome", self.nome)
                print("Nível deletado com sucesso!")
                return True
            else:
                return False

    def editar_nome_nivel(self):
        nome = input("Digite o novo nome: ")
        if nome == self.nome:
            print("Valor igual ao atual, insira outro valor.")
        else:
            self.__facade.db.update("niveis", "nome", "nome", nome, self.nome)

    def editar_limite_nivel(self):
        limite = int(input("Digite o novo limite: "))
        if limite == self.limite:
            print("Valor igual ao atual, insira outro valor.")
        else:
            self.__facade.db.update("niveis", "limite", "nome", limite, self.nome)
            print("Valor alterado com sucesso!")

    def editar_alerta_nivel(self):
        alerta = input("Digite a mensagem de alerta: ")
        if alerta == self.alerta:
            print("Valor igual ao atual, insira outro valor.")
        else:
            self.__facade.db.update("niveis", "alerta", "nome", alerta, self.nome)
            print("Valor alterado com sucesso!")