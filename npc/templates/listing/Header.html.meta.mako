<%page args="metadata, encoding"/>\
<!DOCTYPE html>
<html>
<head>
    <title>${metadata['title']}</title>
    % for k, v in metadata.items():
    <%
        if k == 'title':
            continue
    %>\
<meta name="${k}" content="${v}" />
    % endfor
<meta charset="${encoding}">
</head>
<body>
