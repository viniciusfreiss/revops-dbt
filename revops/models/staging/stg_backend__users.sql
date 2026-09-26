with source as (

    select * from {{ source('raw', 'raw_users') }}

),

renamed as (

    select
        user_id,
        cast(created_at as timestamp) as signed_up_at,
        signup_platform

    from source

)

select * from renamed
