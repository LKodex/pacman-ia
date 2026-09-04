# pacman-ia

Aluno: [Lucas Gonçalves Cordeiro](mailto:lucas.g.cordeiro@ufms.br) (2021.1906.031-0)

O projeto está público no GitHub -> [LKodex/pacman-ia](https://github.com/LKodex/pacman-ia)

## Resumo do Projeto

Deverão ser implementados algoritmos Minimax, Minimax com poda Alfa-Beta e Expectimax em uma versão do jogo do Pacman fornecida pelo professor. Também deverá ser implementada um algoritmo de avaliação `betterEvaluationFunction` melhor que o algoritmo padrão que considera apenas a pontuação atual do jogo.

As regras do Pacman são:
- Ganha 10 pontos por comida (não inclui cápsulas)
- Perde 1 ponto a cada movimento (inclusive se manter parado)
- Ganha 500 pontos ao vencer
- Perde 500 pontos ao perder
- Ganha 500 pontos ao comer um fantasma usando o poder da cápsula

## O que foi feito

Foram implementados todos os algoritmos: Minimax, poda Alfa-Beta e Expectimax.

No algoritmo de avaliação `betterEvaluationFunction` foram implementadas as seguintes diretivas.
- Utiliza a pontuação atual do jogo como base.
- Remove pontos para cada Comida restante (peso 50 para cada)
- Remove pontos para cada Cápsula restante (peso 50 para cada)
- Remove pontos por quão longe o Pacman está da Comida ou Cápsula mais próxima (peso 5 para cada unidade de distância)
- Remove pontos adicionais por derrota (peso 250 para derrota)
- Adiciona pontos adicionais por vitória (peso 250 para vitória)
- Adiciona pontos por quão próximo o Fanstama está das Cápsulas e o quão próximo o Pacman está desse Fantasma (peso 500. O peso máximo é atingido quando o Fantasma está até 2 unidades de distância da Cápsula e o Pacman está até 3 unidades da cápsula mais próxima do Fantasma. Veja o cálculo a seguir)

### Cálculo da Heurística de Distância entre Cápsulas, Fantasmas e o Pacman

A pontuação somada na pontuação total é dada pela seguinte definição

- `W` = Peso da heurística = 500
- `P` = Pacman
- `G` = Fantasma
- `C` = Cápsula
- `d(a, b)` = Distância de `a` até `b`

> `Pontuação Adicional = W * min(1, 1 / (max(2, d(G, C)) - 1) ^ 2) * min(1, 1 / (max(2, d(P, C)) - 1) ^ 2)`

Basicamente considerando um peso de até 100% para ambas as distâncias independentes que se movem exponencialmente em direção a 0% conforme a distância aumenta e que serão multiplicados pelo peso real de 500.

Essa função foi pouco explorada e tem espaço para ajustes e testes com diferentes valores, por exemplo, aumentar a distância em que será considerado o peso máximo.

Nota: Apesar da complexidade ligeiramente superior as outras heurísticas essa não deve possuir muito impacto geral além de incentivar o Pacman a aproveitar de momentos que ele pode facilmente pontuar com a captura dos fantasmas.

### Cálculo de Distância até as Comidas e Cápsulas

Essa é a heurística mais relevante do algoritmo junto a heurística de comidas e cápsulas restantes que previnem que o Pacman fique parado ou andando em zigue-zague de um lado para o outro. Usando o algoritmo de _pathfinding_ de Dijkstra é calculada a distância até a comida ou cápsula mais próxima e multiplicada por um peso de 5.

## Changelog 04/09/2026

Após mostrar o algoritmo para um amigo ele por curiosidade jogou o código em um modelo de IA que identificou um bug na conta `Pontuação Adicional = W * 1^(2 / max(1, d(G, C))) * 1^(2 / max(1, d(P, G)))` onde o peso sempre era multiplicado por 100% em todos os casos (pois 1 elevado a qualquer número continua sendo 1). Também identifiquei que o Pacman continuava com comportamentos de zigue-zague ou de ficar parado quando a próxima comida disponível estava muito distante. Com esses problemas identificados realizei as seguintes tratativas:

- Aumentado o peso por comida restante de 25 para 50
- Aumentado o peso por cápsula restante de 25 para 50
- Substituído o cálcuo anterior de pontuação adicional por proximidade do fanstasma a cápsulas de `Pontuação Adicional = W * 1^(2 / max(1, d(G, C))) * 1^(2 / max(1, d(P, G)))` para `Pontuação Adicional = W * min(1, 1 / (max(2, d(G, C)) - 1) ^ 2) * min(1, 1 / (max(2, d(P, C)) - 1) ^ 2)`

O cálculo da distância do Pacman até o Fantasma foi substituído pelo cálculo do Pacman até a Cápsula pois o cálculo anterior promovia um comportamento perseguidor.

Com o novo cálculo agora é corretamente aplicada a intenção de reduzir o peso da heurística exponencialmente de acordo com a distância do Fantasma até a Cápsula e do Pacman até a cápsula  
