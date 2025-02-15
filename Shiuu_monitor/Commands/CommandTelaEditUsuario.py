from Commands.Command import Command
from FacadeSingletonManager import FacadeManager
import time

class CommandTelaEditUsuario(Command):
    def __init__(self):
        self.__facade = FacadeManager()

    def execute(self):
        current_command = self
        user = self.__facade.buscar_usuario()
        if user:
            while True:
                self.__facade.clear_screen()
                print(f"Editar {user['nome']}")
                print("+--------------------------------------+")
                print("| 1. NOME                              |")
                print("| 2. CARGO                             |")
                print("| 3. SENHA                             |")
                print("| 4. ADICIONAR AMBIENTES               |")
                print("| 5. REMOVER AMBIENTES                 |")
                print("| 6. VOLTAR                            |")
                print("+--------------------------------------+")
                opcao = input("ESCOLHA UMA OPÇÃO: ")

                if opcao == "1":
                    from Commands.CommandTelaUsuario import CommandTelaUsuario
                    current_command = CommandTelaUsuario()
                    self.__facade.editar_nome_usuario(user['email'])
                    break
                elif opcao == "2":
                    from Commands.CommandTelaUsuario import CommandTelaUsuario
                    current_command = CommandTelaUsuario()
                    self.__facade.editar_cargo_usuario(user['email'])
                    break
                elif opcao == "3":
                    from Commands.CommandTelaUsuario import CommandTelaUsuario
                    current_command = CommandTelaUsuario()
                    self.__facade.editar_senha_usuario(user['email'])
                    break
                elif opcao == "4":
                    from Commands.CommandTelaUsuario import CommandTelaUsuario
                    current_command = CommandTelaUsuario()
                    self.__facade.adicionar_ambientes_usuario(user['email'])
                    break
                elif opcao == "5":
                    from Commands.CommandTelaUsuario import CommandTelaUsuario
                    current_command = CommandTelaUsuario()
                    self.__facade.remover_ambientes_usuario(user['email'])
                    break
                elif opcao == "6":
                    from Commands.CommandTelaUsuario import CommandTelaUsuario
                    print("Voltando...")
                    current_command = CommandTelaUsuario()
                    break
                else:
                    print("Opção inválida. Tente novamente.")
                    time.sleep(2)
        time.sleep(2)
        current_command.execute()  # Chama o execute do comando que foi escolhido