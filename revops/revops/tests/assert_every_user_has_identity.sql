-- Todo usuário cadastrado precisa aparecer no mapa de identidade.
-- Se faltar alguém, os eventos anteriores ao cadastro dele ficaram sem dono.

select users.user_id

from {{ ref('stg_backend__users') }} as users
left join {{ ref('int_identity_map') }} as identity_map
    on users.user_id = identity_map.user_id

where identity_map.user_id is null
