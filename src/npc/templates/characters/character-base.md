{% block name -%}
    {{- "#" * header_level + " " -}}
    {{- character.realname -}} {% if has("dead") -%}
        {{ " (Deceased)" }}
    {%- endif -%}
{%- endblock -%}

{%- block portrait -%}
    {# portrait image. Only used if portrait tag is set. #}
    {%- if has("portrait") -%}
        <img src="/{{ character.portrait.first() }}" class="align-right decor-shadow" width="150px" loading="lazy">
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
    {{ character.race.all() | join("/") }}
{%- else -%}
    {{ character.type | title }}
{%- endif -%}
{%- if has("age") -%}
    , {{ character.age.all() | join("/") }}
{%- endif -%}
{%- if has("pronouns") -%}
    , {{ character.pronouns.all() | join(", ") }}
{%- endif -%}
{%- endblock -%}

{%- block orgs -%}
    {# group and org membership #}
    {%- if has("org") -%}
        {{- "\n\n**Member of:**\n" -}}
        {%- for org in character.org.all() -%}
            {{- "\n* " -}}
            {{- org.value -}}
            {%- if org.has("rank") -%}
                {{- ", " + org.rank.all() | join(", ") -}}
            {%- endif -%}
            {%- if org.has("role") -%}
                {{- " (" + org.role.all() | join(", ") + ")"-}}
            {%- endif -%}
        {%- endfor -%}
    {%- endif -%}
{%- endblock -%}

{%- block location -%}
    {# details of the character's location #}
    {%- if has("location") -%}
        {{- "\n" -}}
        {%- for location in character.location.all() -%}
            {{- "\n" -}}
            {%- if location.has("wanderer") -%}
                {{- "Wanders " -}}
            {%- else -%}
                {{- "Found in " -}}
            {%- endif -%}
            {%- if location.has("region") -%}
                {%- for region in location.region.all() -%}
                    {%- if region.has("locale") -%}
                        {{- region.locale.all() | join(" and ") + ", " -}}
                    {% endif %}
                    {{- region.value + ", " -}}
                {%- endfor -%}
            {%- endif -%}
            {{- location -}}
            {%- if not loop.last %}; {% endif -%}
        {%- endfor -%}
    {%- endif -%}
{%- endblock -%}

{%- block employment -%}
    {# details about the charcters job #}
    {%- if has("employer") -%}
        {{- "\n" -}}
        {%- for employer in character.employer.all() -%}
            {{- "\nEmployed by " + employer.value -}}
            {%- if employer.has("job") -%}
                {{- " as a " + employer.job.all() | join(" and ") -}}
            {%- endif -%}
            {%- if not loop.last %}; {% endif -%}
        {%- endfor -%}
    {%- endif -%}
{%- endblock -%}

{%- block system -%}
{# extra info specific to a game system. Like FATE aspects and such. Blank by default. #}
{%- endblock -%}

{%- block appearance -%}
    {# character appearance #}
    {%- if has("appearance") -%}
        {{- "\n\n*Appearance:* " + character.appearance.all() | join(' ') -}}
    {%- endif -%}
{%- endblock -%}

{%- block description -%}
    {# character description #}
    {{- "\n\n" + character.description -}}
{%- endblock -%}

{%- block dead -%}
    {# details about the character's death #}
    {%- if has("dead") and character.dead.first().value -%}
        {{- "\n\n*Deceased:* " + character.dead.all() | join(' ') -}}
    {%- endif -%}
{%- endblock %}
