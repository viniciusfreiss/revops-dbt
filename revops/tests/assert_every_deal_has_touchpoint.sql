-- Todo deal precisa de pelo menos um toque.
-- Um deal sem toque não recebe crédito de nenhum canal e some da atribuição.

select deals.deal_id

from {{ ref('stg_hubspot__deals') }} as deals
left join {{ ref('int_deal_touchpoints') }} as touchpoints
    on deals.deal_id = touchpoints.deal_id

where touchpoints.deal_id is null
