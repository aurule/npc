<%page args="character"/>
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
%if character.has_items('foreign'):
 in ${' and '.join(character['foreign'])}\
%endif
%if 'wanderer' in character:
, Wanderer\
%endif
%if character.has_items('motley'):
, ${character.get_first('motley')} Motley${make_ranks(character.get_first('motley'))}\
%endif
%if character.has_items('court'):
, ${character.get_first('court')} Court${make_ranks(character.get_first('court'))}\
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
<p markdown="1"><em>Appearance:</em> ${' '.join(character['appearance'])}</p>
%endif
%if character.has_items('mien'):
<p markdown="1"><em>Mien:</em> ${' '.join(character['mien'])}</p>
%endif
%if character.has_items('mask'):
<p markdown="1"><em>Mask:</em> ${' '.join(character['mask'])}</p>
%endif
\
<p markdown="1"><em>Notes:</em> ${character['description']}</p>
\
%if character.has_items('dead'):
<p markdown="1"><em>Dead:</em> ${' '.join(character['dead'])}</p>
%endif
