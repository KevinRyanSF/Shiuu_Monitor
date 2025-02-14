from Commands.Command import Command
from FacadeSingletonManager import FacadeManager
import time

class CommandUsuario(Command):
    def __init__(self):
        self.__facade = FacadeManager()

    def execute(self):
        current_command = self
        while True:
            self.__facade.clear_screen()
            print("TELA DE USUÁRIOS")
            print("+--------------------------------------+")
            print("| 1. CADASTRAR USUÁRIO                 |")
            print("| 2. VISUALIZAR USUÁRIO                |")
            print("| 3. EDITAR USUÁRIO                    |")
            print("| 4. DELETAR USUÁRIO                   |")
            print("| 5. SAIR                              |")
            print("+--------------------------------------+")
            opcao = input("ESCOLHA UMA OPÇÃO: ")

            if opcao == "1":
                self.__facade.cadastrar_usuario()
                break
            elif opcao == "2":
                self.__facade.listar_usuarios()
                break
            elif opcao == "3":
                self.__facade.editar_usuario()
                break
            elif opcao == "4":
                delete = self.__facade.deletar_usuario()
                break
            elif opcao == "5":
                from Commands.CommandTelaPrincipal import CommandTelaPrincipal
                print("Saindo...")
                current_command = CommandTelaPrincipal()
                break
            else:
                print("Opção inválida. Tente novamente.")
                time.sleep(2)
        current_command.execute()  # Chama o execute do comando que foi escolhido