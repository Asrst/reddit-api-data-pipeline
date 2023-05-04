{{ config(materialized='table') }}

with all_posts as (
    select *
    from {{ ref('stg_all_posts') }}
)

select author
    , count(distinct post_id) as num_posts
    , sum(num_comments) as comments_obtained
    , avg(score) as avg_post_score
    , avg(upvote_ratio) as avg_upvote_ratio
    , count(distinct sub_reddit) as num_active_subreddits
from all_posts
where author <> '[deleted]'
group by author