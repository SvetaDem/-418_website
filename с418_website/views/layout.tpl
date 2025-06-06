<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - C418</title>
    <link rel="stylesheet" type="text/css" href="/static/content/bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="/static/content/site.css" />
    <script src="/static/scripts/modernizr-2.6.2.js"></script>
</head>

<body>
    <div class="navbar navbar-inverse navbar-fixed-top">
        <div class="container">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a href="/" class="navbar-brand">C418</a>
            </div>
            <div class="navbar-collapse collapse">
                <ul class="nav navbar-nav">
                    <li class="{{ 'active' if request.path == '/about' else '' }}"><a href="/about">About</a></li>
                    <li class="{{ 'active' if request.path == '/contact' else '' }}"><a href="/contact">Contact</a></li>
                    <li class="{{ 'active' if request.path == '/songs' else '' }}"><a href="/songs">C418 Songs</a></li>
                    <li class="{{ 'active' if request.path == '/biography' else '' }}"><a href="/biography">Biography</a></li>
                    <li class="{{ 'active' if request.path == '/active_users' else '' }}"><a href="/active_users">Active users</a></li>
                    <li class="{{ 'active' if request.path == '/articles' else '' }}"><a href="/articles">Articles</a></li>
                </ul>
            </div>
        </div>
    </div>

    <div class="container body-content">
        {{!base}}
        <hr />
        <footer>
            <p>&copy; {{ year }} - C418</p>
        </footer>
    </div>

    <script src="/static/scripts/jquery-1.10.2.js"></script>
    <script src="/static/scripts/bootstrap.js"></script>
    <script src="/static/scripts/respond.js"></script>

</body>
</html>
