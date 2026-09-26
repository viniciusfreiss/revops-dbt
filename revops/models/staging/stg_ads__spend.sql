with source as (

    select * from {{ source('raw', 'raw_ad_spend') }}

),

renamed as (

    select
        {{ dbt_utils.generate_surrogate_key(['date', 'channel', 'campaign_id']) }} as spend_id,
        cast(date as date) as spend_date,
        lower(channel) as channel,
        campaign_id,
        campaign_name,
        cast(cost as decimal(12, 2)) as cost,
        cast(impressions as integer) as impressions,
        cast(clicks as integer) as clicks

    from source

)

select * from renamed
