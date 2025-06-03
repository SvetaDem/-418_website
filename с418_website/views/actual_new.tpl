% rebase('layout.tpl', title='Actual new C418`s releases')

<div class="container body-content">
    <div class="head">
        <h1>Actual new C418`s releases</h1>
    </div>

    % if errors:
    <div class="contact-container validation-summary-errors">
        <h3>Errors:</h3>
        <ul>
            % for error in errors:
            <li>{{error}}</li>
            % end
        </ul>
    </div>
    % end

    <div class="contact-container">
        <div class="contact-info">
            <h3>Add New Release</h3>
            <form action="/add_song" method="post">
                <p>
                    <label for="author">Name:</label><br>
                    <input type="text" id="author" name="author" value="{{form_data['author']}}" required>
                </p>
                <p>
                    <label for="description">Description:</label><br>
                    <textarea id="description" name="description" required>{{form_data['description']}}</textarea>
                </p>
                <p>
                    <label for="date">Date (DD.MM.YYYY):</label><br>
                    <input type="text" id="date" name="date" value="{{form_data['date']}}" required>
                </p>
                <p>
                    <button type="submit" class="btn-custom">Add</button>
                </p>
            </form>
        </div>
    </div>

    <div class="description-container move">
        <div class="description-text">
            <div class="filter-buttons">
                <a href="/actual_new?filter=recent" class="btn-custom" style="margin-right: 10px;">Recent Releases</a>
                <a href="/actual_new?filter=older" class="btn-custom">Late Releases</a>
            </div>
            <h3>List of Latest C418 Songs</h3>
            % if songs:
            % for song in songs:
            <div class="song-item">
                <div class="song-details">
                    <h3>{{song['author']}}</h3>
                    <p><strong>Date:</strong> {{song['date']}}</p>
                    <p class="quote">{{song['description']}}</p>
                </div>
            </div>
            % end
            % else:
            <p>No C418 songs available.</p>
            % end
        </div>
    </div>

    <div class="description-container links move">
        <h3>Get to Know C418's Released Songs</h3>
        <a href="/songs" class="btn-custom">Songs</a>
        <a href="/contact" class="btn-custom">Contact</a>
    </div>
</div>