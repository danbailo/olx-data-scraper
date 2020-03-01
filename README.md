# OLX Scraper

## Descrição
Este projeto consiste em coletar os dados dos anúncios nos quais os links para esses anúncios se encontram no arquivo [input.txt](input.txt). Os dados são armazenados num banco de dados PostgreSQL. O usuário também tem a opção de baixar as imagens referentes aos anúncios e essas imagens são armazenadas no diretório `~/imgs/` que será criado automaticamente após a execução do programa.

As imagens serão separadas por pasta, onde o nome de cada pasta consiste no ID do anúncio. Ao final da execução, será mostrado a quantidade total de imagens que foram baixadas.

---
## Dependências

Para instalar as dependências, execute o comando abaixo num terminal na raiz do projeto:

* `make prepare-dev`

---
## Como usar

Para executar o programa, abra um terminal na raiz do projeto e execute:

* `make run`

### Informacoes

* `make [help]` - Exibe as informacoes sobre cada comando.
* `make config` - Modulo para configurar a frequencia de execucao do programa principal e habilitar/desabilitar o download das imagens;
* `make db-config` - Modulo para configurar a conexao ao banco de dados.
---