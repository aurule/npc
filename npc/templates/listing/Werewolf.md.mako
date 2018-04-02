<%page args="character, header_level"/>\
<%def name="make_ranks(group_name)">\
    % if group_name in character['rank']:
 (${', '.join(character['rank'][group_name])})\
    % endif
</%def>\
${'#' * header_level} ${character.get_first('name')}\
% if 'dead' in character:
 (Deceased)\
% endif


% if character.has_items('name', 2):
*AKA ${', '.join(character.get_remaining('name'))}*
% endif
\
% if character.has_items('title'):
${', '.join(character['title'])}
% endif
\
${character.get_first('type')}\
%if character.has_locations:
 in ${' and '.join(character.locations)}\
%elif character.has_items('foreign'):
 (foreign)
%endif
% if 'wanderer' in character:
, Wanderer\
% endif
%if character.has_items('pack'):
, ${character.get_first('pack')} Pack${make_ranks(character.get_first('pack'))}\
%endif
%if character.has_items('tribe'):
, ${character.get_first('tribe')} Tribe${make_ranks(character.get_first('tribe'))}\
%else:
, Ghost Wolf
%endif
\
% if character.has_items('auspice'):

${'/'.join(character['auspice'])}\
% endif
\
% if character.has_items('lodge'):

${character.get_first('lodge')}${make_ranks(character.get_first('lodge'))}\
% endif
% if character.has_items('group'):

    % for group in character['group']:
${group}${make_ranks(group)}\
        % if not loop.last:
, \
        % endif
    % endfor
% endif

% if character.has_items('appearance'):

*Appearance:* ${' '.join(character['appearance'])}
% endif

*Notes:* ${character['description']}
% if character.has_items('dead'):

*Dead:* ${' '.join(character['dead'])}
% endif

