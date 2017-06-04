%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<p>Search Results</p>

Searching for <i><a href="/wiki/{{pagename}}/">{{pagename}}</a></i>

<ol>
%for page in items:
  <li><a href="/wiki/{{page}}/">{{page}}</a></li>
%end
</ol>
<hr/>