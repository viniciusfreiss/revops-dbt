-- Liga cada dispositivo anônimo ao usuário que se cadastrou nele.
-- O vínculo nasce no primeiro evento em que anonymous_id e user_id aparecem juntos.

with identified_events as (

    select
        anonymous_id,
        user_id,
        event_at

    from {{ ref('stg_segment__events') }}

    where user_id is not null

),

ranked as (

    select
        anonymous_id,
        user_id,
        event_at as linked_at,
        row_number() over (
            partition by anonymous_id
            order by event_at
        ) as link_order

    from identified_events

)

select
    anonymous_id,
    user_id,
    linked_at

from ranked

where link_order = 1
