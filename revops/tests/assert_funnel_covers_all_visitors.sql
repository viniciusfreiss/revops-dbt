-- O funil precisa ter todos os visitantes e todos os usuários, sem perder nem duplicar.

with totals as (

    select
        (select count(distinct anonymous_id) from {{ ref('stg_segment__events') }}) as visitors_events,
        (select count(*) from {{ ref('fct_visitor_funnel') }}) as visitors_funnel,
        (select count(*) from {{ ref('stg_backend__users') }}) as users_backend,
        (select count(user_id) from {{ ref('fct_visitor_funnel') }}) as users_funnel

)

select *

from totals

where visitors_events != visitors_funnel
   or users_backend != users_funnel
