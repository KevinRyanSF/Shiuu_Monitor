from Commands.Command import Command
from FacadeSingletonManager import FacadeManager
import time

class CommandTelaNivel(Command):
    def __init__(self):
        self.__facade = FacadeManager()

    def execute(self):
        current_command = self
        while True:
            self.__facade.clear_screen()
            print("TELA DE NÍVEIS")
            print("+--------------------------------------+")
            print("| 1. CADASTRAR NIVEL                   |")
            print("| 2. VISUALIZAR NÍVEIS                 |")
            print("| 3. EDITAR NÍVEL                      |")
            print("| 4. DELETAR NÍVEL                     |")
            print("| 5. SAIR                              |")
            print("+--------------------------------------+")
            opcao = input("ESCOLHA UMA OPÇÃO: ")

            if opcao == "1":
                self.__facade.cadastrar_nivel()
                break
            elif opcao == "2":
                self.__facade.listar_niveis()
                break
            elif opcao == "3":
                from Commands.CommandTelaEditNivel import CommandTelaEditNivel
                current_command = CommandTelaEditNivel()
                break
            elif opcao == "4":
                self.__facade.deletar_nivel()
                break
            elif opcao == "5":
                from Commands.CommandTelaPrincipal import CommandTelaPrincipal
                print("Saindo...")
                current_command = CommandTelaPrincipal()
                break
            else:
                print("Opção inválida. Tente novamente.")
                time.sleep(2)
        time.sleep(2)
        current_command.execute()  # Chama o execute do comando que foi escolhido