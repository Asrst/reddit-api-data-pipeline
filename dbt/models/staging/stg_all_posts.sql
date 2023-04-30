{{ config(materialized='view') }}

with ipl_subreddit as 
(
  select *, 'ipl' as sub_reddit
  from {{ source('bq_subreddit','ext_ipl') }}
  where EXTRACT(YEAR FROM created_utc) = 2022
),

stranger_things_subreddit as (
    select *, 
        'stranger_things' as sub_reddit
    from {{ source('bq_subreddit','ext_stranger_things') }}
    where EXTRACT(YEAR FROM created_utc) = 2022
), 

technology_subreddit as (
    select *, 
        'technology' as sub_reddit
    from {{ source('bq_subreddit','ext_technology') }}
    where EXTRACT(YEAR FROM created_utc) = 2022
)

select
    -- identifiers
    id as post_id,
    -- timestamps
    cast(created_utc as timestamp) as created_utc,
    -- user info
    author, 
    ifnull(author_flair_type, 'unknown'),
    ifnull(author_premium, 'unknown'),
    -- engagement
    cast(score as numeric) as score,
    cast(upvote_ratio as numeric) as upvote_ratio,
    cast(num_comments as integer) as num_comments,
    cast(num_crossposts as integer) as num_crossposts,
    -- booleans
    over_18 as is_18_plus,
    spoiler as has_spolier,
     -- strings
    {{ get_post_type('url') }} as post_type,
    ifnull(post_hint, 'unknown') as post_hint,
    title as title,
    sub_reddit
from ipl_subreddit

union all

select
    -- identifiers
    id as post_id,
    -- timestamps
    cast(created_utc as timestamp) as created_utc,
    -- user info
    author, 
    ifnull(author_flair_type, 'unknown'),
    ifnull(author_premium, 'unknown'),
    -- engagement
    cast(score as numeric) as score,
    cast(upvote_ratio as numeric) as upvote_ratio,
    cast(num_comments as integer) as num_comments,
    cast(num_crossposts as integer) as num_crossposts,
    -- booleans
    over_18 as is_18_plus,
    spoiler as has_spolier,
    -- strings
    {{ get_post_type('url') }} as post_type,
    ifnull(post_hint, 'unknown') as post_hint,
    title as title,
    sub_reddit
from stranger_things_subreddit

union all

select
    -- identifiers
    id as post_id,
    -- timestamps
    cast(created_utc as timestamp) as created_utc,
    -- user info
    author, 
    ifnull(author_flair_type, 'unknown'),
    ifnull(author_premium, 'unknown'),
    -- engagement
    cast(score as numeric) as score,
    cast(upvote_ratio as numeric) as upvote_ratio,
    cast(num_comments as integer) as num_comments,
    cast(num_crossposts as integer) as num_crossposts,
    -- booleans
    over_18 as is_18_plus,
    spoiler as has_spolier,
    -- strings
    {{ get_post_type('url') }} as post_type,
    ifnull(post_hint, 'unknown') as post_hint,
    title as title,
    sub_reddit
from technology_subreddit


-- dbt build --m <model.sql> --var 'is_test_run: true'
{% if var('is_test_run', default=false) %}

  limit 1000

{% endif %}
