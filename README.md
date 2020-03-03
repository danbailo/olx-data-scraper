# OLX Scraper

## Descrição
Este projeto consiste em coletar os dados dos anúncios nos quais os caminhos para esses anúncios se encontram no arquivo [input.txt](input.txt). 

Os dados coletados são armazenados num banco de dados PostgreSQL.

 O usuário também tem a opção de realizar o download das imagens referentes aos anúncios, essas imagens serão armazenadas no diretório `~/imgs/`, que será criado automaticamente após a execução do programa.

As imagens serão separadas por pasta, onde o nome de cada pasta consiste no ID do anúncio. Ao final da execução, será mostrado a quantidade total de imagens que foram baixadas.

---

Todos os comandos devem ser executados num terminal na pasta raiz do programa.


## Dependências

* `make prepare-dev` - Executa o comando para instalar as dependências do programa.

---
## Como usar

Para executar o programa, abra um terminal na raiz do projeto e execute:

* `make` ou `make help` - Exibe as informações sobre cada comando.

* `make config` - Executa o módulo para configurar a frequência de execução do programa principal e habilita/desabilita o download das imagens;

* `make db-config` - Executa o módulo para configurar a conexão com o banco de dados.

* `make run` - Executa o programa principal.
---