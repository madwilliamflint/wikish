%#template for editing a wikipage
%#the template expects to receive a value for "no" as well a "old", the text of the selected ToDo item
<p>Editing page {{pagename}}</p>
<form action="/wiki/save/{{pagename}}" method="post">
  <textarea rows="10" cols="60" name="content">{{body}}</textarea>
  <br/>
  <input type="submit" name="save" value="save">
</form>