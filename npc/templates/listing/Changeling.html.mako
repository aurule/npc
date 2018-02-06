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
%if character.has_items('motley'):
, ${character.get_first('motley')} Motley${make_ranks(character.get_first('motley'))}\
%endif
%if character.has_items('court'):
, ${character.get_first('court')} Court${make_ranks(character.get_first('court'))}\
%else:
, Courtless
%endif
%if character.has_items('freehold'):
 (${character.get_first('freehold')})
%endif
</div>
\
<%
has_seeming = character.has_items('seeming')
has_kith = character.has_items('kith')
%>\
%if has_seeming or has_kith:
<div>\
    %if has_seeming:
${'/'.join(character['seeming'])}\
        %if has_kith:
${' '}\
        %endif
    %endif
    %if has_kith:
${'/'.join(character['kith'])}\
    %endif
</div>
%endif
\
%if character.has_items('entitlement'):
<div>\
${character.get_first('entitlement')}${make_ranks(character.get_first('entitlement'))}
</div>
%endif
\
%if character.has_items('group'):
<div>\
%for g in character['group']:
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
%if character.has_items('mien'):
${mdconv('*Mien:* ' + ' '.join(character['mien']))}
%endif
%if character.has_items('mask'):
${mdconv('*Mask:* ' + ' '.join(character['mask']))}
%endif
\
${mdconv('*Notes:* ' + character['description'])}
\
%if character.has_items('dead'):
${mdconv('*Dead:* ' + ' '.join(character['dead']))}
%endif
