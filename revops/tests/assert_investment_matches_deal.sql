-- O aporte precisa pertencer ao mesmo usuário e ao mesmo produto do deal que o originou.
-- O teste falha se esta query devolver alguma linha.

select
    i.transaction_id,
    i.deal_id,
    i.user_id as investment_user_id,
    d.user_id as deal_user_id,
    i.product_id as investment_product_id,
    d.product_id as deal_product_id

from {{ ref('stg_backend__investments') }} as i
inner join {{ ref('stg_hubspot__deals') }} as d
    on i.deal_id = d.deal_id

where i.user_id != d.user_id
   or i.product_id != d.product_id
