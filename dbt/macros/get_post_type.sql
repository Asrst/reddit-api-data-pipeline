 {#
    This macro returns the post_type using the url of the subreddit posts 
#}

{% macro get_post_type(post_url) -%}

    case {{ post_url }}
        when like '%i.redd%' then 'image'
        when like '%v.redd%' then 'video'
        when like '%comments%' then 'text'
        when like '%gallery%' then 'gallery'
        else 'external_link'
    end

{%- endmacro %}

              