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
% if character.has_items('foreign'):
 in ${' and '.join(character['foreign'])}\
% endif
% if character.has_items('group'):
, ${character.get_first('group')}${make_ranks((character.get_first('group')))}\
% endif
\
% if character.has_items('motley'):

    % for motley in character['motley']:
${motley} Motley${make_ranks(motley)}\
        % if not loop.last:
, \
        % endif
    % endfor
% endif
\
% if character.has_items('group'):

    % for group in character.get_remaining('group'):
${group}${make_ranks(group)}\
        % if not loop.last:
, \
        % endif
    % endfor
% endif


% if character.has_items('appearance'):
*Appearance:* ${' '.join(character['appearance'])}
% endif

${character['description']}
\
% if character.has_items('dead'):
${' '.join(character['dead'])}
% endif\
