-- A soma de eventos das sessões precisa bater com o total de eventos sessionizados.
-- Se não bater, alguma sessão se perdeu no join com o evento de entrada.

with counts as (

    select
        (select count(*) from {{ ref('int_events_sessionized') }}) as sessionized_events,
        (select sum(event_count) from {{ ref('int_sessions') }}) as events_in_sessions

)

select *

from counts

where sessionized_events != events_in_sessions
