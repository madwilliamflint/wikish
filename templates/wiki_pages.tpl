%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<p>Full Page List:</p>
<table border="1">
%for page in pagelist:
  <tr>
    <td><a href="/wiki/{{page}}/">{{page}}</a></td>
  </tr>
%end
</table>