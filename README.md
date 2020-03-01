# OLX Scraper

## Descrição
Este projeto consiste em coletar os dados dos anúncios nos quais os links para esses anúncios se encontram no arquivo [input.txt](input.txt). Os dados são armazenados num banco de dados PostgreSQL. O usuário também tem a opção de baixar as imagens referentes aos anúncios e essas imagens são armazenadas no diretório `/imgs/` que será criado automaticamente após a execucao do programa.

As imagens serao separadas por pasta, onde o nome de cada pasta e o ID do anuncio.

---
## Dependências

Para instalar as dependências, execute o comando abaixo num terminal/power sheel/prompt de comando de comando:

* `make prepare-dev`

---
## Como usar

Para executar o programa, abra um terminal/power sheel/prompt de comando e como parâmetro de execução do mesmo é preciso passar o link da pesquisa que foi realizada na OLX e como parâmetro opcional, você pode escolher o nome da planilha que será gravado os números.:

* `make run`

#TODO

---