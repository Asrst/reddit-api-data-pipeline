 {#
    This macro returns the post_type using the url of the subreddit posts 
#}

{% macro get_post_type(post_url) -%}

    case
        when {{ post_url }} like '%i.redd%' then 'image'
        when {{ post_url }} like '%v.redd%' then 'video'
        when {{ post_url }} like '%comments%' then 'text'
        when {{ post_url }} like '%gallery%' then 'gallery'
        else 'external_link'
    end

{%- endmacro %}

              