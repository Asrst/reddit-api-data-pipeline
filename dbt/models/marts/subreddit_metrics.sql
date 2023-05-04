{{ config(materialized='table') }}

with all_posts as (
    select *
    from {{ ref('stg_all_posts') }}
)

select sub_reddit
    , LAST_DAY(DATE_TRUNC(cast(created_utc as date), MONTH)) as date_ending
    , count(distinct post_id) as num_posts
    , count(distinct author) as num_active_users
    , sum(num_comments) as comments_obtained
    , sum(case when author = '[deleted]' then 1 else 0 end) as num_posts_deleted
from all_posts
group by 1, 2