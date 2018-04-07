<%page args="character, header_level, mdconv"/>
<%def name="make_ranks(group_name)">\
    %if group_name in character['rank']:
 (${', '.join(character['rank'][group_name])})\
    %endif
</%def>\
${"<h{}>".format(header_level)}
${character.get_first('name')}\
%if 'dead' in character:
 (Deceased)\
%endif
${"</h{}>".format(header_level)}

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

%if character.has_items('pack'):
${character.get_first('pack')} Pack${make_ranks(character.get_first('pack'))}\
%endif
%if character.has_items('tribe'):
, ${character.get_first('tribe')} Tribe${make_ranks(character.get_first('tribe'))}\
%else:
, Ghost Wolf
%endif
</div>
\
%if character.has_items('auspice'):
<div>\
${'/'.join(character['auspice'])}\
</div>
%endif
\
%if character.has_items('lodge'):
<div>\
${character.get_first('lodge')}${make_ranks(character.get_first('lodge'))}
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
\
${mdconv('*Notes:* ' + character['description'])}
\
%if character.has_items('dead'):
${mdconv('*Dead:* ' + ' '.join(character['dead']))}
%endif
