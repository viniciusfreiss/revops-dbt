-- Eventos com o usuário resolvido, inclusive os que aconteceram antes do cadastro.

with events as (

    select * from {{ ref('stg_segment__events') }}

),

identity_map as (

    select * from {{ ref('int_identity_map') }}

),

joined as (

    select
        events.event_id,
        events.anonymous_id,
        coalesce(events.user_id, identity_map.user_id) as user_id,
        events.user_id is null
            and identity_map.user_id is not null as is_backfilled,
        events.event_name,
        events.event_at,
        events.platform,
        events.utm_source,
        events.utm_medium,
        events.utm_campaign,
        events.product_id

    from events
    left join identity_map
        on events.anonymous_id = identity_map.anonymous_id

)

select * from joined
