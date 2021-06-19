<%page args="tags, header_level, mdconv"/>\
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
%if tags('group').filled:
, ${tags('group').first_value()} ${make_ranks(tags('group'))}\
%endif
</div>
\
%if 'motley' in tags:
<div>\
${tags('motley').first_value()} Motley ${make_ranks(tags('motley'))}\
</div>
%endif
\
%if tags('group').remaining().filled:
<div>\
${', '.join(["{} {}".format(g, make_ranks(tags('group'), g)) for g in tags('group').remaining()])}\
</div>
%endif
\
%if tags('appearance').filled:
${mdconv('*Appearance:* ' + ' '.join(tags('appearance')))}
%endif
\
%if tags('ban').filled:
${mdconv('*Ban:* ' + ' '.join(tags('ban')))}
%endif
\
%if tags('description').filled:
${mdconv('*Notes:* ' + "\n".join(tags('description')))}
%endif
\
%if tags('dead').filled:
${mdconv('*Dead:* ' + ' '.join(tags('dead')))}
%endif
