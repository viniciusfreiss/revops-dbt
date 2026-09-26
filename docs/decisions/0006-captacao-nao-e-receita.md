# 0006 Captação não é receita

## Contexto

Numa plataforma de renda fixa, o valor aportado pertence ao investidor. A plataforma ganha uma fração, a taxa de distribuição ou estruturação. Tratar o aporte como receita inflaria o retorno de todos os canais.

## Decisão

O mart de unit economics separa **captação**, o volume aportado, de **receita**, a captação multiplicada pela var `revenue_take_rate`. O valor de 2% é uma premissa declarada, não um dado.

O CAC usa apenas o primeiro aporte liquidado de cada usuário, porque cliente recorrente já foi adquirido antes.

## Alternativas consideradas

- **Usar a captação direto como receita.** Resultaria em ROAS cerca de 50 vezes maior e sem significado econômico.
- **Taxa por produto.** Mais precisa, mas o gerador não diferencia a margem entre CRI, CRA, debênture e CCB.

## Consequências

- O ROAS mede o retorno real para a plataforma, dado o take rate assumido.
- Qualquer mudança na premissa altera o ROAS de todos os canais na mesma proporção.
- O ROAS cobre só a janela simulada de seis meses. Clientes adquiridos no fim do período ainda não tiveram tempo de aportar de novo, o que pede uma análise de coorte com LTV e payback.
