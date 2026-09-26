# 0003 Eventos de backend fora das sessões

## Contexto

`kyc_approved` e `investment_started` são disparados pelo sistema, horas ou dias depois da última ação da pessoa. Sessionizados como os demais, cada um abriria uma sessão sem UTM, classificada como direct.

## Decisão

Esses eventos ficam fora de `int_events_sessionized`. A lista está na var `server_side_events` do `dbt_project.yml`. Eles continuam disponíveis em `int_events_identified`, que é de onde o funil os lê.

## Alternativas consideradas

- **Sessionizar tudo.** O `investment_started` acontece no momento do aporte, então a sessão falsa seria o último toque de quase todo deal. O direct receberia 40% do crédito de praticamente todos os aportes sem ter feito nada.
- **Identificar pela biblioteca que enviou o evento**, como o Segment real permite. O gerador não simula esse campo, então a lista explícita cumpre o mesmo papel.

## Consequências

- O último toque de cada deal reflete uma visita real.
- Um evento novo de backend precisa ser incluído na var, ou vai gerar sessões falsas sem nenhum erro visível.
