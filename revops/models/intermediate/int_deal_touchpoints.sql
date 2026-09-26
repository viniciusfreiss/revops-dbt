-- Liga cada deal às sessões que aconteceram antes dele.
-- Janela de atribuição
--   entram as sessões do usuário até a criação do deal,
--   e a partir da criação do deal anterior do mesmo usuário (se existir).
-- Assim, cada sessão pertence a no máximo um deal.

with deals as (

    select
        deal_id,
        user_id,
        created_at as deal_created_at,
        lag(created_at) over (
            partition by user_id
            order by created_at, deal_id
        ) as previous_deal_created_at,
        row_number() over (
            partition by user_id
            order by created_at, deal_id
        ) as deal_number

    from {{ ref('stg_hubspot__deals') }}

),

sessions as (

    select
        session_id,
        user_id,
        started_at,
        channel,
        channel_type,
        utm_campaign

    from {{ ref('int_sessions') }}

    where user_id is not null

),

joined as (

    select
        deals.deal_id,
        deals.user_id,
        deals.deal_number,
        deals.deal_created_at,
        sessions.session_id,
        sessions.started_at as touch_at,
        sessions.channel,
        sessions.channel_type,
        sessions.utm_campaign

    from deals
    inner join sessions
        on sessions.user_id = deals.user_id
        and sessions.started_at <= deals.deal_created_at
        and (
            deals.previous_deal_created_at is null
            or sessions.started_at > deals.previous_deal_created_at
        )

),

numbered as (

    select
        {{ dbt_utils.generate_surrogate_key(['deal_id', 'session_id']) }} as touchpoint_id,
        deal_id,
        user_id,
        deal_number,
        session_id,
        touch_at,
        channel,
        channel_type,
        utm_campaign,
        row_number() over (
            partition by deal_id
            order by touch_at, session_id
        ) as touch_number,
        count(*) over (partition by deal_id) as total_touches,
        date_diff('day', touch_at, deal_created_at) as days_before_deal

    from joined

)

select * from numbered
