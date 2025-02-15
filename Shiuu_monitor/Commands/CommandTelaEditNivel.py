from Commands.Command import Command
from FacadeSingletonManager import FacadeManager
import time


class CommandTelaEditNivel(Command):
    def __init__(self):
        self.__facade = FacadeManager()

    def execute(self):
        current_command = self
        nivel = self.__facade.buscar_niveis()
        if nivel:
            while True:
                self.__facade.clear_screen()
                print(f"Editar {nivel['nome']}")
                print("+--------------------------------------+")
                print("| 1. NOME                              |")
                print("| 2. LIMITE                            |")
                print("| 3. ALERTA                            |")
                print("| 4. SAIR                              |")
                print("+--------------------------------------+")
                opcao = input("ESCOLHA UMA OPÇÃO: ")

                if opcao == "1":
                    from Commands.CommandTelaNivel import CommandTelaNivel
                    current_command = CommandTelaNivel()
                    self.__facade.editar_nome_nivel(nivel['nome'])
                    break
                elif opcao == "2":
                    from Commands.CommandTelaNivel import CommandTelaNivel
                    current_command = CommandTelaNivel()
                    self.__facade.editar_limite_nivel(nivel['nome'])
                    break
                elif opcao == "3":
                    from Commands.CommandTelaNivel import CommandTelaNivel
                    current_command = CommandTelaNivel()
                    self.__facade.editar_alerta_nivel(nivel['nome'])
                    break
                elif opcao == "4":
                    from Commands.CommandTelaNivel import CommandTelaNivel
                    print("Saindo...")
                    current_command = CommandTelaNivel()
                    break
                else:
                    print("Opção inválida. Tente novamente.")
                    time.sleep(2)
        time.sleep(2)
        current_command.execute()  # Chama o execute do comando que foi escolhido