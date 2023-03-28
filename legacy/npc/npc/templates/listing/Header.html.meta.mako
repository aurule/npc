<%page args="metadata, encoding"/>\
<!DOCTYPE html>
<html>
<head>
    % for k, v in metadata.items():
        % if k == 'title':
    <title>${v}</title>
        % else:
    <meta name="${k}" content="${v}" />
        % endif
    % endfor
    <meta charset="${encoding}">
</head>
<body>
