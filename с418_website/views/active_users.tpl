% rebase('layout.tpl', title=title, year=year)

<div class="contact-container">
    <div class="contact-info">
        <h3>Active Users</h3>
        <div class="skip-block">
            <h4>Want to add a new user?</h4>
            <a href="#userForm">Go straight to the add form &rarr;</a>
        </div>

        <h4>User List</h4>
        % if users:
            % for username, info in users.items():
            <div class="user-entry">
                <p><strong>{{ username }}</strong></p>
                <p>{{ info["description"] }}</p>
                <ul>
                    <li>Birthday: {{ info["birthday"] }}</li>
                    <li>Phone: {{ info["telephone"] }}</li>
                    <li>Added: {{ info["add_date"] }}</li>
                </ul>
            </div>
            % end
        % else:
            <p><em>No active users found.</em></p>
        % end
    </div>
</div>

<div class="contact-container">
    <div class="contact-info">
        <h4 class="h4-form">Add User Form</h4>
        <!--Print error-->
        <p id="formError" class="form-error"></p>
        <form id="userForm">
            <table class="table-form">
                <tr>
                    <td><p>Username</p</td>
                    <td><input type="text" name="username" id="username" placeholder="Your name"></td>
                </tr>
                <tr>
                    <td><p>Describe your activity</p></td>
                    <td><textarea name="description" id="description" rows="3" placeholder="Description"></textarea></td>
                </tr>
                <tr>
                    <td><p>Birthday</p></td>
                    <td><input type="text" name="date" id="date" placeholder="dd.mm.yyyy"></td>
                </tr>
                <tr>
                    <td><p>Telephone</p></td>
                    <td><input type="text" name="telephone" id="telephone" placeholder="+7(xxx)xxx-xx-xx"></td>
                </tr>
            </table>
            <input type="submit" value="Add">
        </form>
    </div>
</div>

<script src="/static/scripts/user_form.js"></script>