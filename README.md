Coisas feitas até agora:
- Criação e leitura do arquivo .ini contendo as configurações das localizações e pokémons;
- Representação dos caminhos utilizando grafos (biblioteca networkx);
- Começo e fim coloridos em verde e vermelho respectivamente;
- Cálculo do caminho mais curto utilizando Dijkstra.

Coisas para fazer:
- Movimentação pelo terminal (listar os vizinhos e escolher um lugar);
- Atualização dinâmica do mapa ao movimentar-se;
- Sistema de stamina (sei lá, não entendi a proposta da win condition).

O jogo se desenvolverá da seguinte forma:
- Utilizando grafos, mapeamos uma "cidade" para o jogador se locomover, com diferentes distâncias.
- O jogador poderá planejar essas rotas, tendo como condição de vitória a passagem por todos os locais de forma otimizada.
- Para calcular a melhor rota até o ginásio final percorrendo todos os locais será implementado algum algoritmo ainda não definido.
- Conceitos de OOP serão aplicados para o desenvolvimento do sistema de gerenciamento de recursos do jogador.
- Seguir as mecânicas de batalha descritas no arquivo (pois nunca joguei Pokémon :P)
- Se houver tempo, fazer uma interface gráfica bonitinha.