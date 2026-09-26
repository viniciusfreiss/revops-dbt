-- Uma linha por sessão, com o canal definido pelo evento de entrada.

with events as (

    select * from {{ ref('int_events_sessionized') }}

),

entry_events as (

    select
        session_id,
        utm_source,
        utm_medium,
        utm_campaign

    from events

    where event_sequence = 1

),

aggregated as (

    select
        session_id,
        anonymous_id,
        max(user_id) as user_id,
        max(platform) as platform,
        min(event_at) as started_at,
        max(event_at) as ended_at,
        count(*) as event_count,
        bool_or(event_name = 'product_viewed') as has_product_view,
        bool_or(event_name = 'simulation_completed') as has_simulation,
        bool_or(event_name = 'signup_completed') as has_signup

    from events

    group by 1, 2

),

final as (

    select
        aggregated.session_id,
        aggregated.anonymous_id,
        aggregated.user_id,
        aggregated.platform,
        aggregated.started_at,
        aggregated.ended_at,
        aggregated.event_count,

        entry_events.utm_source,
        entry_events.utm_medium,
        entry_events.utm_campaign,

        case
            when entry_events.utm_medium in ('cpc', 'paid_social') then entry_events.utm_source
            when entry_events.utm_medium = 'organic' then 'organic'
            else 'direct'
        end as channel,

        case
            when entry_events.utm_medium in ('cpc', 'paid_social') then 'paid'
            when entry_events.utm_medium = 'organic' then 'organic'
            else 'direct'
        end as channel_type,

        aggregated.has_product_view,
        aggregated.has_simulation,
        aggregated.has_signup

    from aggregated
    inner join entry_events
        on aggregated.session_id = entry_events.session_id

)

select * from final
