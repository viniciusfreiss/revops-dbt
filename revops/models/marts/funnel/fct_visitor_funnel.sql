-- Jornada de cada visitante pelo funil, do primeiro acesso ao primeiro aporte.
-- Uma linha por dispositivo (anonymous_id). Cada etapa guarda a primeira vez
-- em que foi alcançada, ou nulo se nunca foi.

with first_sessions as (

    select
        anonymous_id,
        started_at as first_seen_at,
        channel as acquisition_channel,
        channel_type as acquisition_channel_type

    from (
        select
            *,
            row_number() over (
                partition by anonymous_id
                order by started_at, session_id
            ) as session_order

        from {{ ref('int_sessions') }}
    )

    where session_order = 1

),

identity_map as (

    select * from {{ ref('int_identity_map') }}

),

users as (

    select * from {{ ref('stg_backend__users') }}

),

user_events as (

    select
        user_id,
        min(case when event_name = 'kyc_submitted' then event_at end) as kyc_submitted_at,
        min(case when event_name = 'kyc_approved' then event_at end) as kyc_approved_at,
        min(case when event_name = 'simulation_completed' then event_at end) as first_simulation_at

    from {{ ref('int_events_identified') }}

    where user_id is not null

    group by 1

),

first_deals as (

    select
        user_id,
        min(created_at) as first_deal_at

    from {{ ref('stg_hubspot__deals') }}

    group by 1

),

first_investments as (

    select
        user_id,
        min(settled_at) as first_investment_at

    from {{ ref('stg_backend__investments') }}

    group by 1

),

final as (

    select
        first_sessions.anonymous_id,
        identity_map.user_id,
        first_sessions.acquisition_channel,
        first_sessions.acquisition_channel_type,

        first_sessions.first_seen_at,
        users.signed_up_at,
        user_events.kyc_submitted_at,
        user_events.kyc_approved_at,
        user_events.first_simulation_at,
        first_deals.first_deal_at,
        first_investments.first_investment_at

    from first_sessions
    left join identity_map
        on first_sessions.anonymous_id = identity_map.anonymous_id
    left join users
        on identity_map.user_id = users.user_id
    left join user_events
        on identity_map.user_id = user_events.user_id
    left join first_deals
        on identity_map.user_id = first_deals.user_id
    left join first_investments
        on identity_map.user_id = first_investments.user_id

)

select * from final
