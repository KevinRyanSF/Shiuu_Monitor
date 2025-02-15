from Commands.Command import Command
from FacadeSingletonManager import FacadeManager
import time

class CommandTelaAmbiente(Command):
    def __init__(self):
        self.__facade = FacadeManager()

    def execute(self):
        current_command = self
        while True:
            self.__facade.clear_screen()
            print("TELA DE AMBIENTES")
            print("+--------------------------------------+")
            print("| 1. CADASTRAR AMBIENTE                |")
            print("| 2. VISUALIZAR AMBIENTES              |")
            print("| 3. MONITORAR AMBIENTE                |")
            print("| 4. EDITAR AMBIENTE                   |")
            print("| 5. DELETAR AMBIENTE                  |")
            print("| 6. SAIR                              |")
            print("+--------------------------------------+")
            opcao = input("ESCOLHA UMA OPÇÃO: ")

            if opcao == "1":
                self.__facade.cadastrar_ambiente()
                break
            elif opcao == "2":
                self.__facade.listar_ambientes()
                break
            elif opcao == "3":
                break
            elif opcao == "4":
                from Commands.CommandTelaEditAmbiente import CommandTelaEditAmbiente
                current_command = CommandTelaEditAmbiente()
                break
            elif opcao == "5":
                self.__facade.deletar_ambiente()
                break
            elif opcao == "6":
                from Commands.CommandTelaPrincipal import CommandTelaPrincipal
                print("Saindo...")
                current_command = CommandTelaPrincipal()
                break
            else:
                print("Opção inválida. Tente novamente.")
                time.sleep(2)
        time.sleep(2)
        current_command.execute()  # Chama o execute do comando que foi escolhido