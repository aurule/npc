<%page args="metadata"/>\
% for k, v in metadata.items():
${k.title()}: ${v}
% endfor

