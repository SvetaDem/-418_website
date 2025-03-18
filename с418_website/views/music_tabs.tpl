% from bottle import request
% rebase('layout.tpl', title='Music Tabs', year=year)

<div class="contact-container">
    <div class="contact-info">
        <h3>Song:</h3>
        <div class="song-item">
            <img src="{{ request.query.image }}" alt="{{ request.query.song }}" class="album-cover">
            <div class="song-details">
                <h3>{{ request.query.song }}</h3>
                <p><strong>Genres:</strong> {{ request.query.genres }}</p>
            </div>
        </div>
    </div>
</div>

<div class="contact-container">
    <div class="contact-info">
        <h3>Tabs:</h3>
        <div class="tabs-container">
            <img src="{{ request.query.tab }}" alt="Tabs for {{ request.query.song }}" class="tabs-image">
        </div>
    </div>
</div>

<div class="contact-container">
    <h3>Back to:</h3>
    <div class="button-group">
        <a href="/songs" class="btn btn-custom">Songs</a>
        <a href="/" class="btn btn-custom">C418</a>
    </div>
</div>

