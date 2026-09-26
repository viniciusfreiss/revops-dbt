-- Agrupa os eventos de navegação em sessões.
-- Uma sessão nova começa quando
--   é o primeiro evento do dispositivo,
--   passou mais que o timeout desde o evento anterior,
--   ou o evento chega com UTM (nova entrada por campanha).
-- Eventos disparados pelo backend ficam de fora, porque não representam visita.

with events as (

    select * from {{ ref('int_events_identified') }}

    where event_name not in (
        {%- for e in var('server_side_events') %}
        '{{ e }}'{% if not loop.last %},{% endif %}
        {%- endfor %}
    )

),

with_previous as (

    select
        *,
        lag(event_at) over (
            partition by anonymous_id
            order by event_at, event_id
        ) as previous_event_at

    from events

),

flagged as (

    select
        *,
        case
            when previous_event_at is null then 1
            when event_at - previous_event_at
                > interval '{{ var("session_timeout_minutes") }} minutes' then 1
            when utm_source is not null then 1
            else 0
        end as is_new_session

    from with_previous

),

numbered as (

    select
        *,
        sum(is_new_session) over (
            partition by anonymous_id
            order by event_at, event_id
            rows between unbounded preceding and current row
        ) as session_number

    from flagged

),

final as (

    select
        {{ dbt_utils.generate_surrogate_key(['anonymous_id', 'session_number']) }} as session_id,
        event_id,
        anonymous_id,
        user_id,
        session_number,
        row_number() over (
            partition by anonymous_id, session_number
            order by event_at, event_id
        ) as event_sequence,
        event_name,
        event_at,
        platform,
        utm_source,
        utm_medium,
        utm_campaign,
        product_id

    from numbered

)

select * from final
