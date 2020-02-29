import os

print("\nMódulo de configuração")

while True:
        days = " "
        while not days.isdigit():                
            days = input("\nApós quantos dias deseja realziar a nova consulta?> ")
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
            option = input("Deseja alterar algum dado inserido, [s]im ou [n]ão/Enter?>")
            if option == "":
                option = "n"
        if option[0].lower() == "n" or option=="": break

with open(os.path.join("..","config.txt"), "w") as file:
    file.write("Intervalo de busca em dias: {days} #quantidade em dias\n".format(days=days))
    if download[0].lower() == "s":
        file.write("Download de imagens: on #on/off")
    else:
        file.write("Download de imagens: off #on/off")

print("\nArquivo de configuração gravado com sucesso!\n")