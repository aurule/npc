<%page args="metadata"/>\
% for k, v in metadata.items():
<meta name="${k}" content="${v}" />
% endfor
