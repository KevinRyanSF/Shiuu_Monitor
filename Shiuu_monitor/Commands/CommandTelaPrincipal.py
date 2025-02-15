from Commands.Command import Command
from FacadeSingletonManager import FacadeManager
import time

class CommandTelaPrincipal(Command):
    def __init__(self):
        self.__facade = FacadeManager()

    def execute(self):
        current_command = self
        log_user = self.__facade.get_usuario_logado()
        while True:
            self.__facade.clear_screen()
            print(f"TELA PRINCIPAL  ({log_user['nome']})".upper())
            print("+--------------------------------------+")
            print("| 1. USUÁRIOS                          |")
            print("| 2. AMBIENTES                         |")
            print("| 3. NÍVEIS                            |")
            print("| 4. RELATÓRIO                         |")
            print("| 5. SAIR                              |")
            print("+--------------------------------------+")
            opcao = input("ESCOLHA UMA OPÇÃO: ")

            if opcao == "1":
                from Commands.CommandTelaUsuario import CommandTelaUsuario
                current_command = CommandTelaUsuario()
                break
            elif opcao == "2":
                from Commands.CommandTelaAmbiente import CommandTelaAmbiente
                current_command = CommandTelaAmbiente()
                break
            elif opcao == "3":
                from Commands.CommandTelaNivel import CommandTelaNivel
                current_command = CommandTelaNivel()
                break
            elif opcao == "4":
                from Commands.CommandExibirMenu import CommandExibirMenu
                print("Saindo...")
                current_command = CommandExibirMenu()
                break
            elif opcao == "5":
                from Commands.CommandExibirMenu import CommandExibirMenu
                print("Saindo...")
                current_command = CommandExibirMenu()
                self.__facade.logout()
                break
            else:
                print("Opção inválida. Tente novamente.")
                time.sleep(2)
        time.sleep(2)
        current_command.execute()  # Chama o execute do comando que foi escolhido