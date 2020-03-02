from termcolor import colored
import os

print("\n# Pressione ctrl+c para finalizar o programa!")

print("\n{msg}".format(msg=colored("Módulo de configuração.", "blue")))

try:
    while True:
            days = " "
            while not days.isdigit():                
                days = input("\nApós quantos dias deseja realizar a nova consulta?> ")
                if not days.isdigit():
                    print('Por favor, entre apenas com valores numéricos!')

            download = " "
            while download[0].lower() not in ["s", "n"]:
                download = input("\nDeseja realizar o download das imagens, [s]im ou [n]ão?> ")
                if download == "":
                    download = " "
                if download[0].lower() not in ["s", "n"]:
                    print('Por favor, entre com "sim" ou "não"!')
            print()
            option = " "
            while option[0].lower() not in ["s", "n"]:
                option = input("Deseja alterar alguma informação inserida, [s]im ou [n]ão/Enter?>")
                if option == "":
                    option = "n"
            if option[0].lower() == "n" or option=="": break
except KeyboardInterrupt:
    print("\n\nPrograma finalizado!")
    exit()

with open(os.path.join("config", "config.txt"), "w") as file:
    file.write("Intervalo de busca em dias: {days} #quantidade em dias\n".format(days=days))
    if download[0].lower() == "s":
        file.write("Download de imagens: on #on/off\n")
    else:
        file.write("Download de imagens: off #on/off\n")

print("\nArquivo de configuração gravado com {success}!\n".format(success=colored("SUCESSO", "green")))