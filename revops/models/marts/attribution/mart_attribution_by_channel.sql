-- Resultado da atribuição por canal, comparando os três modelos.

with attribution as (

    select * from {{ ref('fct_touchpoint_attribution') }}

),

by_channel as (

    select
        channel,
        channel_type,

        sum(weight_position_based) as deals_position_based,
        sum(case when is_won then weight_position_based else 0 end) as won_deals_position_based,

        sum(revenue_position_based) as revenue_position_based,
        sum(revenue_first_touch) as revenue_first_touch,
        sum(revenue_last_touch) as revenue_last_touch

    from attribution

    group by 1, 2

),

final as (

    select
        *,
        revenue_position_based / sum(revenue_position_based) over () as revenue_share_position_based,
        revenue_first_touch / sum(revenue_first_touch) over () as revenue_share_first_touch,
        revenue_last_touch / sum(revenue_last_touch) over () as revenue_share_last_touch

    from by_channel

)

select * from final
order by revenue_position_based desc
