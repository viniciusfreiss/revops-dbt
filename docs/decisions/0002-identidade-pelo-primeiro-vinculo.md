# 0002 Identidade pelo primeiro vínculo

## Contexto

O Segment só preenche `user_id` a partir do cadastro. Tudo o que a pessoa fez antes, incluindo o clique no anúncio que a trouxe, fica associado apenas ao `anonymous_id` do dispositivo. Sem ligar os dois, a atribuição perderia o primeiro toque.

## Decisão

O modelo `int_identity_map` liga cada `anonymous_id` ao `user_id` do primeiro evento em que os dois aparecem juntos. Os eventos anônimos anteriores recebem esse `user_id` em `int_events_identified`.

## Alternativas consideradas

- **Tabela de identifies separada**, como o Segment real produz. Descartada para manter o projeto com cinco fontes, já que a co-ocorrência nos eventos carrega a mesma informação.
- **Último vínculo em vez do primeiro.** Em dispositivos compartilhados, o último cadastro roubaria o histórico de quem usou o dispositivo antes.
- **Grafo de identidade entre dispositivos.** Fora do escopo, porque o gerador simula um dispositivo por pessoa.

## Consequências

- A resolução recuperou 6.926 eventos anteriores ao cadastro, praticamente dobrando o histórico conhecido de quem converteu.
- Uma pessoa que usa dois dispositivos aparece como dois visitantes até se cadastrar em cada um.
- Os testes garantem que todo usuário está no mapa e que o join não cria nem perde eventos.
