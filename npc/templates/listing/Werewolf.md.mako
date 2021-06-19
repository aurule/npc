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

%if tags('pack').filled:
${tags('pack').first_value()} Pack${make_ranks(tags('pack'), tags('pack').first_value())}, \
%endif
%if tags('tribe').filled:
${tags('tribe').first_value()} Tribe${make_ranks(tags('tribe'), tags('tribe').first_value())}\
%else:
Ghost Wolf
%endif
\
% if tags('auspice').filled:

${'/'.join(tags('auspice'))}\
% endif
\
% if tags('lodge').filled:

${tags('lodge').first_value()}${make_ranks(tags('lodge'), tags('lodge').first_value())}\
% endif
% if tags('group').filled:

${', '.join(["{}{}".format(g, make_ranks(tags('group'), g)) for g in tags('group')])}\
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

