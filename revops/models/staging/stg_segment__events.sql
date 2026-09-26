with source as (

    select * from {{ source('raw', 'raw_events') }}

),

renamed as (

    select
        event_id,
        anonymous_id,
        user_id,
        event_name,
        cast(event_at as timestamp) as event_at,
        platform,
        lower(utm_source) as utm_source,
        lower(utm_medium) as utm_medium,
        utm_campaign,
        product_id

    from source

)

select * from renamed
