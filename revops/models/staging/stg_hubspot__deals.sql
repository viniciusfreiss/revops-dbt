with source as (

    select * from {{ source('raw', 'raw_deals') }}

),

renamed as (

    select
        deal_id,
        user_id,
        product_id,
        stage as deal_stage,
        cast(created_at as timestamp) as created_at,
        cast(closed_at as timestamp) as closed_at

    from source

)

select * from renamed
