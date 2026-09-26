-- Todo real gasto em mídia precisa aparecer no mart de unit economics.
-- Se sobrar gasto, existe canal com custo que nunca gerou um toque em deal.

with totals as (

    select
        (select sum(cost) from {{ ref('stg_ads__spend') }}) as spend_staging,
        (select sum(spend) from {{ ref('mart_channel_unit_economics') }}) as spend_mart

)

select *

from totals

where abs(spend_staging - spend_mart) > 0.01
