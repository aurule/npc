<%page args="sectioner"/>
${"<h{}>".format(sectioner.heading_level)}${sectioner.current_text}${"</h{}>".format(sectioner.heading_level)}
