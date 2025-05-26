% rebase('layout.tpl', title=title, year=year)

<div class="contact-container">
    <div class="contact-info move">
        <h3>{{ message }}</h3>
        <div class="skip-block">
            <h4>Want to add a new partner?</h4>
            <a href="#partnerForm">Go straight to the add form?</a>
        </div>

        <h4>Total Partners: {{ total_partners }}</h4>

        <h4>Partner Companies</h4>
        <div id="partnersList">
            % if no_partners:
                <p><em>No partners yet.</em></p>
            % else:
                % for partner in partners:
                    <div class="user-entry">
                        <p><strong>{{ partner['name'] }}</strong></p>
                        <p>{{ partner['description'] }}</p>
                        <ul>
                            <li>Phone: {{ partner['phone'] }}</li>
                            <li>Collaboration Date: {{ partner['date'] }}</li>
                        </ul>
                    </div>
                % end
            % end
        </div>
    </div>
</div>

<div class="contact-container">
    <div class="contact-info move">
        <h4 class="h4-form">Add Partner Form</h4>
        <!-- Print errors -->
        <p id="formError" class="form-error">{{ success_message }}</p>
        <form id="partnerForm" method="post" action="/partners">
            <table class="table-form">
                <tr>
                    <td><p>Company Name</p></td>
                    <td><input type="text" name="name" id="name" value="{{ form_data['name'] }}" placeholder="Enter company name"></td>
                </tr>
                <tr>
                    <td><p>Description</p></td>
                    <td><textarea name="description" id="description" rows="3" placeholder="Enter description">{{ form_data['description'] }}</textarea></td>
                </tr>
                <tr>
                    <td><p>Phone (+XXXXXXXXXXXX)</p></td>
                    <td><input type="text" name="phone" id="phone" value="{{ form_data['phone'] }}" placeholder="+71234567890"></td>
                </tr>
                <tr>
                    <td><p>Email</p></td>
                    <td><input type="text" name="email" id="email" value="{{ form_data.get('email', '') }}" placeholder="example@domain.com"></td>
                </tr>
                <tr>
                    <td><p>Collaboration Date (DD-MM-YYYY)</p></td>
                    <td><input type="text" name="date" id="date" value="{{ form_data['date'] }}" placeholder="20-05-2025"></td>
                </tr>
            </table>
            <input class="btn-custom" type="submit" value="Add Partner">
        </form>

        <!-- Errors -->
        <div class="validation-summary-errors">
            <ul>
                % for error in errors:
                    <li>{{ error }}</li>
                % end
            </ul>
        </div>
    </div>
</div>