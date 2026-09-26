with source as (

    select * from {{ source('raw', 'raw_investments') }}

),

renamed as (

    select
        transaction_id,
        deal_id,
        user_id,
        product_id,
        cast(amount as decimal(14, 2)) as amount,
        cast(settled_at as timestamp) as settled_at

    from source

)

select * from renamed
