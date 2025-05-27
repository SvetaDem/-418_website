% rebase('layout.tpl', title=title, year=year)

<div class="head">
    <h2>{{ message }}</h2>
</div>

<div class="partners-container">
    <!-- Отображение ошибок -->
    % if errors:
        <div class="validation-summary-errors">
            <ul>
                % for error in errors:
                    <li>{{ error }}</li>
                % end
            </ul>
        </div>
    % end

    <!-- Сообщение об успехе -->
    % if not errors and request.method == 'POST':
        <div class="success-message">
            <p>Partner added successfully!</p>
        </div>
    % end

    <!-- Форма добавления партнёра -->
    <div class="partner-form">
        <h3>Add a New Partner</h3>
        <form method="post" action="/partners">
            <div class="form-group">
                <label for="name">Company Name:</label>
                <input type="text" name="name" id="name" value="{{ form_data['name'] }}" class="form-control" />
            </div>
            <div class="form-group">
                <label for="description">Description:</label>
                <textarea name="description" id="description" class="form-control">{{ form_data['description'] }}</textarea>
            </div>
            <div class="form-group">
                <label for="phone">Phone (+X-XXX-XXX-XXXX):</label>
                <input type="text" name="phone" id="phone" value="{{ form_data['phone'] }}" class="form-control" />
            </div>
            <div class="form-group">
                <label for="date">Collaboration Date (YYYY-MM-DD):</label>
                <input type="text" name="date" id="date" value="{{ form_data['date'] }}" class="form-control" />
            </div>
            <button type="submit" class="btn btn-custom">Add Partner</button>
        </form>
    </div>

    <!-- Список партнёров -->
    <div class="partners-list">
        <h3>Partner Companies</h3>
        % if not partners:
            <p>No partners yet.</p>
        % else:
            % for partner in partners:
                <div class="partner-item">
                    <h4>{{ partner['name'] }}</h4>
                    <p><strong>Description:</strong> {{ partner['description'] }}</p>
                    <p><strong>Phone:</strong> {{ partner['phone'] }}</p>
                    <p><strong>Collaboration Date:</strong> {{ partner['date'] }}</p>
                </div>
            % end
        % end
    </div>
</div>