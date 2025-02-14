from Commands.Command import Command
from FacadeSingletonManager import FacadeManager
import time

class CommandTelaPrincipal(Command):
    def __init__(self):
        self.__facade = FacadeManager()

    def execute(self):
        current_command = self
        while True:
            self.__facade.clear_screen()
            print("TELA PRINCIPAL")
            print("+--------------------------------------+")
            print("| 1. USUÁRIOS                          |")
            print("| 2. SAIR                              |")
            print("+--------------------------------------+")
            opcao = input("ESCOLHA UMA OPÇÃO: ")

            if opcao == "1":
                from Commands.CommandUsuario import CommandUsuario
                current_command = CommandUsuario()
                break
            elif opcao == "2":
                from Commands.CommandExibirMenu import CommandExibirMenu
                print("Saindo...")
                current_command = CommandExibirMenu()
                break
            else:
                print("Opção inválida. Tente novamente.")
                time.sleep(2)
        current_command.execute()  # Chama o execute do comando que foi escolhido