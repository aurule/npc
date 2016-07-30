<%page args="character"/>
<%def name="make_ranks(group_name)">\
    %if group_name in character['rank']:
 (${', '.join(character['rank'][group_name])})\
    %endif
</%def>\
<h1>${character.get_first('name')}\
%if 'dead' in character:
 (Deceased)\
%endif
</h1>

%if character.has_items('name', 2):
<div><em>AKA ${', '.join(character.get_remaining('name'))}</em></div>
%endif
%if character.has_items('title'):
<div>${', '.join(character['title'])}</div>
%endif
\
<div>${'/'.join(character['type'])}\
%if character.has_items('foreign'):
 in ${' and '.join(character['foreign'])}\
%endif
%if character.has_items('group'):
, ${character.get_first('group')}${make_ranks(character.get_first('group'))}\
%endif
</div>
\
%if character.has_items('motley'):
<div>\
${', '.join(["{} Motley{}".format(m, make_ranks(m)) for m in character['motley']])}\
</div>
%endif
\
%if character.has_items('group', 2):
<div>\
${', '.join(["{}{}".format(g, make_ranks(g)) for g in character.get_remaining('group')])}\
</div>
%endif
\
%if character.has_items('appearance'):
<p><em>Appearance:</em> ${' '.join(character['appearance'])}</p>
%endif
\
<p>${character['description']}</p>
\
%if character.has_items('dead'):
<p><em>Dead:</em> ${' '.join(character['dead'])}</p>
%endif
