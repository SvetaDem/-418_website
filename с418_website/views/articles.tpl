% rebase('layout.tpl', title='Useful Articles about C418')

<div class="container body-content">
    <div class="head">
        <h1>Useful Articles about C418</h1>
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
            <h3>Add New Article about C418</h3>
            <form action="/add_article" method="post">
                <p>
                    <label for="author">Author:</label><br>
                    <input type="text" id="author" name="author" value="{{form_data['author']}}" required>
                </p>
                <p>
                    <label for="title">Title:</label><br>
                    <input type="text" id="title" name="title" value="{{form_data['title']}}" required>
                </p>
                <p>
                    <label for="text">Text:</label><br>
                    <textarea id="text" name="text" required>{{form_data['text']}}</textarea>
                </p>
                <p>
                    <label for="date">Date (DD.MM.YYYY):</label><br>
                    <input type="text" id="date" name="date" value="{{form_data['date']}}" required>
                </p>
                <p>
                    <button type="submit" class="btn-custom">Add Article</button>
                </p>
            </form>
        </div>
    </div>

    <div class="description-container center-blocks"> 
        <img src="/static/images/face2.jpg" alt="C418" class="album-cover-all"> 
    </div>

    <div class="description-container move">
        <div class="description-text">
            <h3>List of Articles about C418</h3>
            % if articles:
            % for article in articles:
            <div class="song-item">
                <div class="song-details">
                    <h3>{{article['title']}}</h3>
                    <p><strong>Author:</strong> {{article['author']}}</p>
                    <p><strong>Date:</strong> {{article['date']}}</p>
                    <p class="quote">{{article['text']}}</p>
                </div>
            </div>
            % end
            % else:
            <p>No articles about C418 available.</p>
            % end
        </div>
    </div>

    <div class="description-container links move">
        <h3>Explore More about C418</h3>
        <a href="/songs" class="btn-custom">Songs</a>
        <a href="/contact" class="btn-custom">Contact</a>
    </div>
</div>