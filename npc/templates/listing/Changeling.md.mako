<%page args="tags, header_level"/>\
<%!
def make_ranks(group_tag, subtag_name=None):
    if not subtag_name:
        subtag_name = group_tag.first_value()
    if group_tag.subtag(subtag_name).filled:
        return '(' + ', '.join(group_tag.subtag(subtag_name)) + ')'
%>\
<%def name="locations()">\
<%
    return tags('foreign').filled_data + tags('location').filled_data
    %>
</%def>\
${'#' * header_level} ${tags('name').first_value()}\
% if tags('dead').present:
 (Deceased)\
% endif


% if tags('name').remaining().filled:
*AKA ${', '.join(tags('name').remaining())}*
% endif
% if tags('title').filled:
${', '.join(tags('title'))}
% endif
\
${'/'.join(tags('type'))}\
%if locations():
 in ${' and '.join(locations())}\
%elif tags('foreign').present:
 (foreign)\
%endif
% if tags('wanderer').present:
, Wanderer\
% endif
% if tags('motley').filled:
, ${tags('motley').first_value()} Motley${make_ranks(tags('motley'), tags('motley').first_value())}\
% endif
% if tags('court').filled:
, ${tags('court').first_value()} Court${make_ranks(tags('court'), tags('court').first_value())}\
% else:
, Courtless\
% endif
% if tags('freehold').filled:
 (${tags('freehold').first_value()})\
% endif
\
<%
has_seeming = tags('seeming').filled
has_kith = tags('kith').filled
%>\
% if has_seeming or has_kith:

    % if has_seeming:
${'/'.join(tags('seeming'))}\
    % endif
    % if has_seeming and has_kith:
${' '}\
    % endif
    % if has_kith:
${'/'.join(tags('kith'))}\
    % endif
\
% endif
\
% if tags('court').remaining().filled:

${', '.join(["{} Court{}".format(g, make_ranks(tags('court'), g)) for g in tags('court').remaining()])}\
% endif
% if tags('motley').remaining().filled:

${', '.join(["{} Motley{}".format(g, make_ranks(tags('motley'), g)) for g in tags('motley').remaining()])}\
% endif
% if tags('entitlement').filled:

${tags('entitlement').first_value()}${make_ranks(tags('entitlement'), tags('entitlement').first_value())}\
% endif
% if tags('group').filled:

${', '.join(["{}{}".format(g, make_ranks(tags('group'), g)) for g in tags('group')])}\
% endif

% if tags('appearance').filled:

*Appearance:* ${' '.join(tags('appearance'))}
% endif
% if tags('mien').filled:

*Mien:* ${' '.join(tags('mien'))}
% endif
% if tags('mask').filled:

*Mask:* ${' '.join(tags('mask'))}
% endif
%if tags('description').filled:

*Notes:* ${"\n".join(tags('description'))}
% endif
\
% if tags('dead').filled:

*Dead:* ${' '.join(tags('dead'))}
% endif

