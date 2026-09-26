-- Funil por canal de aquisição (canal da primeira sessão do visitante).
-- Cada taxa de etapa compara com a etapa anterior. A taxa final compara aporte com visita.

with funnel as (

    select * from {{ ref('fct_visitor_funnel') }}

),

counts as (

    select
        acquisition_channel,
        acquisition_channel_type,
        count(*) as visitors,
        count(signed_up_at) as signups,
        count(kyc_submitted_at) as kyc_submitted,
        count(kyc_approved_at) as kyc_approved,
        count(first_simulation_at) as simulated,
        count(first_deal_at) as with_deal,
        count(first_investment_at) as investors,
        median(date_diff('day', signed_up_at, first_investment_at)) as median_days_signup_to_investment

    from funnel

    group by 1, 2

),

final as (

    select
        *,
        signups / nullif(visitors, 0) as rate_signup,
        kyc_submitted / nullif(signups, 0) as rate_kyc_submitted,
        kyc_approved / nullif(kyc_submitted, 0) as rate_kyc_approved,
        simulated / nullif(kyc_approved, 0) as rate_simulated,
        with_deal / nullif(simulated, 0) as rate_deal,
        investors / nullif(with_deal, 0) as rate_investment,
        investors / nullif(visitors, 0) as rate_visitor_to_investor

    from counts

)

select * from final
order by visitors desc
