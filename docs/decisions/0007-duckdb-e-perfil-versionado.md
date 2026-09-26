# 0007 DuckDB com perfil versionado

## Contexto

O projeto precisa rodar igual na máquina de qualquer pessoa e no CI, sem depender de conta em warehouse na nuvem.

## Decisão

O warehouse é o DuckDB, um banco em arquivo local. Os parquets são lidos direto como sources, pela configuração `external_location`. O `profiles.yml` fica dentro de `revops/` e é versionado.

## Alternativas consideradas

- **BigQuery, Snowflake ou Redshift.** Exigiriam credenciais e custo para quem quisesse rodar o projeto.
- **Perfil em `~/.dbt`.** É o padrão recomendado, mas o CI não teria acesso a ele.

## Consequências

- O projeto roda com `pip install` e quatro comandos, sem nenhuma configuração manual.
- Versionar o perfil só é seguro porque o DuckDB não tem senha. Com banco remoto, o perfil nunca deve ir para o repositório. O próprio arquivo registra essa exceção.
- O SQL usa algumas funções do DuckDB (`date_diff`, `bool_or`, `median`). Migrar para outro warehouse exigiria ajustes pontuais.
