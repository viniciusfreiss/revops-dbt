-- Em cada deal, os pesos de cada modelo precisam somar 1.
-- Se não somarem, o modelo está criando ou perdendo crédito.

select
    deal_id,
    sum(weight_position_based) as total_position_based,
    sum(weight_first_touch) as total_first_touch,
    sum(weight_last_touch) as total_last_touch

from {{ ref('fct_touchpoint_attribution') }}

group by deal_id

having abs(sum(weight_position_based) - 1) > 0.0001
    or abs(sum(weight_first_touch) - 1) > 0.0001
    or abs(sum(weight_last_touch) - 1) > 0.0001
