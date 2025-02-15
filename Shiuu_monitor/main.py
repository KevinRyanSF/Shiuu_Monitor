from Commands.CommandExibirMenu import CommandExibirMenu

def main():
    menu_command = CommandExibirMenu()  # Criando o comando
    menu_command.execute()  # Executando o menu

if __name__ == "__main__":
    main()