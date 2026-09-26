-- Crédito de cada toque em cada deal, em três modelos de atribuição.
-- O position based é o modelo oficial. First e last touch ficam para comparação.

with touchpoints as (

    select * from {{ ref('int_deal_touchpoints') }}

),

deals as (

    select
        deal_id,
        deal_stage

    from {{ ref('stg_hubspot__deals') }}

),

investments as (

    select
        deal_id,
        amount

    from {{ ref('stg_backend__investments') }}

),

weighted as (

    select
        touchpoints.touchpoint_id,
        touchpoints.deal_id,
        touchpoints.user_id,
        touchpoints.deal_number,
        touchpoints.session_id,
        touchpoints.touch_at,
        touchpoints.channel,
        touchpoints.channel_type,
        touchpoints.utm_campaign,
        touchpoints.touch_number,
        touchpoints.total_touches,

        deals.deal_stage,
        investments.deal_id is not null as is_won,
        coalesce(investments.amount, 0) as investment_amount,

        {{ position_based_weight('touchpoints.touch_number', 'touchpoints.total_touches') }}
            as weight_position_based,
        case when touchpoints.touch_number = 1 then 1.0 else 0.0 end
            as weight_first_touch,
        case when touchpoints.touch_number = touchpoints.total_touches then 1.0 else 0.0 end
            as weight_last_touch

    from touchpoints
    inner join deals
        on touchpoints.deal_id = deals.deal_id
    left join investments
        on touchpoints.deal_id = investments.deal_id

),

final as (

    select
        *,
        investment_amount * weight_position_based as revenue_position_based,
        investment_amount * weight_first_touch as revenue_first_touch,
        investment_amount * weight_last_touch as revenue_last_touch

    from weighted

)

select * from final
