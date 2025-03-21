# PokeJourney

Bem vindo à PokeJourney!

Essa aventura se passa em uma cidade mapeada por meio de grafos, onde cada localização é um nó conectado por caminhos de diferentes distâncias.

Nesse jogo, você deverá passar por cada local antes de enfrentar o chefe da cidade, batalhando e gerenciando seus recursos ao longo do caminho.

Para ajudá-lo nessa jornada, seu movimento é dado pelo algoritmo de Dijkstra, que calcula a melhor rota até o destino escolhido, permitindo que você otimize seu tempo e recursos.

_Esse jogo foi desenvolvido por Allan Duarte Ehlert para o projeto final da cadeira Algoritmos e Estruturas de Dados II._

## Como jogar
1. No terminal, selecione o local que você deseja visitar digitando o número associado com o grafo.
2. Se você ainda não visitou o local que está nesse momento, você entrará em uma batalha (ainda não implementado).
3. Ganhe o jogo passando por todas as batalhas e derrotando o chefe da cidade!

## Como rodar
```
$ pip install -r requirements.txt
$ python main.py
```

## Detalhes Técnicos

### Coisas feitas até agora:
- Criação e leitura do arquivo .ini contendo as configurações das localizações e pokémons;
- Representação dos caminhos utilizando grafos coloridos (utilizando networkx);
- Movimentação pelo terminal (calcula a rota mais curta usando Dijkstra e realiza os movimentos);
- Atualização dinâmica do mapa ao movimentar-se;
- CLI interface bonita (mais ou menos :P)

### Coisas para fazer:
- Sistema de batalha;
- Greedy algo com os stats dos pokemons (auto-play);
- Classes e conceitos de OOP para gerenciamento de recursos;
- Melhorar a UI.