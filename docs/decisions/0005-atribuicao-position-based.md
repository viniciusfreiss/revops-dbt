# 0005 Atribuição position based 40/20/40

## Contexto

Operações de inside sales têm jornadas longas, com canais que iniciam o interesse e canais que capturam a conversão. First touch e last touch valorizam só um desses papéis.

## Decisão

O modelo oficial é position based. O primeiro e o último toque recebem 40% cada, e os do meio dividem 20%. Jornadas com 2 toques dividem 50/50, e com 1 toque ele recebe 100%. A regra fica na macro `position_based_weight`, com os pesos nas vars do projeto.

First touch e last touch são calculados junto, na mesma tabela, para comparação.

## Alternativas consideradas

- **Last touch.** O Google cairia de 19,7% para 14,0% da captação, apesar de ser o canal que mais inicia jornadas.
- **Linear.** Trata igual um toque que iniciou a jornada e um que só passou por ela.
- **Markov ou Shapley.** Mais robustos, mas exigem volume maior e são menos explicáveis para o time comercial. Ficam como evolução natural.

## Consequências

- O crédito reflete os dois papéis sem ignorar o meio da jornada.
- Os pesos são uma escolha de negócio, não uma estimativa causal. Mudar para 30/40/30 é só alterar duas vars.
- Um unit test cobre os casos de 1, 2 e 4 toques. Ele encontrou um erro de ponto flutuante (`1 - 0.4 - 0.4` resultava em `0.19999...`), corrigido com arredondamento na macro.
