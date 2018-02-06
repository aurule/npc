<%page args="character, mdconv"/>
<%def name="make_ranks(group_name)">\
    %if group_name in character['rank']:
 (${', '.join(character['rank'][group_name])})\
    %endif
</%def>\
<h3>${character.get_first('name')}\
%if 'dead' in character:
 (Deceased)\
%endif
</h3>

%if character.has_items('name', 2):
<div><em>AKA ${', '.join(character.get_remaining('name'))}</em></div>
%endif
%if character.has_items('title'):
<div>${', '.join(character['title'])}</div>
%endif
\
<div>${'/'.join(character['type'])}\
%if character.has_locations:
 in ${' and '.join(character.locations)}\
%elif character.has_items('foreign'):
 (foreign)
%endif
%if 'wanderer' in character:
, Wanderer\
%endif
%if character.has_items('group'):
, ${character.get_first('group')}${make_ranks(character.get_first('group'))}\
%endif
</div>
\
%if character.has_items('motley'):
<div>\
${character.get_first('motley')} Motley${make_ranks(character.get_first('motley'))}\
</div>
%endif
\
%if character.has_items('group', 2):
<div>\
%for g in character.get_remaining('group'):
${g}${make_ranks(g)}\
    %if not loop.last:
${', '}
    %endif
%endfor
</div>
%endif
\
%if character.has_items('appearance'):
${mdconv('*Appearance:* ' + ' '.join(character['appearance']))}
%endif
\
${mdconv('*Notes:* ' + character['description'])}
\
%if character.has_items('dead'):
${mdconv('*Dead:* ' + ' '.join(character['dead']))}
%endif
