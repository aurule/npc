<%page args="tags, header_level"/>\
<%!
def make_ranks(group_tag, subtag_name=None):
    if not subtag_name:
        subtag_name = group_tag.first_value()
    if group_tag.subtag(subtag_name).filled:
        return ' (' + ', '.join(group_tag.subtag(subtag_name)) + ')'
    return ''
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
% if tags('group').filled:
, ${tags('group').first_value()}${make_ranks(tags('group'))}\
% endif
\
% if 'motley' in tags:
, ${tags('motley').first_value()} Motley${make_ranks(tags('motley'))}\
% endif
\
% if tags('group').remaining().filled:

${', '.join(["{}{}".format(g, make_ranks(tags('group'), g)) for g in tags('group').remaining()])}\
% endif

% if tags('appearance').filled:

*Appearance:* ${' '.join(tags('appearance'))}
% endif
%if tags('description').filled:

*Notes:* ${"\n".join(tags('description'))}
% endif
\
% if tags('dead').filled:

*Dead:* ${' '.join(tags('dead'))}
% endif

