<%page args="data, tag"/>\
<table>
    <caption>Characters by ${tag.title()}</caption>
    <thead>
        <tr>
            <th>${tag.title()}</th>
            <th>Characters</th>
        </tr>
    </thead>
    <tbody>
    %for row in data.most_common():
        <tr>
            <td>${row[0]}</td>
            <td>${row[1]}</td>
        </tr>
    %endfor
    </tbody>
</table>
