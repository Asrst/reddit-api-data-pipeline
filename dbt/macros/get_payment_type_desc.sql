 {#
    This macro returns the description of the payment_type 
#}

{% macro get_payment_type_desc(payment_type) -%}

    case {{ payment_type }}
        when 1 then 'Credit card'
        when 2 then 'Cash'
        when 3 then 'No charge'
        when 4 then 'Dispute'
        when 5 then 'Cancelled'
        when 6 then 'Unknown'
    end

{%- endmacro %}

              