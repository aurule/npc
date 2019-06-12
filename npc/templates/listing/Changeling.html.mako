<%page args="tags, header_level, mdconv"/>\
<%def name="make_ranks(group_tag, subtag_name=None)">\
<%
    if not subtag_name:
        subtag_name = group_tag.first_value()
    %>\
    %if group_tag.subtag(subtag_name).filled:
<% return ' (' + ', '.join(group_tag.subtag(subtag_name)) + ')' %>\
    %endif
</%def>\
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
%if tags('motley').filled:
, ${tags('motley').first_value()} Motley${make_ranks(tags('motley'), tags('motley').first_value())}\
%endif
%if tags('court').filled:
, ${tags('court').first_value()} Court${make_ranks(tags('court'), tags('court').first_value())}\
%else:
, Courtless\
%endif
%if tags('freehold').filled:
 (${tags('freehold').first_value()})\
%endif
</div>
\
<%
has_seeming = tags('seeming').filled
has_kith = tags('kith').filled
%>\
% if has_seeming or has_kith:
<div>\
    % if has_seeming:
${'/'.join(tags('seeming'))}\
        %if has_kith:
${' '}\
        %endif
    %endif
    % if has_kith:
${'/'.join(tags('kith'))}\
    %endif
</div>
%endif
\
%if tags('entitlement').filled:
<div>\
${tags('entitlement').first_value()}${make_ranks(tags('entitlement'))}\
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
%if tags('mien').filled:
${mdconv('*Mien:* ' + ' '.join(tags('mien')))}
%endif
%if tags('mask').filled:
${mdconv('*Mask:* ' + ' '.join(tags('mask')))}
%endif
\
%if tags('description').filled:
${mdconv('*Notes:* ' + "\n".join(tags('description')))}
%endif
\
%if tags('dead').filled:
${mdconv('*Dead:* ' + ' '.join(tags('dead')))}
%endif
