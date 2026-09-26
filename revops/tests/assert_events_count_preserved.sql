-- O join com o mapa de identidade não pode criar nem perder eventos.

with counts as (

    select
        (select count(*) from {{ ref('stg_segment__events') }}) as staging_events,
        (select count(*) from {{ ref('int_events_identified') }}) as identified_events

)

select *

from counts

where staging_events != identified_events
