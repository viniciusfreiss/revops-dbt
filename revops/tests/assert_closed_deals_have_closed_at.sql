-- Deal ganho ou perdido precisa ter data de fechamento, e deal aberto não pode ter.
-- O teste falha se esta query devolver alguma linha.

select
    deal_id,
    deal_stage,
    closed_at

from {{ ref('stg_hubspot__deals') }}

where (deal_stage in ('ganho', 'perdido') and closed_at is null)
   or (deal_stage not in ('ganho', 'perdido') and closed_at is not null)
