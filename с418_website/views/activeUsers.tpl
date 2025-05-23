% rebase('layout.tpl', title=title, year=year)

<h2>�������� ������������</h2>

% if error:
  <p class="error">{{error}}</p>
% end

<form action="/active_users" method="post">
  <p><input type="text" name="username" placeholder="��� ���" value="{{username or ''}}"></p>
  <p><textarea name="description" rows="3" placeholder="������� ���� ����������">{{description or ''}}</textarea></p>
  <p><input type="text" name="date" placeholder="���� (����-��-��)" value="{{date or ''}}"></p>
  <p><input type="submit" value="����������"></p>
</form>

<hr>

<ul>
% for user in users:
  <li><strong>{{user['username']}}</strong> ({{user['date']}}): {{user['description']}}</li>
% end
</ul>
