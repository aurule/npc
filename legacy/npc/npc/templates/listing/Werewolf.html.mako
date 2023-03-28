<%page args="tags, header_level, mdconv"/>\
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
${"<h{}>".format(header_level)}\
${tags('name').first_value()}\
%if tags('dead').present:
 (Deceased)\
%endif
${"</h{}>".format(header_level)}

%if tags('name').remaining().filled:
<div><em>AKA ${', '.join(tags('name').remaining())}</em></div>
%endif
%if tags('title').filled:
<div>${', '.join(tags('title'))}</div>
%endif
\
<div>${'/'.join(tags('type'))}\
%if locations():
 in ${' and '.join(locations())}\
%elif tags('foreign').present:
 (foreign)\
%endif
%if tags('wanderer').present:
, Wanderer\
%endif

%if tags('pack').filled:
<br />${tags('pack').first_value()} Pack${make_ranks(tags('pack'), tags('pack').first_value())}, \
%endif
%if tags('tribe').filled:
${tags('tribe').first_value()} Tribe${make_ranks(tags('tribe'), tags('tribe').first_value())}\
%else:
Ghost Wolf
%endif
</div>
\
% if tags('auspice').filled:
<div>\
${'/'.join(tags('auspice'))}\
</div>
%endif
\
% if tags('lodge').filled:
<div>\
${tags('lodge').first_value()}${make_ranks(tags('lodge'), tags('lodge').first_value())}\
</div>
%endif
\
% if tags('group').filled:
<div>\
${', '.join(["{}{}".format(g, make_ranks(tags('group'), g)) for g in tags('group')])}\
</div>
%endif
\
%if tags('appearance').filled:
${mdconv('*Appearance:* ' + ' '.join(tags('appearance')))}
%endif
\
%if tags('description').filled:
${mdconv('*Notes:* ' + "\n".join(tags('description')))}
%endif
\
%if tags('dead').filled:
${mdconv('*Dead:* ' + ' '.join(tags('dead')))}
%endif
