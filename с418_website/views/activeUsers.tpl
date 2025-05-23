% rebase('layout.tpl', title=title, year=year)

<h2>Активные пользователи</h2>

% if error:
  <p class="error">{{error}}</p>
% end

<form action="/active_users" method="post">
  <p><input type="text" name="username" placeholder="Ваш ник" value="{{username or ''}}"></p>
  <p><textarea name="description" rows="3" placeholder="Опишите свою активность">{{description or ''}}</textarea></p>
  <p><input type="text" name="date" placeholder="Дата (ГГГГ-ММ-ДД)" value="{{date or ''}}"></p>
  <p><input type="submit" value="Разместить"></p>
</form>

<hr>

<ul>
% for user in users:
  <li><strong>{{user['username']}}</strong> ({{user['date']}}): {{user['description']}}</li>
% end
</ul>
