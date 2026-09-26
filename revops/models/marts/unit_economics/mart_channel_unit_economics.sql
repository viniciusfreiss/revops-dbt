-- Custo, aquisição e retorno por canal, com crédito position based.
--
-- Definições
--   novo investidor   usuário no seu primeiro aporte liquidado
--   CAC               gasto dividido por novos investidores atribuídos
--   captação          volume aportado (não é receita)
--   receita           captação multiplicada pela var revenue_take_rate

with attribution as (

    select * from {{ ref('fct_touchpoint_attribution') }}

),

first_investments as (

    -- O primeiro aporte liquidado de cada usuário marca a aquisição
    select deal_id

    from (
        select
            deal_id,
            row_number() over (
                partition by user_id
                order by settled_at, transaction_id
            ) as investment_number

        from {{ ref('stg_backend__investments') }}
    )

    where investment_number = 1

),

spend as (

    select
        channel,
        sum(cost) as spend

    from {{ ref('stg_ads__spend') }}

    group by 1

),

credited as (

    select
        attribution.channel,
        attribution.channel_type,

        sum(case when first_investments.deal_id is not null
            then attribution.weight_position_based else 0 end) as new_investors,

        sum(case when first_investments.deal_id is not null
            then attribution.revenue_position_based else 0 end) as captacao_new_investors,

        sum(case when first_investments.deal_id is null
            then attribution.revenue_position_based else 0 end) as captacao_repeat,

        sum(attribution.revenue_position_based) as captacao_total

    from attribution
    left join first_investments
        on attribution.deal_id = first_investments.deal_id

    group by 1, 2

),

final as (

    select
        credited.channel,
        credited.channel_type,
        coalesce(spend.spend, 0) as spend,

        credited.new_investors,
        credited.captacao_new_investors,
        credited.captacao_repeat,
        credited.captacao_total,
        credited.captacao_total * {{ var('revenue_take_rate') }} as revenue,

        spend.spend / nullif(credited.new_investors, 0) as cac,
        credited.captacao_total / nullif(spend.spend, 0) as captacao_per_real,
        credited.captacao_total * {{ var('revenue_take_rate') }}
            / nullif(spend.spend, 0) as revenue_roas

    from credited
    left join spend
        on credited.channel = spend.channel

)

select * from final
order by spend desc
