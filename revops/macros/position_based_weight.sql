{#
    Peso de um toque no modelo position based.

    1 toque        100% para ele
    2 toques       dividido igualmente
    3 ou mais      primeiro e último recebem os pesos das vars,
                   o restante é dividido igualmente entre os do meio
#}

{% macro position_based_weight(touch_number, total_touches) %}

    {%- set first_w = var('attribution_first_touch_weight') -%}
    {%- set last_w = var('attribution_last_touch_weight') -%}
    {%- set middle_w = (1 - first_w - last_w) | round(6) -%}

    case
        when {{ total_touches }} = 1 then 1.0
        when {{ total_touches }} = 2 then 0.5
        when {{ touch_number }} = 1 then {{ first_w }}
        when {{ touch_number }} = {{ total_touches }} then {{ last_w }}
        else {{ middle_w }} / ({{ total_touches }} - 2)
    end

{% endmacro %}
