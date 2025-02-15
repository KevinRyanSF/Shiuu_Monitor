from Commands.Command import Command
from FacadeSingletonManager import FacadeManager
import time


class CommandTelaEditAmbiente(Command):
    def __init__(self):
        self.__facade = FacadeManager()

    def execute(self):
        current_command = self
        ambiente = self.__facade.buscar_ambiente()
        if ambiente:
            while True:
                self.__facade.clear_screen()
                print(f"Editar {ambiente['nome']}")
                print("+--------------------------------------+")
                print("| 1. NOME                              |")
                print("| 2. ID DO DISPOSITIVO                 |")
                print("| 3. IP DO DISPOSITIVO                 |")
                print("| 4. PORTA DO DISPOSITIVO              |")
                print("| 5. ADICIONAR NÍVEIS                  |")
                print("| 6. REMOVER NÍVEIS                    |")
                print("| 7. SAIR                              |")
                print("+--------------------------------------+")
                opcao = input("ESCOLHA UMA OPÇÃO: ")

                if opcao == "1":
                    from Commands.CommandTelaAmbiente import CommandTelaAmbiente
                    current_command = CommandTelaAmbiente()
                    self.__facade.editar_nome_ambiente(ambiente['nome'])
                    break
                elif opcao == "2":
                    from Commands.CommandTelaAmbiente import CommandTelaAmbiente
                    current_command = CommandTelaAmbiente()
                    self.__facade.editar_dispositivo_id_ambiente(ambiente['nome'])
                    break
                elif opcao == "3":
                    from Commands.CommandTelaAmbiente import CommandTelaAmbiente
                    current_command = CommandTelaAmbiente()
                    self.__facade.editar_dispositivo_ip_ambiente(ambiente['nome'])
                    break
                elif opcao == "4":
                    from Commands.CommandTelaAmbiente import CommandTelaAmbiente
                    current_command = CommandTelaAmbiente()
                    self.__facade.editar_dispositivo_port_ambiente(ambiente['nome'])
                    break
                elif opcao == "5":
                    from Commands.CommandTelaAmbiente import CommandTelaAmbiente
                    current_command = CommandTelaAmbiente()
                    self.__facade.adicionar_niveis_ambiente(ambiente['nome'])
                    break
                elif opcao == "6":
                    from Commands.CommandTelaAmbiente import CommandTelaAmbiente
                    current_command = CommandTelaAmbiente()
                    self.__facade.remover_niveis_ambiente(ambiente['nome'])
                    break
                elif opcao == "7":
                    from Commands.CommandTelaAmbiente import CommandTelaAmbiente
                    print("Saindo...")
                    current_command = CommandTelaAmbiente()
                    break
                else:
                    print("Opção inválida. Tente novamente.")
                    time.sleep(2)
        time.sleep(2)
        current_command.execute()  # Chama o execute do comando que foi escolhido