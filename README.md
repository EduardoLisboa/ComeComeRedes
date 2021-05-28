# ComeComeRedes

Este repositório foi criado para hospedar o jogo ComeCome, projeto final da disciplina de Redes de Computadores. O jogo foi desenvolvido na linguagem Python e utiliza a biblioteca Pygames.

## Instruções para execução

Para executar o jogo, é recomendado que se tenha a biblioteca Pygame instalada em seu computador. Caso você utilize alguma distribuição Linux, a instalação pode ser feita através do seguinte comando:

```python3 -m pip install -U pygame --user```

Para verificar como instalar a biblioteca em outros sistemas operacionais, clique [aqui](https://www.pygame.org/wiki/GettingStarted).

Após a instalação da biblioteca, é preciso que se execute o arquivo server.py para inicializar o servidor através do seguinte comando:

```python3 server.py```

Em seguida, que seja executado o arquivo game.py em dois terminais diferentes, através do comando:

```python3 game.py```

Depois das execuções, o jogo abrirá duas telas para ser executado em paralelo e jogado por dois jogadores.

Caso o código não funcione depois dos comandos, é recomendável que se altere o "host" nos arquivos "server" e "network" para o endereço IPv4 da máquina em que o servidor está sendo rodado.
