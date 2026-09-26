# 0001 Dados sintéticos reproduzíveis

## Contexto

O projeto precisa de dados que liguem mídia, comportamento, CRM e aportes pela mesma identidade. Bases públicas não têm essa ligação, e dados reais de uma operação regulada não podem ser publicados.

## Decisão

Os dados são gerados por um script Python que simula pessoas, e as tabelas são consequência do que essas pessoas fazem. A geração usa semente fixa e quatro geradores aleatórios independentes, um por etapa (jornadas, eventos, deals e mídia), criados com `SeedSequence.spawn`.

A mídia é calculada a partir das sessões pagas que já existem nos eventos, e não o contrário.

## Alternativas consideradas

- **Bases públicas** como o sample do GA4. Descartada por não ter CRM nem receita ligados ao comportamento.
- **Um único gerador aleatório para tudo.** Funcionava no começo, mas qualquer mudança numa etapa alterava os números de todas as outras.
- **Gerar mídia e sessões de forma independente.** Nada garantiria que cliques e sessões batessem.

## Consequências

- Qualquer pessoa gera exatamente os mesmos dados, e o CI valida isso a cada push.
- Mudar a simulação de deals não altera cadastros nem eventos.
- Os dados só contêm os padrões que o gerador simula. A qualidade do lead por canal, por exemplo, não varia depois do cadastro.
