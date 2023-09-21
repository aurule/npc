{% block name -%}
    {{- "#" * header_level + " " -}}
    {{- character.realname -}} {% if has("dead") -%}
        {{ " (Deceased)" }}
    {%- endif -%}
{%- endblock -%}

{%-block aka -%}
    {# titles and other names the character has #}
    {%- if has("name") -%}
        {{ "\n\n*AKA " + character.name.all() | join(", ") + "*" }}
    {%- endif -%}
    {%- if has("title") -%}
        {{ "\n\n" + character.title.all() | join(", ") }}
    {%- endif -%}
{%- endblock -%}

{{- "\n\n" -}}

{%- block vitals -%}
    {# vital info: race, age, location, pronouns, etc. #}
    {%- if has("race") -%}
        {{ character.race.first() | title }}
    {%- else -%}
        {{ character.type | title }}
    {%- endif -%}

    {%- if has("foreign") -%}
        (foreign)
    {%- endif -%}
    {%- if has("wanderer") -%}
        , Wanderer
    {%- endif -%}
    {%- if has("group") -%}
        , {{ character.group.first() }} ({{ character.group.first().rank.all() | join(", ") }})
    {%- endif -%}
    {%- if has("pronouns") -%}
        ; {{ character.pronouns.all() | join(", ") }}
    {%- endif -%}
{%- endblock -%}
