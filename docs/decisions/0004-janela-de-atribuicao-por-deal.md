# 0004 Janela de atribuição por deal

## Contexto

Um usuário pode ter vários deals, um por produto. Se todos os toques da história dele valessem para todos os deals, o primeiro clique de meses atrás levaria crédito por aportes gerados por remarketing.

## Decisão

Cada deal recebe as sessões do usuário entre a criação do deal anterior e a criação do deal atual. O primeiro deal recebe tudo desde o primeiro acesso. O marco é a criação do deal, não o fechamento.

## Alternativas consideradas

- **Janela fixa em dias** (30 ou 90 dias antes do deal). Arbitrária, e poderia sobrepor deals próximos.
- **Fechamento do deal como marco.** O que acontece entre criação e fechamento é trabalho comercial, não resultado de mídia.
- **Todos os toques para todos os deals.** Contaria a mesma sessão várias vezes.

## Consequências

- Cada sessão pertence a no máximo um deal, garantido por um teste de unicidade de `session_id` em `int_deal_touchpoints`.
- Os deals seguintes têm em média 2 toques, contra 4,2 do primeiro deal.
- Sessões entre a criação e o fechamento de um deal vão para o próximo deal, se existir.
