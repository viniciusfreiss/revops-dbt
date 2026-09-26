-- A receita atribuída tem que bater com o total aportado, em qualquer modelo.
-- Atribuição redistribui o dinheiro entre canais, nunca cria nem some com ele.

with totals as (

    select
        (select sum(amount) from {{ ref('stg_backend__investments') }}) as invested,
        (select sum(revenue_position_based) from {{ ref('fct_touchpoint_attribution') }}) as position_based,
        (select sum(revenue_first_touch) from {{ ref('fct_touchpoint_attribution') }}) as first_touch,
        (select sum(revenue_last_touch) from {{ ref('fct_touchpoint_attribution') }}) as last_touch

)

select *

from totals

where abs(invested - position_based) > 0.01
   or abs(invested - first_touch) > 0.01
   or abs(invested - last_touch) > 0.01
