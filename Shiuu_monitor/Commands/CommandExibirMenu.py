from Commands.Command import Command
from Commands.CommandTelaPrincipal import CommandTelaPrincipal
from FacadeSingletonManager import FacadeManager
import time

class CommandExibirMenu(Command):
    def __init__(self):
        self.__facade = FacadeManager()

    def execute(self):
        current_command = self
        while True:
            self.__facade.clear_screen()
            print("TELA DE LOGIN")
            print("+--------------------------------------+")
            print("| 1. LOGIN                             |")
            print("| 2. SAIR                              |")
            print("+--------------------------------------+")
            opcao = input("ESCOLHA UMA OPÇÃO: ")

            if opcao == "1":
                login = self.__facade.login()
                if login:
                    current_command = CommandTelaPrincipal()
                    break
            elif opcao == "2":
                print("Saindo...")
                return 0
            else:
                print("Opção inválida. Tente novamente.")
                time.sleep(2)
        time.sleep(2)
        current_command.execute()  # Chama o execute do comando que foi escolhido







