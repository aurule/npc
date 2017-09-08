<%page args="character"/>\
<%def name="make_ranks(group_name)">\
    % if group_name in character['rank']:
 (${', '.join(character['rank'][group_name])})\
    % endif
</%def>\
# ${character.get_first('name')}\
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
% if character.has_items('foreign') or character.has_items('location'):
 in ${' and '.join(character['foreign'] + character['location'])}\
% endif
% if 'wanderer' in character:
, Wanderer\
% endif
% if character.has_items('motley'):
, ${character.get_first('motley')} Motley${make_ranks((character.get_first('motley')))}\
% endif
% if character.has_items('court'):
, ${character.get_first('court')} Court${make_ranks((character.get_first('court')))}\
% else:
, Courtless
% endif
% if character.has_items('freehold'):
 (${character.get_first('freehold')})
% endif
\
<%
has_seeming = character.has_items('seeming')
has_kith = character.has_items('kith')
%>\
% if has_seeming or has_kith:

    % if has_seeming:
${'/'.join(character['seeming'])}\
    % endif
    % if has_seeming and has_kith:
${' '}\
    % endif
    % if has_kith:
${'/'.join(character['kith'])}\
    % endif
\
% endif
\
% if character.has_items('court', 2):

    % for court in character.get_remaining('court'):
${court} Court${make_ranks(court)}\
        % if not loop.last:
, \
        % endif
    % endfor
% endif
% if character.has_items('motley', 2):

    % for motley in character.get_remaining('motley'):
${motley} Motley${make_ranks(motley)}\
        % if not loop.last:
, \
        % endif
    % endfor
% endif
% if character.has_items('entitlement'):

${character.get_first('entitlement')}${make_ranks(character.get_first('entitlement'))}\
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
% if character.has_items('mien'):

*Mien:* ${' '.join(character['mien'])}
% endif
% if character.has_items('mask'):

*Mask:* ${' '.join(character['mask'])}
% endif

*Notes:* ${character['description']}
% if character.has_items('dead'):

*Dead:* ${' '.join(character['dead'])}
% endif

