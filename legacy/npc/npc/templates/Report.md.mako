<%page args="data, tag"/>\
<%
col_width = max([len(k) for k in data.keys()])
%>\
| ${'{:<{}s}'.format(tag.title(), col_width)} | Characters |
| ${'-'*col_width} | ---------: |
%for row in data.most_common():
| ${'{:<{}s}'.format(row[0], col_width)} | ${'{:>10}'.format(row[1])} |
%endfor
[Characters by ${tag.title()}]
